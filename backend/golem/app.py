import os
from dotenv import load_dotenv
from langchain_community.llms.octoai_endpoint import OctoAIEndpoint
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

def llama_chat(question: str) -> str:
    """Chat with the llama."""
    client = OctoAI(api_key=octo_api_key,)

    context = retrieve_context()  # Retrieve the context from the context.txt file

    template = """You suggest things or places to be. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
    Question: {question} 
    Context: {context} 
    Answer:"""

    formatted_template = template.format(question=question, context=retriever)

    completion = client.text_gen.create_chat_completion(
        model="meta-llama-3-8b-instruct",
        messages=[
            ChatMessage(
                role="system",
                content=formatted_template,
            ),
        ],
        max_tokens=150,
    )

    print(json.dumps(completion.dict(), indent=2))

    return completion  # Return the completion as a string




