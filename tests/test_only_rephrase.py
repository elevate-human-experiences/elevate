"""Module to test the email generation functionalities of the OnlyEmail class."""

from elevate.only_rephrase import OnlyRephrase


def test_rephase_text_formal() -> None:
    """
    Test the rephrase_text method with a formal style.

    This test case uses the OnlyRephrase class to rephrase an input message
    with a formal style and a lengthy output. It then prints the rephrased text.
    """
    input_message = """
    I need 2 days of sick leave.
    """
    only_rephrase = OnlyRephrase(with_model="gemini/gemini-2.0-flash-lite")
    rephrased_text = only_rephrase.rephrase_text(input_message, "fomral", "lengthy")
    print(rephrased_text)


test_rephase_text_formal()


def test_rephase_text_informal() -> None:
    """
    Test the rephrase_text method with a infformal style.

    This test case uses the OnlyRephrase class to rephrase an input message
    with a informal style and a short output. It then prints the rephrased text.
    """
    input_message = """
    I need 2 days of sick leave.
    """
    only_rephrase = OnlyRephrase(with_model="gemini/gemini-2.0-flash-lite")
    rephrased_text = only_rephrase.rephrase_text(input_message, "informal", "short")
    print(rephrased_text)


test_rephase_text_informal()


def test_rephase_text_urgent() -> None:
    """
    Test the rephrase_text method with an urgent style.

    This test case uses the OnlyRephrase class to rephrase an input message
    with an urgent style and a lengthy output. It then prints the rephrased text.
    """
    input_message = """
    This is a serious problem that needs to be addressed immediately.
    """
    only_rephrase = OnlyRephrase(with_model="gemini/gemini-2.0-flash-lite")
    rephrased_text = only_rephrase.rephrase_text(input_message, "urgent", "lengthy")
    print(rephrased_text)


test_rephase_text_urgent()


def test_rephase_text_enthusiastic() -> None:
    """
    Test the rephrase_text method with an enthusiastic style.

    This test case uses the OnlyRephrase class to rephrase an input message
    with an enthusiastic style and a medium output. It then prints the
    rephrased text.
    """
    input_message = """
    I'm so excited about this project!
    """
    only_rephrase = OnlyRephrase(with_model="gemini/gemini-2.0-flash-lite")
    rephrased_text = only_rephrase.rephrase_text(
        input_message, "enthusiastic", "medium"
    )
    print(rephrased_text)


test_rephase_text_enthusiastic()


def test_rephase_text_infromative() -> None:
    """
    Test the rephrase_text method with an informative style.

    This test case uses the OnlyRephrase class to rephrase an input
    message with an informative style and a lengthy output. It then
    prints the rephrased text.
    """
    input_message = """
    The system utilizes a multi-threaded architecture to improve performance..
    """
    only_rephrase = OnlyRephrase(with_model="gemini/gemini-2.0-flash-lite")
    rephrased_text = only_rephrase.rephrase_text(
        input_message, "informative", "lengthy"
    )
    print(rephrased_text)


test_rephase_text_infromative()
