import logging
import typing
import os

import cachetools
import requests
from cachetools import cached
cache_strategy = cachetools.TTLCache(maxsize=100, ttl=60)

AIRTABLE_TOKEN = os.getenv('AIRTABLE_TOKEN', None)

def fetch_available_posts(filters="") -> typing.Dict:
    response = requests.get(
        "https://api.airtable.com/v0/appe3wFxYkIwHibVi/%D0%A3%D1%87%D0%B0%D1%81%D1%82%D0%BA%D0%B8?view=Grid%20view&"
        +filters,
        headers={
            "Authorization": AIRTABLE_TOKEN,
        },
    )
    return response.json()["records"]

def fetch_persons_info(filters=""):
    records = []
    try:
        offset = ""
        while True:

            response = requests.get(
                f"https://api.airtable.com/v0/appe3wFxYkIwHibVi/%D0%A1%D1%83%D0%B4%D1%8C%D0%B8?view=Grid%20view&offset={offset}&"
                +filters,
                headers={
                    "Authorization": AIRTABLE_TOKEN
                },
            )
            records.extend(response.json()["records"])
            if not response.json().get("offset", False):
                break
            offset=response.json()["offset"]
        return records

    except Exception as e:
        logging.exception("Exception while fetching records in 'fetch_persons_info'", exc_info=e, extra={"filters": filters})
        logging.debug(f"EXTRA ARGS: filter: {filters}, offset: {offset}")
    finally:
        return records

@cached(cache=cache_strategy)
def get_unique_data_by_field(field: "str", table_func) -> typing.List["str"]:

    records = table_func()
    unique_set_list = set()

    for record in records:
        unique_set_list.add(record["fields"][field])

    return list(unique_set_list)

@cached(cache=cache_strategy)
def fetch_judgment_places(post: "str", area: "str"):
    try:
        posts = fetch_available_posts("filterByFormula={Должность} = " + f"'{post}'")
        persons_district = fetch_persons_info("filterByFormula={Район} = " + f"'{area}'")

        unique_post_set_list = set()
        unique_persons_district_set_list = set()

        for record in posts:
            unique_post_set_list.add(record["fields"]["Участок"])

        for record in persons_district:
            unique_persons_district_set_list.add(record["fields"]["Участок"])

        return list(unique_post_set_list & unique_persons_district_set_list)
    except Exception as e:
        logging.exception("Error in fetch_judgment_places.", exc_info=True, extra={"post": post, "area": area})