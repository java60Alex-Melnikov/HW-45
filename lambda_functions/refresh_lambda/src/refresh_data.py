from pydantic import BaseModel, Base64Str

class RefreshData(BaseModel):
    refreshToken: Base64Str
