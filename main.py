from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

SENDER_EMAIL = os.getenv("GMAIL_USER")
SENDER_PASSWORD = os.getenv("GMAIL_PASS")

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/send-email")
async def send_email(
    request: Request,
    email_id: str = Form(...),
    receiver_name: str = Form(...),
    position: str = Form(...),
    linkedin: str = Form(...),
    github: str = Form(...)
):
    subject = f"Applying for {position}"
    greeting = f"Hi {receiver_name}," if receiver_name.strip() else "Dear Hiring Manager,"

    body = f"""
{greeting}

I am writing to express my interest in the {position} role. With over 3+ years of experience in frontend development using React.js, TypeScript, and Next.js, I specialize in building responsive, secure, scalable and high-performance web apps for enterprise and product-based applications.

At I-Exceed Technology, I developed pagination and payment modules for banking systems, optimized performance using React Hooks, and implemented OTP-based authentication integrated with services like Twilio and Firebase. My work resulted in faster transaction speeds and enhanced security, aligning with PCI-DSS standards.

Previously at Infosys, I built a Software Account Invitation Tool managing over 1,000 secure accounts. I applied TDD principles using Jest, implemented role-based access with JWT, and created dynamic dashboards with styled-components, which improved onboarding efficiency by 35%.

In addition to professional experience, I’ve developed personal projects including a Next.js-based animated portfolio and a full-stack job portal with AWS deployment and user authentication.

My current CTC is ₹7.11 LPA, and I am currently serving a 30-day notice period. I am enthusiastic about joining a forward-thinking team where I can contribute my frontend expertise and continue to grow.

Please find my resume attached. I look forward to the opportunity to discuss how I can contribute to your team.

Best regards,  
Pritesh Kumar Sahoo  
📞 +91 79780 17435  
📧 priteshkumarsahoo16@gmail.com  
🔗 LinkedIn: {linkedin}  
🔗 GitHub: {github}
"""

    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = email_id
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with open("CV_Pritesh_Kumar_Sahoo.pdf", "rb") as file:
            part = MIMEApplication(file.read(), Name="CV_Pritesh_Kumar_Sahoo.pdf")
            part['Content-Disposition'] = 'attachment; filename="CV_Pritesh_Kumar_Sahoo.pdf"'
            message.attach(part)
    except FileNotFoundError:
        return templates.TemplateResponse("form.html", {"request": request, "status": "Resume file not found!"})

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(message)
        status = "✅ Email sent successfully!"
    except Exception as e:
        status = f"Error sending email: {str(e)}"

    return templates.TemplateResponse("form.html", {"request": request, "status": status})
