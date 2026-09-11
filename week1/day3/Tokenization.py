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
    response = client.chat.completions.create(model=model, messages=messages,max_tokens=500);
    usage = response.usage;
    print("prompt usuage ---->", usage.prompt_tokens, "completion usage ---->", usage.completion_tokens, "total usage ---->", usage.total_tokens);
    finish_reason = response.choices[0].finish_reason
    print("finish_reason ---->", finish_reason)



# max_tokens tells the API: "generate at most N tokens for the completion, then stop — regardless 
# of whether you were 'done' thinking or not." It's a hard ceiling, not a target. The model might naturally 
# finish earlier (finish_reason: stop) or get cut off at your ceiling (finish_reason: length) 
# — but now you decided where that ceiling is, instead of an invisible default deciding for you.