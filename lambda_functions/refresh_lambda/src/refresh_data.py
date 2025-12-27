from pydantic import BaseModel

class RefreshData(BaseModel):
    refreshToken: str
