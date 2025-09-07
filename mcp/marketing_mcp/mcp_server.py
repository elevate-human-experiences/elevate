import asyncio
import os  # noqa: INP001
import smtplib

from blog_tool import BlogInput, BlogOutput, OnlyVideoToBlog
from demo_script_tool import DemoScriptInput, DemoScriptOutput, OnlyDemoScript
from dotenv import load_dotenv
from email_tool import EmailInput, OnlyEmail
from fastmcp import FastMCP
from slides_tool import OnlySlides, SlidesInput, SlidesOutput
from summary_tool import OnlySummary, SummaryInput, SummaryOutput


load_dotenv()
gmail_app_key = os.getenv("MAIL_KEY")

sender_email = os.getenv("SENDER_EMAIL")


# Create MCP server
mcp = FastMCP("marketing-assistant", version="2.0.0")

# Instantiate the OnlyEmail helper
email_helper = OnlyEmail()
blog_helper = OnlyVideoToBlog()
summary_helper = OnlySummary()
slides_helper = OnlySlides()
demo_script_helper = OnlyDemoScript()


@mcp.tool(name="generate_blog", description="Generate a plain blog string only (no structured fields).")  # type: ignore[misc]
def generate_blog(input_data: BlogInput) -> BlogOutput:
    """
    Generate a plain text blog string from the given input without
    structured fields or metadata. Returns a raw blog message.
    """
    return blog_helper.create_blog_post(input_data)


@mcp.tool(name="generate_summary", description="Generate a plain summary string only (no structured fields).")  # type: ignore[misc]
def generate_summary(input_data: SummaryInput) -> SummaryOutput:
    """
    Generate a plain text summary string from the given input without
    structured fields or metadata. Returns a raw summary message.
    """
    return summary_helper.summarize_and_convert_to_markdown(input_data)


@mcp.tool(name="generate_slides", description="Generate slides content string only (no structured fields).")  # type: ignore[misc]
def generate_slides(input_data: SlidesInput) -> SlidesOutput:
    """
    Generate a plain slides string from the given input without
    structured fields or metadata. Returns a raw slides contents.
    """
    return slides_helper.generate_slides(input_data)


@mcp.tool(name="generate_demo_script", description="Generate a plain demo script only (no structured fields).")  # type: ignore[misc]
def generate_demo_script(input_data: DemoScriptInput) -> DemoScriptOutput:
    """
    Generate a plain demo script from the given input without
    structured fields or metadata. Returns a raw demo script.
    """
    return demo_script_helper.generate_demo_script(input_data)


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
