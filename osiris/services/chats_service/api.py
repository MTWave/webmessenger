
import logging
from optparse import Option
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, Depends, WebSocket,status
from fastapi.responses import RedirectResponse
from collections import defaultdict


from osiris.models.chat_model import ChatModel
from osiris.services.auth_service.dependency import get_current_user, get_current_user_ws
from osiris.services.auth_service.models import UserJwtSchema
from osiris.services.chats_service.models import ChatBriefSchema, MessageBriefSchema, SendedMessage
from osiris.services.chats_service.chat_service import ChatService
from osiris.services.chats_service.websocket_messages import BaseWsMessage, CreateChatWsMessage, CreateMessageWsMessage, ErrorWsMessage


router = APIRouter(
    prefix="/chats",
    tags=["auth"]
)

logger = logging.getLogger("custom")

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
            author=message_model.login,
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


active_connections: Dict[int, List[WebSocket]] = defaultdict(list)


def parse_message(msg: Dict[Any, Any]) -> Optional[BaseWsMessage]:
    
    if msg.get("msg_type") is None:
        return None
    # ToDo: I want to have key IN models

    return {
        "create_chat": CreateChatWsMessage, 
        "create_msg": CreateMessageWsMessage
    }[msg["msg_type"]].model_validate(msg)


async def try_to_send_msg(user_id: int, message: BaseWsMessage):
    logger.info("Try to send msg {} to {}".format(user_id, message.model_dump_json()))
    for connection in active_connections.get(user_id, []):
        logger.info("send msg {} to {}".format(user_id, message.model_dump_json()))
        await connection.send_json(message.model_dump())


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    current_user: Optional[UserJwtSchema] = Depends(get_current_user_ws),
    service: ChatService = Depends()
):
    if current_user is None:
        return RedirectResponse(f"/sign_in")
    user_id = current_user.id

    await websocket.accept()
    active_connections[user_id].append(websocket)

    # try
    while True:
            data = await websocket.receive_json()
            # get type of mesasge
            parsered_message = parse_message(data)
            if parsered_message is None:
                await try_to_send_msg(
                    user_id,
                    ErrorWsMessage("Failed to parse message: {}".format(str(data))),
                )
                continue

            if not await parsered_message.can_apply(service, user_id):
                await try_to_send_msg(
                    user_id,
                    ErrorWsMessage("Don't have permissions for applying: {}".format(str(data)))
                )

            # ToDo: this is not thread safe! (may be AJAX requests is fixing it?)
            affected_users, message = await parsered_message.apply(service, user_id)
            for user_id in affected_users.intersection(set(active_connections.keys())):
                await try_to_send_msg(user_id, message)
    #except Exception as e:
    #    logger.warn("Failed websocket handling: {}".format(e))
    #    raise 
