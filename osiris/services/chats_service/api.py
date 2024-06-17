
from typing import List, Optional
from fastapi import APIRouter, Depends,status
from fastapi.responses import RedirectResponse

from osiris.models.chat_model import ChatModel
from osiris.services.auth_service.dependency import get_current_user
from osiris.services.auth_service.models import UserJwtSchema
from osiris.services.chats_service.models import ChatBriefSchema, MessageBriefSchema, SendedMessage
from osiris.services.chats_service.service import ChatService


router = APIRouter(
    prefix="/chats",
    tags=["auth"]
)


# list
@router.get(
    "/list"
    #response_model=List[ChatBriefSchema]
)
async def get_chats_list(
    current_user: Optional[UserJwtSchema] = Depends(get_current_user),
    service: ChatService = Depends()
):
    if current_user is None:
        return RedirectResponse(f"/sign_in")
    return [
        ChatBriefSchema(
            chat_id=chat_model.id,
            name=chat_model.name
        )
        for chat_model in await service.get_chats_by_user_id(current_user.id)
    ]


@router.get(
    "/{chat_id}/messages"
)
async def get_chat_messages(
    chat_id: str,
    current_user: Optional[UserJwtSchema] = Depends(get_current_user),
    service: ChatService = Depends()
):
    if current_user is None:
        return RedirectResponse(f"/sign_in")
    # ToDo checking that user is in this chat
    
    return [
        MessageBriefSchema(
            chat_id=message_model.chat_id,
            author_id=message_model.user_id,
            text=message_model.content,
            creation_ts=int(message_model.creation_date.timestamp())
        )
        for message_model in await service.get_messages_by_chat_id(chat_id, current_user.id)
    ]


@router.post(
    "/send"
)
async def get_chat_users(
    message: SendedMessage,
    current_user: Optional[UserJwtSchema] = Depends(get_current_user),
    service: ChatService = Depends()
):
    if current_user is None:
        return RedirectResponse(f"/sign_in")
    # ToDo check can send in this chat?
    await service.create_message(
        message.chat_id,
        current_user.id,
        message.message_text
    )

    return message
"""
# contacts
def create_chat():
    pass

"""