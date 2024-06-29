# frontend.py
import streamlit as st
import asyncio
import websockets
import json
import random

async def connect_to_server(uri, room_code):
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                message = await websocket.recv()
                st.session_state.messages.append(message)
            except websockets.exceptions.ConnectionClosed:
                break

def generate_room_code():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))

def main():
    st.title("Multiplayer Scribble Game")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'websocket' not in st.session_state:
        st.session_state.websocket = None

    # Session joining or creating
    room_code = st.text_input("Enter room code:")
    if st.button("Join/Create Room"):
        if room_code:
            st.success(f"Joined/created room: {room_code}")
            asyncio.run(connect_to_server(f"ws://localhost:8000/ws/{room_code}", room_code))
        else:
            st.error("Please enter a room code")

    # Game area (placeholder)
    st.subheader("Game Area")
    drawing = st.empty()

    # Chat area
    st.subheader("Chat")
    for message in st.session_state.messages:
        st.write(message)

    # Send message
    message = st.text_input("Type a message")
    if st.button("Send"):
        if st.session_state.websocket:
            asyncio.run(st.session_state.websocket.send(message))

if __name__ == "__main__":
    main()
