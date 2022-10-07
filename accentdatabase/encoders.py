import json

import pydantic.json


def json_serializer(*args, **kwargs) -> str:
    """
    Encodes json in the same way that pydantic does.
    https://pydantic-docs.helpmanual.io/usage/dataclasses/#json-dumping
    """

    return json.dumps(
        *args,
        default=pydantic.json.pydantic_encoder,
        **kwargs,
    )
