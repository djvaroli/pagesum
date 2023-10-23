import os
from notion_client import Client

from dotenv import load_dotenv

load_dotenv(".env")


def _get_notion_token():
    return os.environ["NOTION_TOKEN"]


def get_notion_client():
    client = Client(auth=_get_notion_token())
    return client
