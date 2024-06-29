# Description: This is the main file for the Golem app. It contains the main code for the app.
# The app will ask each individula what they want to do. Each user will input their name and what they want to do in the meeting.
# Each user after having a detaiked conversation with the LLM, the LLM will figure out 3 sets of activities that the group can do.
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the Octo API key from the environment variables
octo_api_key = os.getenv("OCTO_API_KEY")

# Use the Octo API key in your code
# (replace this with your actual code that uses the API key)
# if octo_api_key:
#     print("Octo API key:", octo_api_key)
# else:
#     print("Octo API key not found in environment variables.")

class GroupEvent:
    def __init__(self, eventid):
        self.eventid = eventid
    
    def __repr__(self):
        return f"GroupEvent({self.eventid})"

    #Create a method to create a new event
    def create_event(self, event_name, event_date, event_location):
        print(f"Creating event: {event_name} on {event_date} at {event_location}")

class User:
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"User({self.name})"

    #Create a method to get user input
    def get_input(self):
        activity = input(f"{self.name}, what would you like to do? ")
        print(f"{self.name} wants to {activity}")
        return activity




