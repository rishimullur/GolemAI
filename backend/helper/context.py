import os
from schemas.schemas import UserBase, ChatBase, MessageBase

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
    for message in messages:
        concat_chat += f"{message.sender.username}: {message.text}\n"

    try:

        with open(os.path.join(context_dir, 'context.txt'), 'w') as f:
            f.write(context)

        return True

    except Exception as e:
        return e


def retrieve():

    context = ""

    with open(os.path.join(context_dir, 'context.txt'), 'w') as f:
        f.read(context)

    # return "Who was the president of the United States in 2016?"

    return "Who was the president of the United States in 2016?"


