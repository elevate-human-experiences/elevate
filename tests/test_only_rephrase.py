"""Module to test the text rephrasing functionalities of the OnlyRephrase class."""

from elevate.only_rephrase import OnlyRephrase


def test_rephase_text_formal() -> None:
    """
    Test the rephrase_text method with a formal style.

    Uses a formal message to request sick leave with a lengthy output.
    """
    input_message = """
    I need 2 days of sick leave.
    """
    only_rephrase = OnlyRephrase()
    # Note: Using "formal" (instead of "fomral") for clarity.
    rephrased_text = only_rephrase.rephrase_text(input_message, "formal", "lengthy")
    print("Formal Rephrase:\n", rephrased_text)


def test_rephase_text_informal() -> None:
    """
    Test the rephrase_text method with an informal style.

    Uses the same message for sick leave but expects a shorter, more casual rephrasing.
    """
    input_message = """
    I need 2 days of sick leave.
    """
    only_rephrase = OnlyRephrase()
    rephrased_text = only_rephrase.rephrase_text(input_message, "informal", "short")
    print("Informal Rephrase:\n", rephrased_text)


def test_rephase_text_urgent() -> None:
    """
    Test the rephrase_text method with an urgent style.

    Uses a message describing a serious problem that requires immediate attention and returns a lengthy output.
    """
    input_message = """
    This is a serious problem that needs to be addressed immediately.
    """
    only_rephrase = OnlyRephrase()
    rephrased_text = only_rephrase.rephrase_text(input_message, "urgent", "lengthy")
    print("Urgent Rephrase:\n", rephrased_text)


def test_rephase_text_enthusiastic() -> None:
    """
    Test the rephrase_text method with an enthusiastic style.

    Rephrases a positive and energetic message with a medium length output.
    """
    input_message = """
    I'm so excited about this project!
    """
    only_rephrase = OnlyRephrase()
    rephrased_text = only_rephrase.rephrase_text(
        input_message, "enthusiastic", "medium"
    )
    print("Enthusiastic Rephrase:\n", rephrased_text)


def test_rephase_text_informative() -> None:
    """
    Test the rephrase_text method with an informative style.

    Uses a technical description to generate a detailed, informative rephrasing.
    """
    input_message = """
    The system utilizes a multi-threaded architecture to improve performance.
    """
    only_rephrase = OnlyRephrase()
    rephrased_text = only_rephrase.rephrase_text(
        input_message, "informative", "lengthy"
    )
    print("Informative Rephrase:\n", rephrased_text)


def test_rephase_text_friendly() -> None:
    """
    Test the rephrase_text method with a friendly style.

    Rephrases a casual invitation message in a warm, approachable manner with a short output.
    """
    input_message = """
    Hey, let's catch up over coffee sometime soon.
    """
    only_rephrase = OnlyRephrase()
    rephrased_text = only_rephrase.rephrase_text(input_message, "friendly", "short")
    print("Friendly Rephrase:\n", rephrased_text)


def test_rephase_text_technical() -> None:
    """
    Test the rephrase_text method with a technical style.

    Rephrases a technical explanation regarding system architecture with a detailed output.
    """
    input_message = """
    Our application leverages containerization and orchestration to optimize deployment pipelines.
    """
    only_rephrase = OnlyRephrase()
    # Here, "technical" style is used with a "detailed" or "lengthy" output variant.
    rephrased_text = only_rephrase.rephrase_text(input_message, "technical", "detailed")
    print("Technical Rephrase:\n", rephrased_text)


def test_rephase_text_apologetic() -> None:
    """
    Test the rephrase_text method with an apologetic style.

    Rephrases a message apologizing for a delay, using a respectful and lengthy tone.
    """
    input_message = """
    I apologize for the delay in my response. I understand that this has caused inconvenience, and I am truly sorry.
    """
    only_rephrase = OnlyRephrase()
    rephrased_text = only_rephrase.rephrase_text(input_message, "apologetic", "lengthy")
    print("Apologetic Rephrase:\n", rephrased_text)
