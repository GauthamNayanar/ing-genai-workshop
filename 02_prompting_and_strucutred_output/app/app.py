import argparse
from prompt_toolkit import print_formatted_text, prompt, HTML
from prompt_toolkit.completion import WordCompleter

from llm import ask_llm
from utils import format_response


# Example travel topics for autocompletion
travel_completer = WordCompleter([
    "I love art and museums",
    "Looking for good food spots",
    "Find cheap flights to Tokyo",
    "Estimate daily budget in Amsterdam",
], ignore_case=True)

def main():
    parser = argparse.ArgumentParser(description="Travel Assistant")
    parser.add_argument("prompt", type=str, nargs="?", help="User travel query prompt")
    args = parser.parse_args()

    if not args.prompt:
        user_prompt = prompt(HTML('<skyblue>Enter your travel query:</skyblue> '), completer=travel_completer)
    else:
        user_prompt = args.prompt

    print("\n=== Travel Assistant ===\n")
    response = ask_llm(
        user_prompt,
    )
    print_formatted_text(format_response(response))
    print("\n")

if __name__ == "__main__":
    main()
