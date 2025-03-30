from elevate.only_markdown import OnlyMarkdown

input_text = """

"""


def test_simple_text_markdown_conversion() -> None:
    """
    Tests the conversion of simple text to Markdown format using the OnlyMarkdown class.

    The test does *not* include assertions; it focuses on generating output
    for manual inspection of the Markdown conversion.

    Note: The test saves the output to "tests/only_markdown_sample_output.md".
    """
    content = input_text
    only_markdown = OnlyMarkdown(with_model="gemini/gemini-2.0-flash-lite")
    with open("tests/only_markdown_sample_output.md", "w") as file:
        file.write(only_markdown.convert_to_markdown(content))


# test_simple_text_markdown_conversion()


def test_simple_text_summarization() -> None:
    """
    Tests the conversion of simple text to Markdown format using the OnlyMarkdown class.

    The test does *not* include assertions; it focuses on generating output
    for manual inspection of the Markdown conversion.

    Note: The test saves the output to "tests/only_markdown_sample_output.md".
    """
    content = input_text
    only_markdown = OnlyMarkdown(with_model="gemini/gemini-2.0-flash-lite")
    with open("tests/only_markdown_sample_output.md", "w") as file:
        file.write(only_markdown.summarize_and_convert_to_markdown(content))


# test_simple_text_summarization()


def test_information_from_an_article_markdown() -> None:
    """Tests summarization of online article content into Markdown."""
    # write code to read text from an article online and call text_simple_test_summarization function
    pass


def test_read_from_document_markdown() -> None:
    """Tests summarization of document content into Markdown."""
    # write code to read text from document and call text_simple_test_summarization function
    pass
