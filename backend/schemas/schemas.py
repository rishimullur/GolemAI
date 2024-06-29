import pydantic
from datetime import datetime
from typing import List, Optional


class UserBase(pydantic.BaseModel):
    username: str
    group_id: str
    full_name: Optional[str] = None
    user_id: Optional[int] = None


class ChatBase(pydantic.BaseModel):
    chat_id: int
    min_responses: Optional[int] = 4
    users: List[UserBase]
    messages: List["MessageBase"] = []


class MessageBase(pydantic.BaseModel):
    message_id: int
    sender: UserBase
    text: str
    date: datetime
