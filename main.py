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
    github: str = Form(...),
):
    subject = f"Application for {position} – Pritesh Kumar Sahoo"
    greeting = (
        f"Hi {receiver_name}," if receiver_name.strip() else "Dear Hiring Manager,"
    )

    body = f"""
{greeting}

I am writing to express my strong interest in the {position} position at your organization.

As a Senior Software Engineer with over 3 years of hands-on experience, I specialize in building scalable, high-performance, and secure web applications using React.js, TypeScript, Golang, and PostgreSQL.

At I-Exceed, I built robust React-based payment and billing modules, introduced OTP authentication with Twilio and Firebase, and developed Golang-based SNMP Telegraf plugins to process device logs—improving monitoring and security compliance. My work consistently aligns with PCI-DSS and other enterprise-grade standards.

During my tenure at Infosys, I developed a full-stack Software Account Invitation Tool using React and Golang, successfully managing 1,000+ secure accounts and improving onboarding time by 35%.

In my personal projects, I’ve implemented a Role-Based Access Control (RBAC) system with full test coverage and integrated Swagger for API documentation. My animated Next.js portfolio and RBAC project are available on GitHub.

Please find my resume attached. I would be thrilled to contribute to your team and further elevate your digital platforms. Currenlty, I am serving notice period and my LWD is 20th September 2025.

Best regards,  
Pritesh Kumar Sahoo  
📞 +91 79780 17435  
📧 priteshkumarsahoo16@gmail.com  
🔗 LinkedIn: {linkedin}  
🔗 GitHub: {github}
"""

    # Construct the email message
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = email_id
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with open("CV_Pritesh_Kumar_Sahoo.pdf", "rb") as file:
            part = MIMEApplication(file.read(), Name="CV_Pritesh_Kumar_Sahoo.pdf")
            part["Content-Disposition"] = (
                'attachment; filename="CV_Pritesh_Kumar_Sahoo.pdf"'
            )
            message.attach(part)
    except FileNotFoundError:
        return templates.TemplateResponse(
            "form.html", {"request": request, "status": "❌ Resume file not found!"}
        )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(message)
        status = "✅ Email sent successfully!"
    except Exception as e:
        status = f"❌ Error sending email: {str(e)}"

    return templates.TemplateResponse(
        "form.html", {"request": request, "status": status}
    )
