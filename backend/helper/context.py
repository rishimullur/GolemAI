import os
from schemas.schemas import UserBase, ChatBase, MessageBase
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

context_dir = os.path.join(parent_dir, 'context')


def save(user_base: UserBase, chat_base: ChatBase, message_base: MessageBase):

    context = ""
    chat_id = chat_base.chat_id
    min_responses = chat_base.min_responses
    users = chat_base.users
    messages = chat_base.messages

    concat_chat = ""
    chat_id = str(chat_id)

    for message in messages:
        concat_chat += f"{message.sender.username}: {message.text}\n"

    context_dict = {
        "chat_id": chat_id,
        "min_responses": min_responses,
        "concat_chat": concat_chat
    }

    context = json.dumps(context_dict)

    try:
        with open(os.path.join(context_dir, f'{chat_id}.txt'), 'w') as f:
            f.write(context)

        return True

    except Exception as e:
        return e


def retrieve():

    with open(os.path.join(context_dir, 'context.txt'), 'r') as f:
        raw_context = f.read()

    context_dict = json.loads(raw_context)

    # context_dict = {
    #     "chat_id": chat_id,
    #     "min_responses": min_responses,
    #     "concat_chat": concat_chat
    # }

    return context_dict

    # return "Who was the president of the United States in 2016?"


