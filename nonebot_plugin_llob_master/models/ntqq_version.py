from pydantic import BaseModel


class NTQQVersion(BaseModel):
    main: str
    build: str


__all__ = ["NTQQVersion"]

