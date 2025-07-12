from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os
import re
from app.utils.whatsapp_tool import send_whatsapp_messages
from app.utils.fetch_data import contact_data


load_dotenv()

def send_whatsapp_message_tool(query):
    available_numbers = contact_data()

    parser = JsonOutputParser()

    chat_history=[]
    model = ChatGoogleGenerativeAI(model='gemini-1.5-flash', api_key=os.getenv('GOOGLE_API_KEY'),temperature=0,max_output_tokens=500)
    template = PromptTemplate(
        input_variables=["question","available_numbers", "chat_history"],
        partial_variables = {"format" : parser.get_format_instructions()},
        template="""
                               Analyze the input {question} to determine if the user is requesting to send a WhatsApp message.

                                Guidelines:
                                1. First check if a phone number is explicitly provided in the query
                                2. If no phone number is found:
                                   - Extract any person/contact name mentioned in the query
                                   - Search the {available_numbers}  for matching names
                                   - Use the corresponding number if a name match is found

                                3. Extracting Message Content:
                                    - Identify the message content from the user query.
                                    - If message is missing, search the {chat_history} for relevant details.
                                    - The message must accurately resolve the user’s query.

                                4. If either phone_number (direct or via name lookup) or message is not found:
                                   - Set the missing parameter(s) to null

                                6. if no message is found, set message to '..'
                                4 Expected output JSON Output Format:
                                {{
                                    "phone_number": "recipient's number",
                                    "message": "message to send"
                                }}
                                5. Always return the output in the following format and no extra text:
                                {format}
                                """
    )

    print(query)
    chain = template | model | parser
    response=chain.invoke({
        "question": query,
        "available_numbers": available_numbers,
        "chat_history": chat_history
    })
    print("\nresponse:\n", response)
    # Fallback extraction
    if not response.get("phone_number"):
        match = re.search(r'\b\d{10}\b', query)
        if match:
            response["phone_number"] = match.group(0)
    try:
        response = send_whatsapp_messages(response['phone_number'], response['message'])
        print(response)
        if response:
            return f"whatsapp message was sent successfully!"
        else:
            return {"error": f"ERROR OCCURED WHILE SENDING WHATSAPP MESSAGE, TRY AGAIN"}
    except Exception as e:
        return {"error": f"ERROR OCCURED WHILE SENDING WHATSAPP MESSAGE, TRY AGAIN"}
    

if __name__ == '__main__':
    send_whatsapp_message_tool('send a message to 7021721482  and say pranam jesht bhrata')























