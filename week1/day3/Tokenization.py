import os;
from dotenv import load_dotenv;
from groq import Groq;
load_dotenv();
my_API_KEY = os.getenv("GROQ_API_KEY");
if not my_API_KEY:
    raise ValueError("wtf is your API-KEY DUDE??"); 
client=Groq(api_key=my_API_KEY);
print("Connected successfully! Key loaded:", my_API_KEY[:10] + "...");
# our model
model = "openai/gpt-oss-120b";
# Starting prompting
role="user"
prompt1="hii"
prompt2="Explain the future scope career of backend engineering in 2027 to future,AI-ENgineer,AI/ML,SDE"
prompt3="write in 100 words should AI-AGENT STARTED TO MAKE FOR SDEBACKEND STRONG OR DSA TREE NEEDED??"

# MAKING LIST OF PROMPTS TO SEND TO THE MODEL
prompts=[prompt1,prompt2,prompt3];
for p in prompts:
    print(f"Sending prompt: {p}")
    message={
        "role": role,
        "content": p
    }
    messages=[message];
    response = client.chat.completions.create(model=model, messages=messages);
    usage = response.usage;
    print("prompt usuage ---->", usage.prompt_tokens, "completion usage ---->", usage.completion_tokens, "total usage ---->", usage.total_tokens);
    finish_reason = response.choices[0].finish_reason
    print("finish_reason ---->", finish_reason)
