import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from octoai.text_gen import ChatMessage
import json

from octoai.client import OctoAI



load_dotenv()

octo_api_key = os.getenv("OCTOAI_API_TOKEN")

if not octo_api_key:
    raise ValueError("Octo API key not found in environment variables.")

class GroupEvent:
    def __init__(self, eventid: str):
        """Initialize a new GroupEvent."""
        self.eventid = eventid
    
    def __repr__(self) -> str:
        return f"GroupEvent({self.eventid})"

    def create_event(self, event_name: str, event_date: str, event_location: str) -> None:
        """Create a new event."""
        print(f"Creating event: {event_name} on {event_date} at {event_location}")

class User:
    def __init__(self, name: str):
        """Initialize a new User."""
        self.name = name
    
    def __repr__(self) -> str:
        return f"User({self.name})"

    def get_input(self) -> str:
        """Get user input."""
        activity = input(f"{self.name}, what would you like to do? ")
        print(f"{self.name} wants to {activity}")
        return activity

def retrieve_context():
    """
    Retrieve the context from the context.txt file.
    """
    context_dir = os.path.join(os.path.dirname(__file__))
    with open('/Users/rishi/dev/GolemAI-1/backend/context.txt', 'r') as f:
        context = f.read()

    return context

def llama_chat(question: str, chat_id) -> str:
    """Chat with the llama."""
    client = OctoAI(api_key=octo_api_key)

    print("Currenting chatting with chat_id: ", chat_id)

    # retriever = retrieve_context()  # Retrieve the context from the context.txt file
    # print(retriever)

    # template = """You suggest things or places to be. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use sentences maximum and keep the answer concise. The context is a collection of chat messages from a individual set of users in a group. The context contains the entire conversation history, but the response will only got to a single user. The response should nudge and finally make the user to figure out where to go as a group.
    # Question: {question} 
    # Answer:"""

    template = """This is a message from user {chat_id}, ask more questions to figure out where the user wants to go. and finally find out a ideally place the user wants to go as part of the group.
    Question: {question} 
    Answer:"""

    formatted_template = template.format(question=question, chat_id=chat_id)

    completion = client.text_gen.create_chat_completion(
        model="meta-llama-3-8b-instruct",
        messages=[
            ChatMessage(
                role="system",
                content=formatted_template,
            ),
        ],
        max_tokens=1000,
    )

    response_content = completion.choices[0].message.content  # Extract the content from the response

    # Write the response to a file
    with open('responses.txt', 'a') as f:
        f.write(response_content + '\n')

    print(response_content)

    return response_content


def llama_decide() -> list:
    """Decide on 1-3 places for the group based on the chat history."""
    
    # Read the responses from the file
    with open('responses.txt', 'r') as f:
        responses = f.read().split('\n')

    client = OctoAI(api_key=octo_api_key)

    # retriever = retrieve_context()  # Retrieve the context from the context.txt file
    # print(retriever)

    # template = """You suggest things or places to be. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use sentences maximum and keep the answer concise. The context is a collection of chat messages from a individual set of users in a group. The context contains the entire conversation history, but the response will only got to a single user. The response should nudge and finally make the user to figure out where to go as a group.
    # Question: {question} 
    # Answer:"""

    template = """find out a ideally place the user wants to go as part of the group.Be ver opiniatned and list places only. Do not be two over rounded.
    Question: {question} 
    Answer:"""

    formatted_template = template.format(question=responses)

    completion = client.text_gen.create_chat_completion(
        model="meta-llama-3-8b-instruct",
        messages=[
            ChatMessage(
                role="system",
                content=formatted_template,
            ),
        ],
        max_tokens=1000,
    )

    response_content = completion.choices[0].message.content  # Extract the content from the response

    # Write the response to a file
    with open('responses.txt', 'a') as f:
        f.write(response_content + '\n')

    print(response_content)

    return response_content


