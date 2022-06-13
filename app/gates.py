from zadarma.api import ZadarmaAPI
from config import ZADARMA_API_KEY, ZADARMA_API_SECRET, ZADARMA_NUMBER, INNER_NUMBER, OUTER_NUMBER, SIP


z_api = ZadarmaAPI(key=ZADARMA_API_KEY, secret=ZADARMA_API_SECRET)


def call_number(to_number):
    return z_api.call(
        "/v1/request/callback/",
        {"from": ZADARMA_NUMBER, "to": to_number, "sip": SIP, "predicted": "1"},
    )


def call_from(from_number, to_number):
    return z_api.call(
        "/v1/request/callback/",
        {"from": from_number, "to": to_number, "sip": SIP, "predicted": "1"},
    )


def open_gates_inner():
    return call_number(INNER_NUMBER)


def open_gates_outer():
    return call_number(OUTER_NUMBER)
