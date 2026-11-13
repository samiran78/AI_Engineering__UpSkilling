import os;
from dotenv import load_dotenv;
from groq import Groq;
from datetime import datetime;
# importing pydantic for data validation and settings management -- DTO {IN SPRINGBOOT)}
from pydantic import BaseModel,Field;
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
currDate = datetime.now();
# we neeed separate nested class for counting experience years
class Experience(BaseModel):
    company: str
    visited_on: str = Field(description="Month of visit in YYYY-MM format")
    left_on: Optional[str] = Field(default=None, description="YYYY-MM, or null if still there")
class Resume(BaseModel):
    name: str
    email: str
    phone: str 
    education: str
    experience: list[Experience]
    skills: list[str] = []
    projects: list[str] = []
    certifications: Optional[str] = None
#now ,passing my RESUME to the llm to see what it extracts and returns in JSON format
inputForLLM = '''
Samiran Roy Bhowmik
samiran.roy.tech@gmail.com — +91 8101387643 — GitHub — LinkedIn — GeeksforGeeks —
LeetCode
Education
• Techno International Batanagar
Bachelor of Technology in Computer Science and Engineering; CGPA: 8.63
• SVM (WBCHSE)
Higher Secondary (12th Grade); Percentage: 78%
Skills
Kolkata, West Bengal
Sept 2020– Aug 2024
West Bengal
2018– 2020
• Languages: Java 8, JavaScript, SQL
• Frameworks & Libraries: Spring Boot, Hibernate/JPA, React.js, Node.js, Express.js
• Databases: MySQL, MongoDB
• Technologies: REST APIs, WebSockets, JWT Authentication, Git, Docker (Learning)
• AI-Assisted Development: Claude, ChatGPT, Cursor, AI-first development workflows, codebase understanding,
debugging, concept clarification, LLD/HLD exploration, and implementation support
• Developer Tools: IntelliJ IDEA, VS Code, Postman, GitHub
• Concepts: MVC Architecture, OOP, Design Patterns, Data Structures & Algorithms
Experience
• Assurex
Software Engineer Intern
Remote
Jul 2026– Present– Enterprise Application Development: Contributing to enterprise web application development using Sitecore CMS
and React.js, working with existing codebases and implementing application enhancements.– Debugging & Collaboration: Troubleshooting application issues, understanding existing application workflows, and
collaborating with the engineering team on development and maintenance tasks.
• GlobalLogic
Associate Analyst, Content Engineering
Remote
Apr 2026– May 2026– Robotics AI Project: Contributed to robotics AI workflows for the Gemini Robotics initiative through structured
annotation, multimodal data review, and task instruction creation.– Data Quality & Evaluation: Performed frame-level validation, error tagging, and edge-case analysis to improve
training datasets for robotics perception and instruction-following systems.– Cross-Functional Collaboration: Worked with QA, Audit, and ML teams to ensure dataset consistency while
maintaining 96–98% accuracy benchmarks in SLA-driven production environments.
• Zediant Technologies
Backend Developer Intern (Java, Spring Boot)
Kolkata, West Bengal
Aug 2025– Mar 2026– Multi-Database Library: Developed a database connector library supporting MongoDB, MySQL, Oracle, and SQL
Server with unified CRUD operations, runtime database switching, batch processing, and transaction management.– IoT Backend Development: Built and maintained 15+ REST APIs for smartwatch device management including
SOS configuration, health monitoring, battery alerts, walk/sleep timers, and language settings using Spring Boot and
MySQL.– Real-Time Systems: Integrated WebSocket-based real-time device status updates and maintained TCP
communication workflows for smartwatch connectivity and event processing.– Architecture & Code Quality: Refactored 4,500+ lines of production code, redesigned API response architecture,
and implemented DTO validation, audit logging, pagination, and Spring Data JPA Specifications.– Production Debugging: Resolved 25+ production issues involving MongoDB Java 1.8 compatibility, WebSocket
event handling, TCP connection management, email services, and device communication workflows.
• Lissica Tech
Frontend Developer Teaching Intern
Kolkata, West Bengal
Jun 2023–Jun 2023
Training: Conducted sessions on HTML, CSS, JavaScript, and Bootstrap with emphasis on responsive web
development fundamentals.
Certifications
• Oracle Cloud Infrastructure 2025 — AI Foundations Associate: Issued by Oracle University · Valid until Oct 2027
Key Skills: AI/ML Fundamentals, LLM Basics, Generative AI, CNN/RNN/LSTM Concepts, OCI AI Services, Oracle
23ai, Select AI.
Verified Badge: Verification Link
Projects
• PrintCraft– Custom Print Commerce Platform
Live — GitHub
Spring Boot 3.5, Java 21, PostgreSQL, Redis, React/Vite, JWT, Razorpay, Flyway– Real-Client Production System: Built and deployed a full-stack e-commerce platform for a live print business,
implementing authentication, product management, shopping cart, order processing, payment, and delivery workflows.– Backend Engineering: Developed REST APIs with Spring Boot, implemented Flyway database migrations,
Redis-backed OTP rate limiting, JWT & Google OAuth authentication, dynamic multi-filter search using Spring Data
JPA Specifications, and Razorpay webhook signature verification.– Order & Delivery Architecture: Designed a delivery state machine with terminal-state guards, duplicate/stale
webhook detection, order event history, and automated email notifications for delivery status updates.– Cloud Deployment: Deployed the production application on AWS using EC2, RDS, S3 image storage, and Nginx
reverse proxy.
• Custom URL Shortener with Analytics
GitHub — Live Demo
Node.js, Express.js, MongoDB, EJS, JWT– Features: Production-ready URL shortener with click analytics tracking, JWT-based authentication, and role-based
access control (admin/user roles).– Backend: Built RESTful APIs using Express.js with MongoDB for URL storage, user management, and analytics.
Implemented secure password hashing with bcrypt and cookie-based session management.
• Real-time Device Tracking System
GitHub — Live Demo
Node.js, Express.js, Socket.IO, Leaflet.js– Real-time Communication: Implemented WebSocket-based location tracking using Socket.IO for bi-directional
communication between devices and server.– Map Integration: Integrated Leaflet.js for interactive map visualization with live marker updates. Implemented
throttled location updates for performance optimization.
• Expense Tracker Management System
GitHub
React.js, Node.js, Express.js, MongoDB, Ant Design– Full-Stack Development: Built secure expense tracking application with complete CRUD operations, category-based
filtering, and analytics dashboard.– Backend: Developed modular REST APIs with optimized MongoDB aggregation queries for expense analytics and
reporting.– Frontend: Created responsive UI using React.js and Ant Design with modals, tables, and progress charts for data
visualization.
Coding Practice
• Competitive Programming: Solved 230+ LeetCode problems using Java and completed the GFG 160 Days Challenge.
Regularly practice Data Structures and Algorithms.
Additional Information
• Availability: Immediate Joiner
'''

# function for substraction of years and months from two dates in YYYY-MM format
def  substract_years_months(start, end):
    start_year = int(start.split("-")[0])
    start_month = int(start.split("-")[1])
    end_year = int(end.split("-")[0])
    end_month = int(end.split("-")[1])
    startScore = start_year * 12 + start_month
    endScore = end_year * 12 + end_month
    total_months = endScore - startScore
    return total_months ;

#call the llm----------------------------
# STEP 1 — BEFORE calling the API — describe the shape i want  
resumeResponseDTO = Resume.model_json_schema();
response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": f"You are a resume parser. You will receive a resume as input. Extract the relevant information and return it in JSON format matching this exact schema: {resumeResponseDTO} Return ONLY valid JSON. No explanation, no markdown."},
        {"role": "user", "content": inputForLLM},],
    max_tokens=15500,
    # not need any creativity need pont to point generic answer ,so temprature needs to be in 0
    temperature=0 
)
# Here we are getting the response from the LLM and parsing it to JSON format----
response_parsing_resume = response.choices[0].message.content;
#check the result
# Validation ---> after calling the API have to see what's in the response and validate it against the schema we defined
try:
    parsed_resume_response  = Resume.model_validate_json(response_parsing_resume);
    # here,we have to loop over the response to iterate over the experience and calculate the total months of experience
    total_months_of_experience = 0;
    for exp in parsed_resume_response.experience:
        # FIX: Use strftime("%Y-%m") instead of to_string()
        end_date_str = exp.left_on if exp.left_on else currDate.strftime("%Y-%m")
        total_months_of_experience += substract_years_months(exp.visited_on, end_date_str);
        print("✅ Parsed ticket object:", parsed_resume_response)
except Exception as e:
    print("Error occurred while validating JSON:", e)

print("Response from LLM:", response_parsing_resume);
print("Full usage:", response.usage)
print("✅ Total months of experience:", total_months_of_experience)