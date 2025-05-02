# MIT License
#
# Copyright (c) 2025 elevate-human-experiences
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module to test the Python code generation functionalities of the OnlyPython class."""

from elevate.only_python import OnlyPython


def test_generate_code_simple_function_generation() -> None:
    """Tests the generate_code method of the OnlyPython class with a simple function generation task.

    The task involves creating a function that adds two numbers and then executing that function.
    The generated code is then printed to the console for verification.
    """
    input_message = """
  Create a function that adds two numbers and execute that function.
  """
    only_python = OnlyPython()
    output = only_python.generate_code(input_message, "", False, False)
    print(output)


# test_generate_code_simple_function_generation()


def test_api_call() -> None:
    """Tests the generate_code method's ability to generate code that fetches data from an API.

    The function provides an API endpoint and a sample response, and instructs the generate_code method
    to fetch data from the API for a specific product ID. The generated code is then printed to the console.
    """
    sample_api_response = """
  """
    api = ""
    input_message = f"""
  Fetch data of product id 2 from given api.
  API : {api}
  Sample reponse from the api:{sample_api_response}
  """
    only_python = OnlyPython()
    output = only_python.generate_code(input_message, "", True, False)
    print("\n" + "*" * 20 + " Printing Final Output " + "*" * 20 + "\n")
    print("\nOutput:\n", output)
    print("\n" + "*" * 20 + " End of Printing " + "*" * 20 + "\n")


# test_api_call()


def test_internet_connection() -> None:
    """Tests the generate_code method's ability to generate code that makes an internet connection.

    The function instructs the generate_code method to create a function that sends a request to google.com.
    The generated code is then printed to the console.
    """
    input_message = """
  Create a function to send request to google.com.
  """
    only_python = OnlyPython()
    output = only_python.generate_code(input_message, "", False, False)
    print("\n" + "*" * 20 + " Printing Final Output " + "*" * 20 + "\n")
    print("\nOutput:\n", output)
    print("\n" + "*" * 20 + " End of Printing " + "*" * 20 + "\n")


# test_internet_connection()


def test_data_structure_code() -> None:
    """Tests the generate_code method's ability to generate code that manipulates a data structure (linked list).

    The function instructs the generate_code method to create code that deletes the middle node of a linked list.
    The generated code is then printed to the console.
    """
    input_message = """
  """
    only_python = OnlyPython()
    output = only_python.generate_code(input_message, "", True, False)
    print("\n" + "*" * 20 + " Printing Final Output " + "*" * 20 + "\n")
    print("\nOutput:\n", output)
    print("\n" + "*" * 20 + " End of Printing " + "*" * 20 + "\n")


# test_data_structure_code()


def test_data_visualization() -> None:
    """Tests the generate_code method's ability to generate code that performs data visualization.

    The function instructs the generate_code method to create code that plots a given set of x and y values.
    The generated code is then printed to the console.
    """
    input_message = """
  Plot below numbers
  x value: [1,2,3,4,5]
  y value: [2,4,6,8,10]
  """
    only_python = OnlyPython()
    output = only_python.generate_code(input_message, "", False, True)
    print("\n" + "*" * 20 + " Printing Final Output " + "*" * 20 + "\n")
    print("\nOutput:\n", output)
    print("\n" + "*" * 20 + " End of Printing " + "*" * 20 + "\n")


# test_data_visualization()


def test_only_email_code_generation() -> None:
    """Tests the generation of a personal email.

    This function uses the OnlyEmail class to generate a personal email based on a
    given input message and then prints the generated email.
    """
    personal_email_input_message = """
    A wedding anuversary message to John and Jane.
    """
    only_python = OnlyPython()
    output = only_python.generate_code(personal_email_input_message, "", False, False)
    print("\n" + "*" * 20 + " Printing Final Output " + "*" * 20 + "\n")
    print("\nOutput:\n", output)
    print("\n" + "*" * 20 + " End of Printing " + "*" * 20 + "\n")


test_only_email_code_generation()
