"""
NOTE: Not a Django management command
usage: python -m tickets_v2.management.commands.tickets_v2_emloaden

This script simulates a large number of buyers browsing and buying tickets from the web shop.
"""

try:
    from uvloop import run as asyncio_run
except ImportError:
    from asyncio import run as asyncio_run

import asyncio
import logging
import multiprocessing
import resource
import sys
from collections import Counter
from enum import Enum, auto
from os import environ
from random import choice, randint, uniform
from statistics import quantiles
from time import monotonic
from uuid import UUID, uuid4

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectionError, ClientResponseError

from ...optimized_server.models.api import CreateOrderResponse, GetOrderResponse, GetProductsResponse
from ...optimized_server.models.customer import Customer
from ...optimized_server.models.enums import PaymentStatus
from ...optimized_server.models.order import CreateOrderRequest

base_url = environ.get("BASE_URL", "http://localhost:7998")
event_slug = "tracon2025"
logger = logging.getLogger("kompassi")


def get_customer() -> Customer:
    return Customer(
        first_name="John",
        last_name="Doe",
        email=f"{uuid4()}@example.com",
        phone="",
    )


async def _view_products_page(session: ClientSession):
    """
    Simulates a buyer viewing the web shop page that tells if the product is available or not.
    """
    async with session.get(
        f"{base_url}/api/tickets-v2/{event_slug}/products/",
    ) as response:
        response.raise_for_status()
        data = await response.json()
        return GetProductsResponse.model_validate(data)


async def _buy_tickets(session: ClientSession, products: dict[int, int]):
    """
    Simulates a buyer buying tickets.
    """
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


async def _view_order_page(session: ClientSession, order_id: UUID):
    """
    Simulates a buyer viewing the order page.
    """
    async with session.get(
        f"{base_url}/api/tickets-v2/{event_slug}/orders/{order_id}/",
    ) as response:
        response.raise_for_status()
        data = await response.json()
        return GetOrderResponse.model_validate(data)


AMOUNTS = [
    *[0] * 10,
    *[1] * 10,
    *[2] * 6,
    *[3] * 4,
    *[4] * 2,
    *[5] * 1,
]


class Result(Enum):
    SUCCESS = auto()
    SERVED_SOLD_OUT_PAGE = auto()
    NOT_ENOUGH_TICKETS = auto()
    JUST_BROWSING = auto()
    CONNECTION_ERROR = auto()
    SERVER_ERROR = auto()
    ORDER_NOT_FOUND = auto()
    ORDER_NOT_PAID = auto()


async def _buyer(
    max_tardiness_seconds: int = 0,
    max_time_to_buy_seconds: int = 0,
    sampling_factor: int = 10,
) -> tuple[Result, float | None, float | None, float | None]:
    time_loading_products = None
    time_buying_tickets = None
    time_viewing_order_page = None

    await asyncio.sleep(uniform(0, max_tardiness_seconds))

    async with ClientSession() as session:
        try:
            t0 = monotonic()
            availability = await _view_products_page(session)
            time_loading_products = monotonic() - t0
        except ClientConnectionError as e:
            if not randint(0, sampling_factor):
                logger.error("SAMPLED (1/%s): Connection error while loading products", sampling_factor, exc_info=e)
            return Result.CONNECTION_ERROR, time_loading_products, time_buying_tickets, time_viewing_order_page
        except ClientResponseError as e:
            if e.status == 500:
                return Result.SERVER_ERROR, time_loading_products, time_buying_tickets, time_viewing_order_page
            raise

        if not any(product.available for product in availability.products):
            return Result.SERVED_SOLD_OUT_PAGE, time_loading_products, time_buying_tickets, time_viewing_order_page

        await asyncio.sleep(uniform(0, max_time_to_buy_seconds))

        # randomize desired amounts for each available product
        desired_amounts = {
            product.id: amount for product in availability.products if product.available and (amount := choice(AMOUNTS))
        }

        if not desired_amounts:
            return Result.JUST_BROWSING, time_loading_products, time_buying_tickets, time_viewing_order_page

        try:
            t0 = monotonic()
            create_order_response = await _buy_tickets(session, desired_amounts)
            time_buying_tickets = monotonic() - t0
        except ClientConnectionError as e:
            if not randint(0, sampling_factor):
                logger.error("SAMPLED (1/%s): Connection error while buying tickets", sampling_factor, exc_info=e)
            return Result.CONNECTION_ERROR, time_loading_products, time_buying_tickets, time_viewing_order_page
        except ClientResponseError as e:
            if e.status == 409:
                return Result.NOT_ENOUGH_TICKETS, time_loading_products, time_buying_tickets, time_viewing_order_page
            elif e.status == 500:
                return Result.SERVER_ERROR, time_loading_products, time_buying_tickets, time_viewing_order_page
            raise

        if create_order_response.payment_redirect:
            raise AssertionError("Performance test should run with payments disabled")

        try:
            t0 = monotonic()
            get_order_response = await _view_order_page(session, create_order_response.order_id)
            time_viewing_order_page = monotonic() - t0
        except ClientConnectionError as e:
            if not randint(0, sampling_factor):
                logger.error("SAMPLED (1/%s): Connection error while viewing order page", sampling_factor, exc_info=e)
            return Result.CONNECTION_ERROR, time_loading_products, time_buying_tickets, time_viewing_order_page
        except ClientResponseError as e:
            if e.status == 400:
                return Result.ORDER_NOT_FOUND, time_loading_products, time_buying_tickets, time_viewing_order_page
            if e.status == 500:
                return Result.SERVER_ERROR, time_loading_products, time_buying_tickets, time_viewing_order_page
            raise
        order = get_order_response.order

        if order.status != PaymentStatus.PAID:
            return Result.ORDER_NOT_PAID, time_loading_products, time_buying_tickets, time_viewing_order_page

        return Result.SUCCESS, time_loading_products, time_buying_tickets, time_viewing_order_page


def _check_resource_limits(num_buyers: int):
    nofile_soft, nofile_hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    new_nofile_soft = num_buyers + 1000
    if nofile_soft < new_nofile_soft:
        print(
            f"WARNING: RLIMIT_NOFILE is too low ({nofile_soft}). Trying to raise it to {new_nofile_soft}.",
            file=sys.stderr,
        )
        resource.setrlimit(resource.RLIMIT_NOFILE, (new_nofile_soft, nofile_hard))


async def _aprocess(num_buyers: int):
    buyers = [_buyer() for _ in range(num_buyers)]
    return await asyncio.gather(*buyers)


def _process(num_buyers: int):
    _check_resource_limits(num_buyers)
    return asyncio_run(_aprocess(num_buyers))


def main(num_processes=16, num_buyers_per_process=250):
    print(f"Buying tickets with {num_processes} processes and {num_buyers_per_process} buyers per process…")

    with multiprocessing.Pool(num_processes) as pool:
        t0 = monotonic()
        results = list(pool.imap_unordered(_process, [num_buyers_per_process] * num_processes))
        t1 = monotonic()

    total = Counter(result for proc_results in results for (result, _, _, _) in proc_results)

    tlt_quantiles = quantiles(
        (tlt for proc_results in results for (_, tlt, _, _) in proc_results if tlt is not None),
        n=100,
    )
    tbt_quantiles = quantiles(
        (tbt for proc_results in results for (_, _, tbt, _) in proc_results if tbt is not None),
        n=100,
    )
    tvt_quantiles = quantiles(
        (tvt for proc_results in results for (_, _, _, tvt) in proc_results if tvt is not None),
        n=100,
    )

    print(f"Total time: {t1 - t0:.4f}s")
    print()

    print("Results:")
    for result, count in total.items():
        print(f"  {result.name}: {count}")
    print()

    print("Time to load products:")
    print(f"  p50: {tlt_quantiles[50 - 1]:.4f}s")
    print(f"  p95: {tlt_quantiles[95 - 1]:.4f}s")
    print(f"  p99: {tlt_quantiles[99 - 1]:.4f}s")
    print()

    print("Time to buy tickets:")
    print(f"  p50: {tbt_quantiles[50 - 1]:.4f}s")
    print(f"  p95: {tbt_quantiles[95 - 1]:.4f}s")
    print(f"  p99: {tbt_quantiles[99 - 1]:.4f}s")
    print()

    print("Time to view order page:")
    print(f"  p50: {tvt_quantiles[50 - 1]:.4f}s")
    print(f"  p95: {tvt_quantiles[95 - 1]:.4f}s")
    print(f"  p99: {tvt_quantiles[99 - 1]:.4f}s")
    print()


if __name__ == "__main__":
    main()
