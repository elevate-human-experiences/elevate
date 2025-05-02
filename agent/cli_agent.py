from elevate.only_python import OnlyPython


def select_genai_snippet(menu_input: str) -> str:
    match menu_input:
        case "1":
            return "only_email.py"
        case "2":
            return "only_rephrase.py"
        case _:
            raise ValueError("Invalid menu type specified.")


def read_geni_snippet(genai_snippet: str) -> str:
    genai_snippet_code = ""
    with open(genai_snippet) as file:
        genai_snippet_code = file.read()
    return genai_snippet_code


def main(with_model: str = "gpt-4o-mini") -> None:
    """Run the command-line interface."""
    print("Welcome to the Elevate CLI Agent!")
    print("Using model:", with_model)
    while True:
        print("\nMenu \n1. Genrate an email \n2. Reframe the message\n3. exit")
        menu_input = input("Enter your choice: ")
        if menu_input.lower() == "3":
            break
        user_input = input("Enter your prompt: ")

        genai_snippet_code_file_name = "src/elevate/" + select_genai_snippet(menu_input)
        genai_snippet_code = read_geni_snippet(genai_snippet_code_file_name)
        # Here you would call the LLM with the user input

        only_python = OnlyPython()
        output = only_python.generate_code(
            user_input, "", False, False, genai_snippet_code
        )
        # print("\n" + "*" * 20 + " Printing Final Output " + "*" * 20 + "\n")
        print("\nOutput:\n", output)
        # print("\n" + "*" * 20 + " End of Printing " + "*" * 20 + "\n")


if __name__ == "__main__":
    main()
