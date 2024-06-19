

from typing import Dict, List, Set, Tuple

from fastapi import WebSocket
from pydantic import BaseModel

from osiris.services.chats_service.chat_service import ChatService

active_connections: Dict[int, WebSocket] = {}

# ToDo inheritence is not 


class ErrorWsMessage(BaseModel):
    msg_type: str = "error"
    text: str

    def __init__(self, text):
        super().__init__(text=text)


class BaseWsMessage(BaseModel):
    msg_type: str

    async def can_apply(self, service: ChatService, user_id: int) -> bool:
        pass

    async def apply(self, service: ChatService, user_id: int) -> Tuple[Set[int], BaseModel]:
        pass


class ChatCreatedWsMessage(BaseModel):
    msg_type: str = "chat_created"
    chat_id: int
    user_list: List[int]
    chat_name: str

class CreateChatWsMessage(BaseModel):
    msg_type: str = "create_chat"
    chat_name: str
    # ToDo
    user_list: List[int]

    async def can_apply(self, service: ChatService, user_id: int) -> bool:
        return True
    
    async def apply(self, service: ChatService, user_id: int) -> Tuple[Set[int], BaseModel]:
        user_list = set(self.user_list).add(user_id)
        chat_model = await service.create_chat(
            name=self.chat_name,
            users=list(user_list)
        )

        return user_list, ChatCreatedWsMessage(
            chat_id=chat_model.id,
            user_list=list(user_list),
            chat_name=chat_model.name
        )


class MessageCreatedWsMessage(BaseModel):
    msg_type: str = "msg_created"
    msg_id: int
    chat_id: int
    author: str
    message_text: str

class CreateMessageWsMessage(BaseModel):
    msg_type: str = "create_msg"
    chat_id: int
    msg_text: str

    async def can_apply(self, service: ChatService, user_id: int) -> bool:
        return await service.has_user_chat(user_id, self.chat_id)
    
    async def apply(self, service: ChatService, user_id: int) -> Tuple[Set[int], BaseModel]:
        message_model = await service.create_message(
            chat_id=self.chat_id,
            user_id=user_id,
            message_text=self.msg_text
        )
        user_list = await service.get_users_by_chat_id(self.chat_id)
        autor = (await service.get_user_by_id(user_id))

        return set(user_list), MessageCreatedWsMessage(
            msg_id=message_model.id,
            chat_id=message_model.chat_id,
            author=autor.login,
            message_text=message_model.content
        )

