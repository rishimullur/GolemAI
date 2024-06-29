import os
from schemas.schemas import UserBase, ChatBase, MessageBase

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

context_dir = os.path.join(parent_dir, 'context')


def generate_context(user_base: UserBase, chat_base: ChatBase, message_base: MessageBase):

    context = ""
    chat_id = chat_base.chat_id
    min_responses = chat_base.min_responses
    users = chat_base.users
    messages = chat_base.messages

    concat_chat = ""
    for chat in chats:
        concat_chat += f"Chat: {chat.chat_id}\n"



def retrieve_context():

    context = ""

    with open(os.path.join(context_dir, 'context.txt'), 'w') as f:
        f.write(context)

    return context


