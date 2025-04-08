"""Module to test the email generation functionalities of the OnlyEmail class."""

from elevate.only_email import OnlyEmail


def test_personal_email() -> None:
    """Tests the generation of a personal email.

    This function uses the OnlyEmail class to generate a personal email based on a
    given input message and then prints the generated email.
    """
    personal_email_input_message = """
    A birthday wishes for John Doe.
    """
    only_email = OnlyEmail(with_model="gemini/gemini-2.0-flash-lite")
    generated_email = only_email.generate_email(
        personal_email_input_message, "personal"
    )
    print(generated_email)


# test_personal_email()


def test_professional_email() -> None:
    """Tests the generation of a professional email.

    This function uses the OnlyEmail class to generate a professional email based on a
    given input message and then prints the generated email.
    """
    professional_email_input_message = """
    Email to boss regarding, asking a sick leave for 3 days.
    """
    only_email = OnlyEmail(with_model="gemini/gemini-2.0-flash-lite")
    generated_email = only_email.generate_email(
        professional_email_input_message, "professional"
    )
    print(generated_email)


# test_professional_email()


def test_marketing_email() -> None:
    """Tests the generation of a marketing email.

    This function uses the OnlyEmail class to generate a marketing email based on a
    given input message and then prints the generated email.
    """
    marketing_email_input_message = """
    Email for a python library which generates professional emails based on user input.

    Important input:
    1. Target Audience: University Students.
    2. Product/Service: Emailer, a Python library which can generate emails of different kinds based on user input. Deelopers can try out different llms while generating emails to see which suits best. This functionality of the library should be called BYOL(Bring Your Own LLM).
    3. Primary Goal: Let developers know about this library.
    4. Key Selling Points:
                        a. Generate email drafts in blink on an eye.
                        b. Bring Your Own LLM.
                        c. Completely open source.
    5. Call to Action: Click here to know more.
    6. Content Length: 400 words.
    7. Desired Tone: A light and energetic tone.
    """
    only_email = OnlyEmail(with_model="gemini/gemini-2.0-flash-lite")
    generated_email = only_email.generate_email(
        marketing_email_input_message, "marketing"
    )
    print(generated_email)


test_marketing_email()
