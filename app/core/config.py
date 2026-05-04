from pydantic import BaseModel


class Settings(BaseModel):
    structural_salt: str = "CHANGE_ME"


settings = Settings()
