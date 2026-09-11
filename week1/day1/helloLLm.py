import os
from dotenv import load_dotenv
from groq import Groq
#   Now, importing the dotenv file
load_dotenv()
#    Now,get the API key from the environment variable
my_API_KEY = os.getenv("GROQ_API_KEY")
# We should trhow error if there has no API-KEY
if not my_API_KEY:
    raise ValueError("wtf is your API-KEY DUDE??");

# this is The actual groq "connection"
client = Groq(api_key=my_API_KEY)
print("Connected successfully! Key loaded:", my_API_KEY[:10] + "...")
model="llama-3.3-70b-versatile"
role="user"
prompt="what is oauth and jwt diffirence?when to use "
# making a messsage dictionary
message = {
    "role": role,
    "content": prompt   # <-- fixed
}
# we want list of messages 
messages=[message]
# now defining the response -- so connection - building through client !!
response = client.chat.completions.create(model=model, messages=messages)
print(response.choices[0].message.content);