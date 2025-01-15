import pandas as pd
from twilio.rest import Client
import openai
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, OPEN_API_KEY

# Load your phone contacts from CSV
contacts_csv_file_path = 'contacts.csv' # Path to your contacts CSV file
contacts = pd.read_csv(contacts_csv_file_path)

# Load your domain knowledge and Q&A from CSV
knowledge_csv_file_path = 'domain_knowledge.csv' # Path to your domain knowledge CSV file
knowledge_data = pd.read_csv(knowledge_csv_file_path)

# Set OpenAI Key 
open.api_key = OPEN_API_KEY

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def generate_response(question):
 # Prepare the context with domain knowledge
 qa_pairs = ""
 for index, row in knowledge_data.iterrows():
    qa_pairs += f"Q: {row['question']}\nA: {row['answer']}\n\n"
 
 context = f"{qa_pairs} Q: {question}\nA:"
 
 # Call OpenAI's GPT-4 API with the context
 response = openai.ChatCompletion.create(
 model="gpt-4",
 messages=[
 {"role": "user", "content": context}
 ],
 max_tokens=150
 )
 return response['choices'][0]['message']['content'].strip()

def make_phone_call(phone_number, response_text):
 call = twilio_client.calls.create(
 to=phone_number,
 from_=TWILIO_PHONE_NUMBER,
 twiml=f'<Response><Say language="ro">{response_text}</Say></Response>'
 )
 print(f'Call initiated to {phone_number}. Call SID: {call.sid}')

# Iterate through contacts and make calls
for index, row in contacts.iterrows():
 phone_number = row['phone_number'] # Assuming your CSV has a 'phone_number' column
 question = "Introduceți întrebarea dvs. aici." # Customize this question as needed
 response_text = generate_response(question)
 make_phone_call(phone_number, response_text)