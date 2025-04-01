"""Module to test the text summarization functionality of the OnlySummary class."""

from elevate.only_summary import OnlySummary

input_text = """ """


def test_simple_text_summarization() -> None:
    """
    Tests the summarization of simple text using the OnlySummary class.
    """
    content = input_text
    only_summary_instance = OnlySummary(with_model="gemini/gemini-1.5-flash-latest")
    summary_output = only_summary_instance.summarize_and_convert_to_markdown(content)
    print(summary_output)


# test_simple_text_summarization()
