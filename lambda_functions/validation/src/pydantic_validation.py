from pydantic import BaseModel
def validate(baseModel: BaseModel, dataJSON: str)->dict:
    return baseModel.model_validate_json(dataJSON)