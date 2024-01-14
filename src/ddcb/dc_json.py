import dataclasses
import json


class DataclassJSONEncoder(json.JSONEncoder):
    # inspired by: https://stackoverflow.com/a/51286749
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def dumps(o, **kwargs):
    return json.dumps(o, cls=DataclassJSONEncoder, **kwargs)


def dump(o, fp, **kwargs):
    return json.dump(o, fp, cls=DataclassJSONEncoder, **kwargs)
