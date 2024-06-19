from pydantic import BaseModel

class ChatBriefSchema(BaseModel):
    chat_id: int
    name: str

class MessageBriefSchema(BaseModel):
    chat_id: int
    author_id: int
    author: str
    creation_ts: int
    text: str

class SendedMessage(BaseModel):
    chat_id: int
    message_text: str
