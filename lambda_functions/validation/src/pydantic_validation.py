from pydantic import BaseModel
from typing import Type
def validate(baseModel: Type[BaseModel], dataJSON: str):
    return baseModel.model_validate_json(dataJSON)