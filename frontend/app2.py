import streamlit as st
import uuid
import os
import json
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# Define Pydantic models
class UserBase(BaseModel):
    username: str
    group_id: str
    full_name: Optional[str] = None
    user_id: Optional[str] = None

class MessageBase(BaseModel):
    message_id: int
    sender: UserBase
    text: str
    date: datetime

class ChatBase(BaseModel):
    chat_id: int
    min_responses: Optional[int] = 4
    users: List[UserBase]
    messages: List[MessageBase] = []

# File paths
group_file_path = "group_data.json"
chat_file_path = "chat_data.json"
voting_file_path = "voting_data.json"

# Function to load data from JSON file
def load_data(file_path, model):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            loaded_data = {}
            for key, value in data.items():
                loaded_data[key] = model.parse_obj(value)  # Convert to Pydantic model instance
            return loaded_data
    return {}

# Function to save data to JSON file
def save_data(file_path, data):
    data_dict = {key: value.dict() for key, value in data.items()}
    with open(file_path, "w") as file:
        json.dump(data_dict, file, default=str)

# Load initial data into session state
if 'groups' not in st.session_state:
    st.session_state['groups'] = load_data(group_file_path, UserBase)

if 'chats' not in st.session_state:
    st.session_state['chats'] = load_data(chat_file_path, ChatBase)

if 'votes' not in st.session_state:
    st.session_state['votes'] = load_data(voting_file_path, BaseModel)

# Function to save chat data to JSON file
def save_chat_data(group_code, user_id, message):
    timestamp = datetime.now().isoformat()
    if group_code not in st.session_state['chats']:
        st.session_state['chats'][group_code] = ChatBase(chat_id=len(st.session_state['chats']) + 1, users=[], messages=[])
    st.session_state['chats'][group_code].messages.append(MessageBase(message_id=len(st.session_state['chats'][group_code].messages) + 1,
                                                                       sender=UserBase(username=st.session_state['username'], group_id=group_code),
                                                                       text=message,
                                                                       date=timestamp))
    save_data(chat_file_path, st.session_state['chats'])

# Function to save user data to JSON file
def save_user_data(group_code, user_id, username):
    if group_code not in st.session_state['groups']:
        st.session_state['groups'][group_code] = UserBase(username=username, group_id=group_code, full_name=None, user_id=user_id)
    save_data(group_file_path, st.session_state['groups'])

# Function to save voting data to JSON file
def save_voting_data(votes):
    save_data(voting_file_path, votes)

# Function to display chat interface
def show_chat_interface():
    st.title(f"Group Chat: {st.session_state['group_code']}")

    # Display users in the group
    st.sidebar.title("Users in this group")
    for user in st.session_state['groups'].values():
        st.sidebar.write(f"{user.username} (User ID: {user.user_id})")

    # Input for user message
    user_input = st.text_input("You: ")

    if user_input:
        save_chat_data(st.session_state['group_code'], st.session_state['user_id'], user_input)

        # Placeholder response
        response = "This is a placeholder response from the bot."
        save_chat_data(st.session_state['group_code'], "bot", response)

        st.experimental_rerun()  # Use experimental_rerun due to st.rerun() issue

    # Display chat history
    if st.session_state['group_code'] in st.session_state['chats']:
        chat_history = st.session_state['chats'][st.session_state['group_code']].messages
        for message in chat_history:
            st.write(f"{message.date} - {message.sender.username}: {message.text}")

    if st.button("Finish Chat", key="finish_chat_button"):
        show_voting_page()

# Function to display voting page
def show_voting_page():
    st.title("Voting Page")
    st.write("Please vote for the suggested events:")

    events = ["Event 1", "Event 2", "Event 3"]  # Replace with actual events

    for event in events:
        st.write(event)
        thumbs_up = st.button(f"👍 ({st.session_state['votes'].get(event, 0)})", key=f"thumbs_up_{event}")
        thumbs_down = st.button(f"👎", key=f"thumbs_down_{event}")

        if thumbs_up:
            st.session_state['votes'][event] = st.session_state['votes'].get(event, 0) + 1
            save_voting_data(st.session_state['votes'])
        if thumbs_down:
            # Implement thumbs down functionality if needed
            pass

    st.title("Results")
    main_event = max(st.session_state['votes'], key=st.session_state['votes'].get)
    st.write(f"The main event is: {main_event}")

    st.write("Event Details:")
    st.write("Event details here...")

    if st.button("Finish Voting", key="finish_voting_button"):
        # Implement post-voting actions
        pass

# Initial screen for joining the group
if st.session_state['user_id'] is None:
    st.markdown("<h1 style='text-align: center;'>PlanPal</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Enter Join Code and Name to join your Plan Pals!</h3>", unsafe_allow_html=True)

    group_code = st.text_input("Enter Group Code")
    username = st.text_input("Enter Username")

    if st.button("Submit"):
        if group_code and username:
            user_id = str(uuid.uuid4())

            st.session_state['groups'] = {group_code: UserBase(username=username, group_id=group_code, full_name=None, user_id=user_id)}
            save_user_data(group_code, user_id, username)

            st.session_state['user_id'] = user_id
            st.session_state['group_code'] = group_code
            st.session_state['username'] = username

            st.experimental_rerun()  # Use experimental_rerun due to st.rerun() issue
else:
    show_chat_interface()
