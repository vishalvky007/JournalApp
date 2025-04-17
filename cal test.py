import os
import streamlit as st
import pickle
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import BaseTool
from langchain.agents import AgentExecutor, create_openai_tools_agent

# Google Calendar API tools
from langchain_community.tools.gmail import GmailCreateDraft
# from langchain_community.tools.google_calendar import GoogleCalendarCreateTool, GoogleCalendarGetEvents
from langchain_google_community.calendar import GoogleCalendarCreateTool, GoogleCalendarGetEvents
# from langchain_google_community.calendar import cr
# Google API authentication
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Define the scopes for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/gmail.compose']

def authenticate_google_calendar():
    """Authenticate with Google Calendar API."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no valid credentials, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # For Streamlit, we'll need to handle the authentication flow differently
            # Display instructions for the user
            st.info("You need to authenticate with Google Calendar.")
            
            # Create a button to trigger the authentication flow
            if st.button("Authenticate with Google"):
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
                
                st.success("Authentication successful!")
                st.rerun()
    
    return creds

# Initialize Google Calendar Tools
def init_calendar_tools():
    creds = authenticate_google_calendar()
    
    if creds:
        get_events_tool = GoogleCalendarGetEvents(credentials=creds)
        create_event_tool = GoogleCalendarCreateTool(credentials=creds)
        email_tool = GmailCreateDraft(credentials=creds)
        
        return [get_events_tool, create_event_tool, email_tool]
    else:
        return []

# Create our language model
def get_llm():
    # You can replace this with your preferred model
    return ChatGoogleGenerativeAI(model="gemini-1.5-pro")

# Create agent prompt
agent_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful calendar assistant that can schedule meetings and check calendar availability.
    
    When scheduling meetings:
    1. Check if there are any conflicts first
    2. Format times appropriately (ISO format for API calls)
    3. Provide confirmation after scheduling
    4. Be specific about the date, time and duration in your responses
    
    Use the provided tools to interact with the calendar.
    """),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Build the calendar agent
def build_calendar_agent():
    tools = init_calendar_tools()
    if not tools:
        return None
        
    llm = get_llm()
    agent = create_openai_tools_agent(llm, tools, agent_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor

# Streamlit app
def main():
    st.set_page_config(page_title="Calendar Assistant", page_icon="📅", layout="wide")
    
    st.title("📅 Calendar Assistant")
    st.markdown("""
    This assistant can help you manage your Google Calendar:
    - Check your schedule for today or any date
    - Schedule new meetings
    - Find available time slots
    """)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Check if authenticated
    creds = authenticate_google_calendar()
    if not creds:
        st.warning("Please authenticate with Google Calendar to use this app")
    else:
        st.success("Connected to Google Calendar")
    
    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Accept user input
    if user_input := st.chat_input("What would you like to do with your calendar?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "human", "content": user_input})
        
        # Display user message in chat message container
        with st.chat_message("human"):
            st.markdown(user_input)
        
        # Process with calendar agent
        if creds:  # Only if authenticated
            # Build or get the agent
            agent_executor = build_calendar_agent()
            
            if agent_executor:
                with st.spinner("Thinking..."):
                    # Format chat history for the agent
                    chat_history = []
                    for msg in st.session_state.chat_history:
                        if msg["role"] == "human":
                            chat_history.append(HumanMessage(content=msg["content"]))
                        elif msg["role"] == "assistant":
                            chat_history.append(AIMessage(content=msg["content"]))
                    
                    # Invoke the agent
                    response = agent_executor.invoke({
                        "input": user_input,
                        "chat_history": chat_history
                    })
                    
                    # Extract the response
                    assistant_response = response["output"]
                    
                    # Update chat histories
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    st.session_state.chat_history.append({"role": "human", "content": user_input})
                    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
                    
                    # Display assistant response
                    with st.chat_message("assistant"):
                        st.markdown(assistant_response)
            else:
                with st.chat_message("assistant"):
                    response = "I'm having trouble initializing the calendar tools. Please check your authentication."
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            # If not authenticated, display a message
            with st.chat_message("assistant"):
                response = "Please authenticate with Google Calendar first before I can help you manage your calendar."
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()