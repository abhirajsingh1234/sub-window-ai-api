from langgraph.graph import StateGraph,START,END

from dotenv import load_dotenv

from typing import TypedDict,List,Annotated,Literal

from langchain_openai import ChatOpenAI

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.prompts import PromptTemplate

from langgraph.graph.message import add_messages

from langchain.schema import AIMessage,HumanMessage

from langchain_core.tools import tool

from langgraph.prebuilt import ToolNode, tools_condition

from langgraph.checkpoint.memory import MemorySaver

import os

load_dotenv()

prompt = PromptTemplate(
    input_variables=['question'],

    template="""always give useful response

    query : {question}"""

)

memory = MemorySaver()

openai_key = os.getenv('GOOGLE_API_KEY')

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3, api_key=openai_key)

chain = prompt | llm

class dataobject(TypedDict):
    
    messages : Annotated[List,add_messages]

@tool
def get_stock_price(symbol: str) -> float:
    '''Return the current price of a stock given the stock symbol
    :param symbol: stock symbol
    :return: current price of the stock
    '''
    return {
        "MSFT": 200.3,
        "AAPL": 100.4,
        "AMZN": 150.0,
        "RIL": 87.6
    }.get(symbol, 0.0)

@tool
def send_whatsapp_messages(name : str, message : str)-> str:
    '''sends whatsapp message to given name
    : param 1) name : name of user
            2) message : message to be sent
    :return : status of message
    '''
    print(f"'{message}' sent to {name} ")
    return 'message was sent to given name'

@tool
def database_insertion(data : str)->str:
    '''inserts given data into database
    : param data:amount to be inserted
    :return : status(if data is inserted or not inserted)'''

    print(f'amount {data}')

    return 'data inserted successfully'

tools = [get_stock_price,send_whatsapp_messages,database_insertion]

llm_with_tools = llm.bind_tools(tools)


def chat_model(state : dataobject) -> dataobject:

        return {"messages": [llm_with_tools.invoke(state["messages"])]}
builder = StateGraph(dataobject)

builder.add_node('llm',chat_model)

builder.add_node('tools', ToolNode(tools))

builder.add_edge(START, 'llm')

builder.add_conditional_edges('llm',tools_condition)

builder.add_edge('tools','llm')

builder.add_edge('llm', END)

graph = builder.compile(checkpointer=memory)

config1 = { 'configurable': { 'thread_id': '1'} }

message = dataobject = {'messages': [{'role':'user',"content":"SEND a message to karan and say hyy"}]}

data= graph.invoke(message, config=config1)

print(data['messages'][-1].content)