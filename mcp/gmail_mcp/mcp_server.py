import asyncio
import os  # noqa: INP001
import smtplib

from dotenv import load_dotenv
from email_schema import EmailInput, OnlyEmail
from fastmcp import FastMCP


load_dotenv()
gmail_app_key = os.getenv("MAIL_KEY")

sender_email = os.getenv("SENDER_EMAIL")


# Create MCP server
mcp = FastMCP("email-assistant", version="2.0.0")

# Instantiate the OnlyEmail helper
email_helper = OnlyEmail()


@mcp.tool(name="generate_email", description="Generate a plain email string only (no structured fields).")  # type: ignore[misc]
def generate_email(input_data: EmailInput) -> str:
    """
    Generate a plain text email string from the given input without
    structured fields or metadata. Returns a raw email message.
    """
    return str(email_helper.generate_email(input_data))


# Send an email via SMTP (requires environment variables)
@mcp.tool(name="send_mail", description="Send an email to a recipient via Gmail SMTP.")  # type: ignore[misc]
def send_mail(receiver_email: str, subject: str, body: str) -> str:
    """
    Sends an email to the specified recipient using Gmail SMTP.

    Args:
        receiver_email (str): The email address of the recipient.
        subject (str): The subject line of the email.
        body (str): The content of the email body.

    Returns:
        str: Confirmation message.
    """
    text = f"Subject: {subject}\n\n{body}"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(str(sender_email), str(gmail_app_key))
        server.sendmail(str(sender_email), receiver_email, text)
        server.quit()

        return f"✅ Mail has been sent to {receiver_email}"  # noqa: TRY300

    except smtplib.SMTPException as e:
        raise smtplib.SMTPException(f"SMTP error: {e}")  # noqa: B904
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")  # noqa: B904, TRY002


# Run MCP server when executed
if __name__ == "__main__":
    asyncio.run(mcp.run())
