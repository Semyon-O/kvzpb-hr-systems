import logging
import typing

import cachetools
import requests

# получение должностей
def fetch_available_posts(filters="") -> typing.Dict:
    response = requests.get(
        "http://backend:8000/api/judgment/vacancy/types"
        +filters,
        headers={
            # "Authorization": AIRTABLE_TOKEN,
        },
    )
    logging.info(response.json())
    return response.json()

def fetch_persons_info(filters=""):
    logging.info("ФИЛЬТРАЦИЯ" + filters)
    response = requests.get(
        "http://backend:8000/api/judgment/district?vacancy="
        +filters,
        headers={
            # "Authorization": AIRTABLE_TOKEN,
        },
    )
    logging.info(response.json())
    return response.json()

def fetch_candidate_status(tgid=""):
    # logging.info("ФИЛЬТРАЦИЯ" + filters)
    response = requests.get(
        "http://backend:8000/api/candidate/" + str(tgid) + "/check-status",
        headers={
            # "Authorization": AIRTABLE_TOKEN,
        },
    )
    logging.info(response.json())
    return response.json()

def post_candidate(name: str, surname: str, email: str, tgid: str):
    data = {
    "name": name,
    "surname": surname,
    "email": email,
    "telegram_id": tgid,
    }
    response = requests.post(
        "http://backend:8000/api/candidate/",
        headers={
            # "Authorization": AIRTABLE_TOKEN,
        },
        json=data
    )
    logging.info(response.json())
    return response.json()

def fetch_judgement_place_byid(filters=""):
    logging.info("ФИЛЬТРАЦИЯ" + filters)
    response = requests.get(
        "http://backend:8000/api/judgment/"
        +filters,
        headers={
            # "Authorization": AIRTABLE_TOKEN,
        },
    )
    logging.info(response.json())
    return response.json()


def get_unique_data_by_field(field: "str", table_func) -> typing.List["str"]:

    records = table_func()
    unique_set_list = set()

    for record in records:
        unique_set_list.add(record["fields"][field])

    return list(unique_set_list)

# участки
def fetch_judgment_places(district: "str", post: "int",):
     response = requests.get(
        "http://backend:8000/api/judgment/",
        headers={
            # "Authorization": AIRTABLE_TOKEN,
        },
    )
    #  logging.info(f"Жажменты без фильт {response.json()}")
    #  logging.info(f"Дист {district} ПОСТ {post}")
    #  a_list = json.loads(response.json())
     filtered_response = [
         dictionary for dictionary in response.json()
         if dictionary['district'] == district and post in dictionary['vacancies']
     ]
     logging.info(filtered_response)
     return filtered_response

def resend_document_status(tg_id):
    logging.info(f"resend_document_status: {tg_id}")
    response = requests.put(
        f"http://backend:8000/api/candidate/{tg_id}/recheck-status"
    )
    logging.info(response.json())
    return response.json()
