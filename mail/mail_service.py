import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to send an email
def send_email(recipient, subject, message, sender_user, sender_password):
    sender = "example@domain.com"  # Update to the actual sender email address

    try:
        # Configure the SMTP server
        server = smtplib.SMTP("smtp.server.com", 587)  # Update with actual SMTP server and port
        server.starttls()
        server.login(sender_user, sender_password)

        # Set up the email message
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        # Send the email
        server.send_message(msg)
        server.quit()
        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# Function to extract email data from the payload
def extract_email_data(payload):
    name = payload["data"]["json"]["name"]["givenName"]
    last_name = payload["data"]["json"]["name"]["familyName"]
    full_name = payload["data"]["json"]["name"]["formatted"]
    email = payload["data"]["json"]["emails"][0]["value"]
    department = payload["data"]["json"]["urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"]["department"]

    return name, last_name, full_name, email, department

# Function to create a welcome message for new users
def create_welcome_message(first_name, last_name, full_name, email, department):
    access_link = "https://example.com"  # Update with actual access link
    message = (
        f"Hello {first_name} {last_name},\n\n"
        f"We are pleased to inform you that your account has been successfully created in our system!\n\n"
        f"Account details:\n"
        f"Full Name: {full_name}\n"
        f"Email: {email}\n"
        f"Department: {department}\n\n"
        f"You can access your account using the following link: {access_link}\n\n"
        f"Your login credentials are the same as those you use for the company network.\n\n"
        f"If you have any questions, feel free to reach out.\n\n"
        f"Welcome to the team!\n"
        f"Best regards,\n"
        f"Support Team"
    )
    return message