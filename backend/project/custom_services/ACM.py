import requests


def get_acm_reponse(payload):
    response = requests.post("http://localhost:8888/api/moderate", data=payload)
