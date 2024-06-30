import streamlit as st
import pydantic
from datetime import datetime
from typing import List, Optional
import json
import os
import time
import random

# Define the schema classes
class UserBase(pydantic.BaseModel):
    username: str
    group_id: str
    full_name: Optional[str] = None
    user_id: Optional[int] = None

class MessageBase(pydantic.BaseModel):
    message_id: int
    role: str  # 'user' or 'assistant'
    content: str
    sender_username: str
    date: datetime

class EventBase(pydantic.BaseModel):
    event_id: int
    name: str
    description: str
    votes_up: int = 0
    votes_down: int = 0

class ChatBase(pydantic.BaseModel):
    chat_id: int
    group_id: str
    min_responses: Optional[int] = 4
    users: List[UserBase]
    messages: List[MessageBase] = []
    events: List[EventBase] = []

# File paths
USERS_FILE = 'users.json'
CHATS_FILE = 'chats.json'

# Function to load data from JSON files
def load_data():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            users_data = json.load(f)
            users = [UserBase(**user) for user in users_data]
    else:
        users = []

    if os.path.exists(CHATS_FILE):
        with open(CHATS_FILE, 'r') as f:
            chats_data = json.load(f)
            chats = [ChatBase(**chat) for chat in chats_data]
    else:
        chats = []

    return users, chats

# Function to save data to JSON files
def save_data(users, chats):
    with open(USERS_FILE, 'w') as f:
        json.dump([user.dict() for user in users], f, default=str)
    
    with open(CHATS_FILE, 'w') as f:
        json.dump([chat.dict() for chat in chats], f, default=str)

# Function to generate a unique response for each user
def generate_response(username, message):
    responses = [
        f"Hey {username}, that's an interesting point about '{message}'!",
        f"I see what you mean, {username}. Tell me more about '{message}'.",
        f"{username}, your message '{message}' got me thinking...",
        f"Hmm, '{message}' is quite intriguing, {username}. What else do you think?",
        f"You know, {username}, I've never thought about '{message}' that way before."
    ]
    return random.choice(responses)

# Function to generate event suggestions
def generate_events(chat_messages):
    # This is a simple implementation. In a real-world scenario, you might use NLP to extract event ideas from the chat.
    events = [
        EventBase(event_id=1, name="Movie Night", description="Watch a movie together virtually"),
        EventBase(event_id=2, name="Online Game Tournament", description="Compete in an online game tournament"),
        EventBase(event_id=3, name="Virtual Book Club", description="Discuss a book together online"),
        EventBase(event_id=4, name="Group Workout Session", description="Exercise together via video call"),
        EventBase(event_id=5, name="Cooking Challenge", description="Cook the same recipe and compare results")
    ]
    return events

# Main app
def main():
    st.markdown("<h1 style='text-align: center;'>PlanPal</h1>", unsafe_allow_html=True)
    

    # Load shared data
    users, chats = load_data()

    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'chat_finished' not in st.session_state:
        st.session_state.chat_finished = False

    if not st.session_state.current_user:
        # Step 1: Ask for Group name and User Name
        st.markdown("<h3 style='text-align: center;'>Enter Join Code and Name to join your Plan Pals!</h3>", unsafe_allow_html=True)
        st.header("Join a Group")
        group_id = st.text_input("Enter Group ID")
        username = st.text_input("Enter Your Username")
        
        if st.button("Join"):
            if group_id and username:
                # Check if the group exists
                existing_chat = next((chat for chat in chats if chat.group_id == group_id), None)
                
                if existing_chat:
                    # Check if username is already taken in this group
                    if any(user.username == username for user in existing_chat.users):
                        st.error("Username already taken in this group. Please choose a different username.")
                        return

                user_id = len(users) + 1
                new_user = UserBase(username=username, group_id=group_id, user_id=user_id)
                users.append(new_user)
                st.session_state.current_user = new_user
                
                if existing_chat:
                    existing_chat.users.append(new_user)
                else:
                    # Create a new chat for this group
                    new_chat = ChatBase(chat_id=len(chats)+1, group_id=group_id, users=[new_user], messages=[])
                    chats.append(new_chat)
                
                save_data(users, chats)
                st.experimental_rerun()
            else:
                st.error("Please enter both Group ID and Username")
    elif not st.session_state.chat_finished:
        # Find the current chat
        current_chat = next(chat for chat in chats if chat.group_id == st.session_state.current_user.group_id)
        
        # Step 2 & 3: Chatbot interface
        st.header(f"Group: {current_chat.group_id}")
        
        # Display users on the left
        st.sidebar.header("Users in this group")
        for user in current_chat.users:
            st.sidebar.text(user.username)
        
        # Display chat messages from history
        for message in current_chat.messages:
            with st.chat_message(message.role):
                st.markdown(f"**{message.sender_username}**: {message.content}")

        # React to user input
        if prompt := st.chat_input("What is up?"):
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(f"**{st.session_state.current_user.username}**: {prompt}")

            # Add user message to chat history
            message_id = len(current_chat.messages) + 1
            new_msg = MessageBase(
                message_id=message_id,
                role="user",
                content=prompt,
                sender_username=st.session_state.current_user.username,
                date=datetime.now()
            )
            current_chat.messages.append(new_msg)

            # Generate unique response
            response = generate_response(st.session_state.current_user.username, prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(f"**AI Assistant**: {response}")

            # Add assistant response to chat history
            message_id = len(current_chat.messages) + 1
            new_msg = MessageBase(
                message_id=message_id,
                role="assistant",
                content=response,
                sender_username="AI Assistant",
                date=datetime.now()
            )
            current_chat.messages.append(new_msg)

            # Save updated chat data
            save_data(users, chats)

        if st.button("Finish Chat"):
            st.session_state.chat_finished = True
            current_chat.events = generate_events(current_chat.messages)
            save_data(users, chats)
            st.experimental_rerun()

    else:
        # Voting page
        current_chat = next(chat for chat in chats if chat.group_id == st.session_state.current_user.group_id)
        st.header("Vote for Your Favorite Event")

        for event in current_chat.events:
            st.subheader(event.name)
            st.write(event.description)
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"👍 ({event.votes_up})", key=f"up_{event.event_id}"):
                    event.votes_up += 1
            with col2:
                if st.button(f"👎 ({event.votes_down})", key=f"down_{event.event_id}"):
                    event.votes_down += 1

        # Find the event with the most upvotes
        if current_chat.events:
            top_event = max(current_chat.events, key=lambda e: e.votes_up)
            st.header("Top Event")
            st.subheader(top_event.name)
            st.write(top_event.description)
            st.write(f"Upvotes: {top_event.votes_up}")
            st.write(f"Downvotes: {top_event.votes_down}")

        save_data(users, chats)

if __name__ == "__main__":
    main()