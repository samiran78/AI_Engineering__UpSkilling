import os;
from dotenv import load_dotenv;
from groq import Groq;
load_dotenv();
my_API_KEY = os.getenv("GROQ_API_KEY");
if not my_API_KEY:
    raise ValueError("wtf is your API-KEY DUDE??");
client = Groq(api_key=my_API_KEY);
print("Connected successfully! Key loaded:", my_API_KEY[:10] + "...");
# our model
model = "openai/gpt-oss-120b";
# now let's give the user a prompt to enter the temperature in celsius ->sarcastic Java backend senior who roasts bad code
system_message ={
    "role": "system",
    "content": "You are a student who failed 12th grade. You misunderstand technical terms, use very simple broken English, and give confidently wrong advice."
}
user_message ={
    "role": "user",
    "content": "Hey, for see building a payment infracture for a backend system.i need to write in a interface ..then call webhook to get verifiy siganture from rajorpay then @transactional to make things strictly follow ACID!?"
}
# storing all responses ina list to maintain the history of the conversation - messages
messages = [system_message, user_message];  
# real-life what happnes-claude say-hi smairan then i said prompt..role.. now 1step++->use temparature to get its crativity and randomness in the response.
#  The higher the temperature, the more creative and random the response will be. The lower the temperature, the more focused and deterministic the response will be.
response = client.chat.completions.create(model=model, 
messages=messages, temperature=1.8);
# i keep tempearture 2 to get strictly creative thinking and randomness in the response.
print(response.choices[0].message.content);