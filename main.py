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

As a Senior Software Engineer with 3.5 years of experience, I specialize in developing scalable, high-performance, and secure applications using React.js, TypeScript, Golang, Java, Spring Boot, and PostgreSQL. My expertise spans frontend architecture, backend services, and database management, enabling me to deliver end-to-end solutions.

At I-Exceed Technology & Solution, I enhanced banking applications by optimizing React.js payment modules with pagination, lazy loading, and reusable UI components, reducing load times by 30%. I also built bill payment functionalities, integrated OTP authentication with Twilio and Firebase, and implemented JWT-based authentication with RBAC for improved security compliance. Additionally, I contributed to backend enhancements by fixing critical bugs and integrating APIs with Spring Boot.

Previously, at Infosys, I developed a full-stack Software Account Invitation Tool using React.js and TypeScript, which streamlined the management of 1,000+ secure accounts and reduced onboarding time by 35%. I also engineered custom SNMP Telegraf plugins in Golang to capture and process device logs, significantly improving monitoring accuracy.

Beyond professional work, I’ve built a Role-Based Access Control (RBAC) project with comprehensive unit and integration testing and integrated Swagger UI for seamless API documentation. I also maintain a Next.js portfolio showcasing responsive design and modern frontend practices.

I am currently serving my notice period, with my last working day on 30th September 2025. I am eager to bring my expertise in full-stack development and secure application design to your team and contribute to building innovative, high-quality digital solutions.

Please find my resume attached for your consideration. I look forward to the opportunity to discuss how my skills can add value to your organization.

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
