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
model = "openai/gpt-oss-120b"
# As it will be growing so empty array/list
messages = []  
while(True):
    # get input from the user using input(). Store it in a variable.
    # making it lowercase to maintain consistency
    userInput = input("Enter your thoughts: ").lower() ;
    # Check: if the user typed "exit" or "quit", break out of the loop.
    if "exit" in userInput or "break" in userInput:
        break;
    # Take that user input and append it to messages as a dict with role: "user" and content: <their input>.
    messages.append({"role": "user","content":userInput}) 
    # Call client.chat.completions.create(model=model, messages=messages) — same as before, but now messages has the growing history.
    response = client.chat.completions.create(model=model, messages=messages)
    print(response.choices[0].message.content)
    messages.append({"role": "assistant", "content": response.choices[0].message.content})

