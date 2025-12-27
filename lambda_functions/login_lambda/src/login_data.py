from pydantic import BaseModel, Field
from typing import Optional

class LoginData(BaseModel):
    username: str
    password: str
    newPassword: Optional[str] = None
