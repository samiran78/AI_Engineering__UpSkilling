import os;
from dotenv import load_dotenv;
from groq import Groq;
# importing pydantic for data validation and settings management -- DTO {IN SPRINGBOOT)}
from pydantic import BaseModel;
#Think it as ENUM ~~~ LITERAL
from typing import Literal, Optional
load_dotenv();
my_API_KEY = os.getenv("GROQ_API_KEY");
if not my_API_KEY:
    raise ValueError("wtf is your API-KEY DUDE??"); 
client=Groq(api_key=my_API_KEY);
print("Connected successfully! Key loaded:", my_API_KEY[:10] + "...");
# our model
model = "openai/gpt-oss-120b";
# Starting prompting

class SupportTicket(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None          # only capture if mentioned
    order_id: Optional[str] = None                 # customer was unsure — must be Optional
    order_id_uncertain: bool                        # flags that even if present, it's not confirmed
    product: str
    amount_paid: Optional[float] = None
    payment_status_conflict: bool                   # True because Razorpay says success, site says pending
    size_discrepancy: Optional[str] = None          # e.g. "ordered 12x18, confirmation shows 12x16"
    new_delivery_address: Optional[str] = None
    deadline: Optional[str] = None                  # "26th" — keep as string, don't assume date format
    wants_refund_if_missed_deadline: bool
    presales_question: Optional[str] = None         # the unrelated metal-print question
    issue_type: Literal["payment_issue", "size_mismatch", "address_change", "delivery_delay", "product_question", "multiple"]
    urgency: Literal["low", "medium", "high"]

inputForLLM = '''hi
so i ordered the WOODEn photo frames on the 3rd (or 4th? my wife did it from her phone) — order number is something like PC2024-8871 or 8877, i can check. we paid 4,200 via razorpay and money got deducted, screenshot attached but it shows "pending" on your site still?? razorpay sms says success.
ALSO the size. we wanted 22x18 but the confirmation mail says 12x16. nobody called. i tried calling the number on your website 3 times, no answer. is this even a real company
and can you change delivery address, we shifted. new one is kestopur,tarulia lane 1 , kolkata 700102. my number 8701248590. use this one not the one on the order.
btw does the metal print thing work for a wedding gift, need it by 26th. if not just cancel everything and refund, i dont have time for this.
— Rajat  my emaiallid -> sroy21197@gmail.com
Sent from my iPhone''';
 # # STEP 1 — BEFORE calling the API — describe the shape i want  
supportTicketDTO = SupportTicket.model_json_schema();
# this goes INTO AS  prompt, so the LLM knows what shape to return
#CALLING THE LLM TO GENERATE && UNDERSTOOD THE SUPPORT TICKET
systemPromptForDTO = f"""You are a support ticket parser. You will receive a customer message as input.
Extract the relevant information and return it in JSON format matching this exact schema:
{supportTicketDTO}
Return ONLY valid JSON. No explanation, no markdown."""
response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "user", "content": inputForLLM},
        {"role": "system", "content": systemPromptForDTO}],
    max_tokens=15500,
    temperature=1
);

#now, we want the response to be in JSON format, so we can parse it into our Pydantic model
response_content_BY_LLM = response.choices[0].message.content;
# Validation ---> after calling the API have to see what's in the response and validate it against the schema we defined
try:
    parsed_ticket = SupportTicket.model_validate_json(response_content_BY_LLM);
except Exception as e:
    print("Error occurred while validating JSON:", e)

print("Response from LLM:", response_content_BY_LLM);
print("Finish reason:", response.choices[0].finish_reason)
print("Repr of content:", repr(response.choices[0].message.content))
print("Full usage:", response.usage)