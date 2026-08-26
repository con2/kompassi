"""
NOTE: Not a Django management command
usage: python -m kompassi.tickets_v2.management.commands.tickets_v2_emloaden

Simulates a large number of buyers browsing and buying tickets from the web shop.

Uses an open-loop arrival model: buyers are launched on a schedule regardless of how
fast the server drains them, so the offered load can exceed what the server can absorb.
A closed-loop generator (wait for buyer N to finish before launching buyer N+1) cannot
do this, and so under-reports latency collapse by construction.

The basket model (which products, what quantities) is derived from the real tracon2026
on-sale (2026-07-12 15:00 UTC) against the production dump kompassi-20260730.sql. See
docs/tickets-v2-load-testing.md for the derivation queries, the full A/B procedure this
script is meant to run under, and the recorded baseline.
"""

try:
    from uvloop import run as asyncio_run
except ImportError:
    from asyncio import run as asyncio_run

import argparse
import asyncio
import json
import logging
import multiprocessing
import random
import resource
import sys
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum, auto
from os import environ
from statistics import quantiles
from time import monotonic
from uuid import UUID, uuid4

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectionError, ClientResponseError

from ...optimized_server.models.api import CreateOrderResponse, GetOrderResponse, GetProductsResponse
from ...optimized_server.models.customer import Customer
from ...optimized_server.models.enums import PaymentStatus
from ...optimized_server.models.order import CreateOrderRequest
from ...optimized_server.models.product import Product

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = environ.get("BASE_URL", "http://localhost:7998")
DEFAULT_API_KEY = environ.get("KOMPASSI_TICKETS_V2_API_KEY", "secret")


def get_customer() -> Customer:
    return Customer(
        first_name="John",
        last_name="Doe",
        email=f"{uuid4()}@example.com",
        phone="",
    )


# --- Basket model --------------------------------------------------------------------
#
# Derived from the product_data of the 1992 successful orders placed in the opening
# minute of the real tracon2026 on-sale. Because only successful orders leave a row,
# these are a floor on the true demand shape, not the shape itself: buyers who got
# NOT_ENOUGH_TICKETS or who only browsed are excluded from the source data.
#
# category -> substring matched case-insensitively against the product title, so this
# works against both the real tracon2026 catalogue and the perftest catalogue seeded by
# tickets_v2_setup_performance_test.
CATEGORY_PATTERNS = {
    "weekend": "viikonloppu",
    "iltabileet": "iltabile",
    "saturday": "lauantai",
    "sunday": "sunnuntai",
    "friday": "perjantai",
}

# Share of the opening-minute orders containing each product. Not mutually exclusive in
# the source data (12% of orders contained two products), so this is renormalised below
# to sum to 1 for use as a single first-product weighted pick.
_RAW_CATEGORY_WEIGHTS = {
    "weekend": 0.83,
    "iltabileet": 0.13,
    "saturday": 0.09,
    "sunday": 0.02,
    "friday": 0.02,
}
_category_weight_sum = sum(_RAW_CATEGORY_WEIGHTS.values())
CATEGORY_WEIGHTS = {category: weight / _category_weight_sum for category, weight in _RAW_CATEGORY_WEIGHTS.items()}

# Weekend ticket quantity histogram from the same opening minute, reused for every
# category as an approximation -- it is the only per-unit quantity distribution the
# source query produced.
QUANTITY_HISTOGRAM = {1: 496, 2: 586, 3: 267, 4: 163, 5: 205}
QUANTITY_CHOICES = list(QUANTITY_HISTOGRAM.keys())
QUANTITY_WEIGHTS = list(QUANTITY_HISTOGRAM.values())

# 88% of orders contained exactly one product, 12% two (the handful of three-product
# orders are folded into the two-product case here).
SECOND_PRODUCT_PROBABILITY = 0.12

# Not measurable from successful-orders-only data -- browsers leave no row. A
# conservative placeholder so the harness still exercises the JUST_BROWSING path.
JUST_BROWSING_PROBABILITY = 0.05


def _categorize_available(products: list[Product]) -> dict[str, Product]:
    result: dict[str, Product] = {}
    for product in products:
        if not product.available:
            continue
        title = product.title.lower()
        for category, pattern in CATEGORY_PATTERNS.items():
            if pattern in title:
                result[category] = product
                break
    return result


@dataclass(frozen=True)
class BuyerPlan:
    """
    A buyer's arrival time and basket, decided upfront by a single-threaded seeded RNG
    pass so the plan is reproducible regardless of how the coroutines that later carry
    it out happen to interleave at runtime.
    """

    arrival_time: float
    just_browsing: bool
    categories: list[str] = field(default_factory=list)
    quantities: list[int] = field(default_factory=list)


def _generate_arrival_times(
    rng: random.Random, rate: float, ramp_seconds: float, duration_seconds: float
) -> list[float]:
    """
    Open-loop arrival schedule via Poisson thinning: draw candidate arrivals from a
    homogeneous Poisson process at the peak rate, then keep each with probability
    rate_at(t)/rate so the ramp-up is honoured.
    """
    if rate <= 0:
        return []

    def rate_at(t: float) -> float:
        if ramp_seconds > 0 and t < ramp_seconds:
            return rate * (t / ramp_seconds)
        return rate

    arrivals: list[float] = []
    t = 0.0
    while True:
        t += rng.expovariate(rate)
        if t >= duration_seconds:
            break
        if rng.random() <= rate_at(t) / rate:
            arrivals.append(t)
    return arrivals


def _generate_buyer_plans(
    rng: random.Random, rate: float, ramp_seconds: float, duration_seconds: float
) -> list[BuyerPlan]:
    plans: list[BuyerPlan] = []
    categories = list(CATEGORY_WEIGHTS.keys())
    weights = list(CATEGORY_WEIGHTS.values())

    for arrival_time in _generate_arrival_times(rng, rate, ramp_seconds, duration_seconds):
        if rng.random() < JUST_BROWSING_PROBABILITY:
            plans.append(BuyerPlan(arrival_time, just_browsing=True))
            continue

        (first_category,) = rng.choices(categories, weights=weights, k=1)
        chosen_categories = [first_category]
        chosen_quantities = [rng.choices(QUANTITY_CHOICES, weights=QUANTITY_WEIGHTS, k=1)[0]]

        if rng.random() < SECOND_PRODUCT_PROBABILITY:
            remaining = [c for c in categories if c != first_category]
            remaining_weights = [CATEGORY_WEIGHTS[c] for c in remaining]
            (second_category,) = rng.choices(remaining, weights=remaining_weights, k=1)
            chosen_categories.append(second_category)
            chosen_quantities.append(rng.choices(QUANTITY_CHOICES, weights=QUANTITY_WEIGHTS, k=1)[0])

        plans.append(
            BuyerPlan(arrival_time, just_browsing=False, categories=chosen_categories, quantities=chosen_quantities)
        )

    return plans


# --- HTTP legs -------------------------------------------------------------------------


async def _view_products_page(session: ClientSession, base_url: str, event_slug: str) -> GetProductsResponse:
    async with session.get(f"{base_url}/api/tickets-v2/{event_slug}/products/") as response:
        response.raise_for_status()
        data = await response.json()
        return GetProductsResponse.model_validate(data)


async def _buy_tickets(
    session: ClientSession, base_url: str, event_slug: str, products: dict[int, int]
) -> CreateOrderResponse:
    order_dto = CreateOrderRequest(
        customer=get_customer(),
        products=products,
        language="en",
    )

    async with session.post(
        f"{base_url}/api/tickets-v2/{event_slug}/orders/",
        json=order_dto.model_dump(mode="json", by_alias=True),
    ) as response:
        response.raise_for_status()
        data = await response.json()
        return CreateOrderResponse.model_validate(data)


async def _view_order_page(session: ClientSession, base_url: str, event_slug: str, order_id: UUID) -> GetOrderResponse:
    async with session.get(f"{base_url}/api/tickets-v2/{event_slug}/orders/{order_id}/") as response:
        response.raise_for_status()
        data = await response.json()
        return GetOrderResponse.model_validate(data)


class Result(Enum):
    SUCCESS = auto()
    SERVED_SOLD_OUT_PAGE = auto()
    NOT_ENOUGH_TICKETS = auto()
    JUST_BROWSING = auto()
    CONNECTION_ERROR = auto()
    SERVER_ERROR = auto()
    ORDER_NOT_FOUND = auto()
    ORDER_NOT_PAID = auto()
    # Anything unforeseen: return_exceptions=True on the surrounding gather() means an
    # unhandled exception no longer aborts the whole run, it lands here instead. This
    # is what let a 401 on every request go unnoticed for 18 months.
    UNEXPECTED_ERROR = auto()


@dataclass(frozen=True)
class BuyerOutcome:
    result: Result
    time_loading_products: float | None
    time_buying_tickets: float | None
    time_viewing_order_page: float | None
    arrival_time: float
    completion_time: float
    attempted_buy: bool


async def _buyer(
    session_headers: dict[str, str],
    base_url: str,
    event_slug: str,
    plan: BuyerPlan,
    t0: float,
    sampling_factor: int = 10,
) -> BuyerOutcome:
    time_loading_products = None
    time_buying_tickets = None
    time_viewing_order_page = None
    attempted_buy = False

    def _finish(result: Result) -> BuyerOutcome:
        return BuyerOutcome(
            result=result,
            time_loading_products=time_loading_products,
            time_buying_tickets=time_buying_tickets,
            time_viewing_order_page=time_viewing_order_page,
            arrival_time=plan.arrival_time,
            completion_time=monotonic() - t0,
            attempted_buy=attempted_buy,
        )

    await asyncio.sleep(max(0.0, (t0 + plan.arrival_time) - monotonic()))

    async with ClientSession(headers=session_headers) as session:
        try:
            t_start = monotonic()
            availability = await _view_products_page(session, base_url, event_slug)
            time_loading_products = monotonic() - t_start
        except ClientConnectionError as e:
            if not random.randint(0, sampling_factor):
                logger.error("SAMPLED (1/%s): Connection error while loading products", sampling_factor, exc_info=e)
            return _finish(Result.CONNECTION_ERROR)
        except ClientResponseError as e:
            if e.status == 500:
                return _finish(Result.SERVER_ERROR)
            raise

        if not any(product.available for product in availability.products):
            return _finish(Result.SERVED_SOLD_OUT_PAGE)

        if plan.just_browsing:
            return _finish(Result.JUST_BROWSING)

        available_by_category = _categorize_available(availability.products)
        desired_amounts: dict[int, int] = {}
        for category, quantity in zip(plan.categories, plan.quantities, strict=True):
            product = available_by_category.get(category)
            if product is not None:
                desired_amounts[product.id] = desired_amounts.get(product.id, 0) + quantity

        if not desired_amounts:
            return _finish(Result.JUST_BROWSING)

        attempted_buy = True
        try:
            t_start = monotonic()
            create_order_response = await _buy_tickets(session, base_url, event_slug, desired_amounts)
            time_buying_tickets = monotonic() - t_start
        except ClientConnectionError as e:
            if not random.randint(0, sampling_factor):
                logger.error("SAMPLED (1/%s): Connection error while buying tickets", sampling_factor, exc_info=e)
            return _finish(Result.CONNECTION_ERROR)
        except ClientResponseError as e:
            if e.status == 409:
                return _finish(Result.NOT_ENOUGH_TICKETS)
            elif e.status == 500:
                return _finish(Result.SERVER_ERROR)
            raise

        if create_order_response.payment_redirect:
            raise AssertionError("Performance test should run with payments disabled")

        try:
            t_start = monotonic()
            get_order_response = await _view_order_page(session, base_url, event_slug, create_order_response.order_id)
            time_viewing_order_page = monotonic() - t_start
        except ClientConnectionError as e:
            if not random.randint(0, sampling_factor):
                logger.error("SAMPLED (1/%s): Connection error while viewing order page", sampling_factor, exc_info=e)
            return _finish(Result.CONNECTION_ERROR)
        except ClientResponseError as e:
            if e.status == 400:
                return _finish(Result.ORDER_NOT_FOUND)
            if e.status == 500:
                return _finish(Result.SERVER_ERROR)
            raise
        order = get_order_response.order

        if order.status != PaymentStatus.PAID:
            return _finish(Result.ORDER_NOT_PAID)

        return _finish(Result.SUCCESS)


def _check_resource_limits(num_buyers: int):
    nofile_soft, nofile_hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    new_nofile_soft = num_buyers + 1000
    if nofile_soft < new_nofile_soft:
        print(
            f"WARNING: RLIMIT_NOFILE is too low ({nofile_soft}). Trying to raise it to {new_nofile_soft}.",
            file=sys.stderr,
        )
        resource.setrlimit(resource.RLIMIT_NOFILE, (new_nofile_soft, nofile_hard))


@dataclass(frozen=True)
class WorkerArgs:
    worker_index: int
    seed: int
    rate: float
    ramp_seconds: float
    duration_seconds: float
    base_url: str
    event_slug: str
    api_key: str


async def _aprocess(worker_args: WorkerArgs, plans: list[BuyerPlan]) -> list[BuyerOutcome]:
    t0 = monotonic()
    headers = {"x-api-key": worker_args.api_key}
    tasks = [_buyer(headers, worker_args.base_url, worker_args.event_slug, plan, t0) for plan in plans]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    outcomes: list[BuyerOutcome] = []
    for plan, result in zip(plans, results, strict=True):
        if isinstance(result, BaseException):
            logger.error("Unexpected error in buyer", exc_info=result)
            outcomes.append(
                BuyerOutcome(
                    result=Result.UNEXPECTED_ERROR,
                    time_loading_products=None,
                    time_buying_tickets=None,
                    time_viewing_order_page=None,
                    arrival_time=plan.arrival_time,
                    completion_time=monotonic() - t0,
                    attempted_buy=False,
                )
            )
        else:
            outcomes.append(result)
    return outcomes


def _process(worker_args: WorkerArgs) -> list[BuyerOutcome]:
    rng = random.Random(worker_args.seed + worker_args.worker_index)
    plans = _generate_buyer_plans(rng, worker_args.rate, worker_args.ramp_seconds, worker_args.duration_seconds)
    _check_resource_limits(len(plans))
    return asyncio_run(_aprocess(worker_args, plans))


def _percentile_report(values: list[float]) -> dict[str, float] | None:
    # quantiles() needs at least two points; short smoke runs may not have any.
    if len(values) < 2:
        return None
    q = quantiles(values, n=100)
    return {"p50": q[49], "p95": q[94], "p99": q[98]}


def _bucket_counts(times: list[float]) -> dict[int, int]:
    counts: Counter[int] = Counter(int(t) for t in times if t >= 0)
    return dict(sorted(counts.items()))


def main(args: argparse.Namespace) -> dict:
    rate_per_process = args.rate / args.processes
    worker_args = [
        WorkerArgs(
            worker_index=i,
            seed=args.seed,
            rate=rate_per_process,
            ramp_seconds=args.ramp_seconds,
            duration_seconds=args.duration_seconds,
            base_url=args.base_url,
            event_slug=args.event_slug,
            api_key=args.api_key,
        )
        for i in range(args.processes)
    ]

    print(
        f"Offering ~{args.rate:.1f} orders/sec ({args.processes} processes x {rate_per_process:.2f}/s each) "
        f"ramping over {args.ramp_seconds:.1f}s, for {args.duration_seconds:.1f}s total, seed={args.seed}…"
    )

    with multiprocessing.Pool(args.processes) as pool:
        t0 = monotonic()
        results = list(pool.imap_unordered(_process, worker_args))
        t1 = monotonic()

    outcomes = [outcome for proc_results in results for outcome in proc_results]

    total = Counter(outcome.result for outcome in outcomes)

    def _times(attr: str) -> list[float]:
        return [value for outcome in outcomes if (value := getattr(outcome, attr)) is not None]

    leg_quantiles = {
        leg: _percentile_report(_times(leg))
        for leg in ("time_loading_products", "time_buying_tickets", "time_viewing_order_page")
    }

    offered_by_second = _bucket_counts([o.arrival_time for o in outcomes if o.attempted_buy])
    achieved_by_second = _bucket_counts([o.completion_time for o in outcomes if o.result is Result.SUCCESS])

    print(f"Total wall-clock time: {t1 - t0:.4f}s")
    print()

    print(f"Buyers launched: {len(outcomes)}")
    print("Results:")
    for result, count in total.items():
        print(f"  {result.name}: {count}")
    print()

    for leg, report in leg_quantiles.items():
        print(f"{leg}:")
        if report is None:
            print("  (fewer than 2 samples)")
        else:
            print(f"  p50: {report['p50']:.4f}s")
            print(f"  p95: {report['p95']:.4f}s")
            print(f"  p99: {report['p99']:.4f}s")
        print()

    report = {
        "params": {
            "base_url": args.base_url,
            "event_slug": args.event_slug,
            "processes": args.processes,
            "rate": args.rate,
            "ramp_seconds": args.ramp_seconds,
            "duration_seconds": args.duration_seconds,
            "seed": args.seed,
        },
        "wall_clock_seconds": t1 - t0,
        "buyers_launched": len(outcomes),
        "outcomes": {result.name: count for result, count in total.items()},
        "legs": leg_quantiles,
        "offered_by_second": offered_by_second,
        "achieved_by_second": achieved_by_second,
    }

    if args.json_out:
        with open(args.json_out, "w") as f:
            json.dump(report, f, indent=2)
        print(f"Wrote JSON report to {args.json_out}")

    return report


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--event-slug", default="perftest")
    parser.add_argument("--processes", type=int, default=4)
    parser.add_argument("--rate", type=float, default=60.0, help="Target orders/sec offered at plateau.")
    parser.add_argument("--ramp-seconds", type=float, default=5.0)
    parser.add_argument(
        "--duration-seconds",
        type=float,
        default=150.0,
        help="Total offered-load duration. Default (ramp 5s + hold ~85s + 60s post-depletion) targets a sell-out "
        "of the default perftest quotas at --rate 60; lengthen for --quota-scale > 1.",
    )
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--json-out", default=None, help="Path to write a JSON report to, for A/B diffing.")
    parser.add_argument("--api-key", default=DEFAULT_API_KEY)
    return parser.parse_args(argv)


if __name__ == "__main__":
    main(_parse_args())
