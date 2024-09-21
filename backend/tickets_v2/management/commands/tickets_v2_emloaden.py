"""
NOTE: Not a Django management command
usage: python -m tickets_v2.management.commands.tickets_v2_emloaden

This script simulates a large number of buyers browsing and buying tickets from the web shop.
"""

import asyncio
import logging
import multiprocessing
import resource
import sys
from collections import Counter
from enum import Enum, auto
from os import environ
from random import choice, uniform
from statistics import quantiles
from time import monotonic

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectionError, ClientResponseError

from ...optimized_server.models.api import CreateOrderResponse, GetProductsResponse
from ...optimized_server.models.customer import Customer
from ...optimized_server.models.order import Order

base_url = environ.get("BASE_URL", "http://localhost:7999")
event_slug = "tracon2025"
customer = Customer(
    firstName="John",
    lastName="Doe",
    email="john.doe@example.com",
    phone="",
)
logger = logging.getLogger("kompassi")


async def _view_products_page(session: ClientSession):
    """
    Simulates a buyer viewing the web shop page that tells if the product is available or not.
    """
    async with session.get(f"{base_url}/api/tickets-v2/events/{event_slug}/products/") as response:
        response.raise_for_status()
        data = await response.json()
        return GetProductsResponse.model_validate(data)


async def _buy_tickets(session: ClientSession, products: dict[int, int]):
    """
    Simulates a buyer buying tickets.
    """
    order_dto = Order(
        customer=customer,
        products=products,
    )

    async with session.post(
        f"{base_url}/api/tickets-v2/events/{event_slug}/orders/",
        json=order_dto.model_dump(by_alias=True),
    ) as response:
        response.raise_for_status()
        data = await response.json()
        return CreateOrderResponse.model_validate(data)


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


async def _buyer(
    max_tardiness_seconds: int = 20,
    max_time_to_buy_seconds: int = 10,
) -> tuple[Result, float | None, float | None]:
    time_loading_products = None
    time_buying_tickets = None

    await asyncio.sleep(uniform(0, max_tardiness_seconds))

    async with ClientSession() as session:
        try:
            t0 = monotonic()
            availability = await _view_products_page(session)
            time_loading_products = monotonic() - t0
        except ClientConnectionError:
            return Result.CONNECTION_ERROR, time_loading_products, time_buying_tickets
        except ClientResponseError as e:
            if e.status == 500:
                return Result.SERVER_ERROR, time_loading_products, time_buying_tickets
            raise

        if not any(product.available for product in availability.products):
            return Result.SERVED_SOLD_OUT_PAGE, time_loading_products, time_buying_tickets

        await asyncio.sleep(uniform(0, max_time_to_buy_seconds))

        # randomize desired amounts for each available product
        desired_amounts = {
            product.id: amount for product in availability.products if product.available and (amount := choice(AMOUNTS))
        }

        if not desired_amounts:
            return Result.JUST_BROWSING, time_loading_products, time_buying_tickets

        try:
            t0 = monotonic()
            await _buy_tickets(session, desired_amounts)
            time_buying_tickets = monotonic() - t0
        except ClientConnectionError as e:
            logger.error("Connection error", exc_info=e)
            return Result.CONNECTION_ERROR, time_loading_products, time_buying_tickets
        except ClientResponseError as e:
            if e.status == 409:
                return Result.NOT_ENOUGH_TICKETS, time_loading_products, time_buying_tickets
            elif e.status == 500:
                return Result.SERVER_ERROR, time_loading_products, time_buying_tickets
            raise
        else:
            return Result.SUCCESS, time_loading_products, time_buying_tickets


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
    return asyncio.run(_aprocess(num_buyers))


def main(num_processes=8, num_buyers_per_process=500):
    _check_resource_limits(num_processes * num_buyers_per_process)

    print(f"Buying tickets with {num_processes} processes and {num_buyers_per_process} buyers per process…")

    with multiprocessing.Pool(num_processes) as pool:
        t0 = monotonic()
        results = list(pool.imap_unordered(_process, [num_buyers_per_process] * num_processes))
        t1 = monotonic()

    total = Counter(result for proc_results in results for (result, _, _) in proc_results)

    tlt_quantiles = quantiles(
        (tlt for proc_results in results for (_, tlt, _) in proc_results if tlt is not None),
        n=100,
    )
    tbt_quantiles = quantiles(
        (tbt for proc_results in results for (_, _, tbt) in proc_results if tbt is not None),
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


if __name__ == "__main__":
    main()
