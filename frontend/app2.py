import streamlit as st
import uuid
import os
import json
from datetime import datetime

# Define file paths
group_file_path = "group_data.txt"
chat_file_path = "chat_data.txt"

# Define Pydantic models
class UserBase(pydantic.BaseModel):
    username: str
    group_id: str
    full_name: Optional[str] = None
    user_id: Optional[str] = None

class ChatBase(pydantic.BaseModel):
    chat_id: int
    min_responses: Optional[int] = 4
    users: List[UserBase]

class MessageBase(pydantic.BaseModel):
    message_id: int
    chat: ChatBase
    sender: UserBase
    text: str
    date: datetime

# Function to load group data from the file
def load_group_data():
    if os.path.exists(group_file_path):
        with open(group_file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                group_data = json.loads(line.strip())
                group_code = group_data['group_id']
                user_id = group_data['user_id']
                username = group_data['username']
                if group_code not in st.session_state['groups']:
                    st.session_state['groups'][group_code] = {}
                st.session_state['groups'][group_code][user_id] = username

# Function to save user data to the file
def save_user_data(user: UserBase):
    with open(group_file_path, "a") as file:
        file.write(user.json() + "\n")

# Function to load chat data from the file
def load_chat_data():
    if os.path.exists(chat_file_path):
        with open(chat_file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                chat_data = json.loads(line.strip())
                group_code = chat_data['chat']['group_id']
                user_id = chat_data['sender']['user_id']
                message = chat_data['text']
                if group_code not in st.session_state['chats']:
                    st.session_state['chats'][group_code] = {}
                if user_id not in st.session_state['chats'][group_code]:
                    st.session_state['chats'][group_code][user_id] = []
                st.session_state['chats'][group_code][user_id].append(message)

# Function to save chat data to the file
def save_chat_data(message: MessageBase):
    with open(chat_file_path, "a") as file:
        file.write(message.json() + "\n")

# Initialize session state to store group data and chat data
if 'groups' not in st.session_state:
    st.session_state['groups'] = {}
    load_group_data()

if 'chats' not in st.session_state:
    st.session_state['chats'] = {}
    load_chat_data()

if 'user' not in st.session_state:
    st.session_state['user'] = None

def show_chat_interface():
    st.title(f"Group Chat: {st.session_state['user'].group_id}")

    # Display existing users in the group on the left
    st.sidebar.title("Users in this group")
    for uid, uname in st.session_state['groups'][st.session_state['user'].group_id].items():
        st.sidebar.write(f"{uname} (User ID: {uid})")

    # Chat interface
    user_input = st.text_input("You: ")

    if user_input:
        # Save the user message
        message = MessageBase(
            message_id=len(st.session_state['chats'][st.session_state['user'].group_id].get(st.session_state['user'].user_id, [])) + 1,
            chat=ChatBase(
                chat_id=1,  # assuming single chat per group
                users=[st.session_state['user']]
            ),
            sender=st.session_state['user'],
            text=user_input,
            date=datetime.now()
        )
        save_chat_data(message)

        # Placeholder response (this could be replaced with actual chatbot logic)
        response = MessageBase(
            message_id=len(st.session_state['chats'][st.session_state['user'].group_id].get('bot', [])) + 1,
            chat=ChatBase(
                chat_id=1,
                users=[st.session_state['user']]
            ),
            sender=UserBase(username='bot', group_id=st.session_state['user'].group_id, user_id='bot'),
            text="This is a placeholder response from the bot.",
            date=datetime.now()
        )
        save_chat_data(response)

        st.experimental_rerun()

    # Display chat history for the user
    if st.session_state['user'].group_id in st.session_state['chats']:
        chat_history = st.session_state['chats'][st.session_state['user'].group_id].get(st.session_state['user'].user_id, [])
        for message in chat_history:
            st.write(f"You: {message}")
        
        bot_responses = st.session_state['chats'][st.session_state['user'].group_id].get("bot", [])
        for message in bot_responses:
            st.write(f"Bot: {message}")

if st.session_state['user'] is None:
    st.title("Group Chat Bot")

    group_code = st.text_input("Enter Group Code")
    username = st.text_input("Enter Username")

    if st.button("Submit"):
        if group_code and username:
            # Generate a unique user ID
            user_id = str(uuid.uuid4())

            # Create user object
            user = UserBase(username=username, group_id=group_code, user_id=user_id)

            # Check if the group code exists in the session state
            if group_code not in st.session_state['groups']:
                st.session_state['groups'][group_code] = {}

            # Add the user to the group
            st.session_state['groups'][group_code][user_id] = username

            # Save the user data to the file
            save_user_data(user)

            # Update session state
            st.session_state['user'] = user

            # Change screen to chat interface
            st.rerun()
else:
    show_chat_interface()
