import os
from dotenv import load_dotenv
from langchain_community.llms.octoai_endpoint import OctoAIEndpoint
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

octo_api_key = os.getenv("OCTO_API_KEY")

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
    with open(os.path.join(context_dir, 'context.txt'), 'r') as f:
        context = f.read()

    return context

def llama_chat(question: str) -> str:
    """Chat with the llama."""
    llm = OctoAIEndpoint(
        model="meta-llama-3-8b-instruct",
        max_tokens=1024,
        presence_penalty=0,
        temperature=0.1,
        top_p=0.9,
    )
    
    context = retrieve_context()  # Retrieve the context from the context.txt file
    
    template="""You are a tour guide. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
    Question: {question} 
    Context: {context} 
    Answer:"""
    prompt = ChatPromptTemplate.from_template(template)
    chain = (
        {"context": context, "question": question}  # Use the retrieved context and the provided question
        | prompt
        | llm
        | StrOutputParser()
    )
    
    response = chain.run()  # Run the chain and save the response
    return response  # Return the response as a string




