from typing import Optional
from pydantic import BaseModel

from core.config_main.config import ALIAS


class DishParams(BaseModel):
    name: str
    description: Optional[str]

mappings = {
    "properties": {
        "name": {
            "type": "text",
            "analyzer": "elk_analyzer"
        },
        "description": {
            "type": "text",
            "analyzer": "elk_analyzer"
        }
    }
}

prepositions = [
    'на',
    "а",
    "по",
    "в",
    "у",
    "со",
    "до",
    "из",
    "из-за",
    "через",
    "из-под",
    "под",
    "над",
    "с"
]

analyzer = {
    "elk_analyzer": {
        "tokenizer": "standard",
        "filter": ["stop_prepos"]
    },
    "filter": {
        "stop_prepos": {
            "type": "stop",
            "ignore_case": "true",
            "stopwords": prepositions
        }
    }
}
settings = {
    "number_of_replicas": 0,
    "number_of_shards": 3
}

aliases = {
    "main_dish_index": {}
}

actions = [
    {"add": {"index": "<index-1>", "alias": ALIAS}}, # OPTIONAL
    {"remove": {"index": "<index-2>", "alias": ALIAS}}
]
