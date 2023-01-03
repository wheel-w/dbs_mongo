import json

from bson.json_util import CANONICAL_JSON_OPTIONS, dumps, loads


def bson_to_json(data):
    return json.loads(dumps(data, json_options=CANONICAL_JSON_OPTIONS))


def json_to_bson(data):
    return loads(json.dumps(data), json_options=CANONICAL_JSON_OPTIONS)
