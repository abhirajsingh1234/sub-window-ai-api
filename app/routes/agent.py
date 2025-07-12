from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from app.utils.mail_content_creator import send_email_tool
from app.utils.whatsapp_message_creator import send_whatsapp_message_tool
from langchain.tools import tool
from dotenv import load_dotenv
from pydantic import BaseModel
from flask import Blueprint, request, jsonify

load_dotenv()
import os

chat_bp = Blueprint('chat', __name__)
parser = JsonOutputParser()
google_api_key = os.getenv('GEMINI_API_KEY')
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=google_api_key)


class validator(BaseModel):
    expression: str
   

@tool(args_schema=validator)
def basic_calculator(expression: str) -> str:
    """Evaluate a basic math expression (e.g. 2 + 2, 5*6)"""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"


@tool(args_schema=validator)
def send_whatsapp_message(expression: str) ->str:
    """Send a WhatsApp message to a specified phone number or contact name."""
    try:
        result = send_whatsapp_message_tool(expression)
        return result
    except:
        return ' i was unable to send message please try again'
    
    
@tool(args_schema=validator)
def send_email(expression: str) ->str:
    """Send an email to a specified recipient."""
    result = send_email_tool(expression)

    return result
 


    
tools = [
    Tool.from_function(
        func=basic_calculator,
        name="Calculator",
        description="Use this tool when you need to perform mathematical calculations."
    ),
    Tool.from_function(
        func=send_whatsapp_message,
        name="whatsapp_message_sender",
        description="Send a WhatsApp message. Input should be a string with 'name or number' (recipient) and 'message' (the message to send)."
    ),
    Tool.from_function(
        func=send_email,
        name="email_sender",
        description="Send an email. Input should be a string containing a  dictionary  with the recipient's name or emailID, subject(auto generate if not provided by user) and email body."
    )
]

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,   #return messages as list instead of concatenated string
    output_key="output"     #only stores the final output key of response
)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory, 
    agent_kwargs={'system_message': """You are a users friend.
                        Use the appropriate tool when needed.
                        If no tool is applicable, generate a informative response directly.
                        You have access to past memory.
                        Use your memory to recall past conversations and provide relevant context.
                        if user asks any query try to provide good and informative responses in least counter question.
                        You are a messaging assistant responsible for sending user messages to specific recipients via WhatsApp. Follow these rules strictly for every query:

                        1. Extract the recipient's name from the input.
                        2. Identify the message intended for the recipient — this can be a statement, command, question, wish, or reminder.
                        3. Rephrase the message using correct grammar and natural language. Ensure the tone is clear, polite, and human-like.
                        4. Do not include the recipient’s name in the final message unless the user explicitly includes it as part of the message (e.g., “tell Abhiraj that…”).
                        5. Do not copy the structure or keywords like "send", "say", "message", "to", "query", etc., from the input. Focus only on the content of the intended message.
                        6. Your output must ONLY be the final message text to be sent — do not include sender or recipient labels, explanations, or any additional text.


                        output json format"""},   
    verbose=True,  
    handle_parsing_errors=True  
)

@chat_bp.route('/', methods = ['GET'])
def home():
    return jsonify({'message' : 'getting started with chat'})

@chat_bp.route('/', methods = ['POST'])
def chat():
    data = request.get_json(force = True)
    query = data.get('query')
    try:
        response = agent.invoke({"input": query})
        output = response['output']

    except Exception as e:
        print(f"Error: {e}")
        print("Let me try again with a simpler approach.")
        direct_response = llm.invoke(f"The user asked: {query}. Provide a helpful response.")
        output = direct_response.content

    memory.chat_memory.add_message(HumanMessage(content=query))
    memory.chat_memory.add_message(AIMessage(content=output))

    return jsonify({'agent' : output})