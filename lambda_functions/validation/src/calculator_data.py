from pydantic import BaseModel
class CalculateData(BaseModel):
    op1: float
    op2: float
    operation: str