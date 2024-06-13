from pydantic import BaseModel


class ExceptionMessageSchema(BaseModel):
    message: str