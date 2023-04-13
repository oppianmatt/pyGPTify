import os
import sys
import ast
import difflib
from dotenv import load_dotenv
import openai


def main(filename: str, iterations: int = 1) -> None:
    print(f"Formatting {filename} {iterations} times...")
    source = read_file(filename)

    compile_source(source)

    error = ""
    new_source = source

    for iteration in range(iterations):
        new_source, error = format_source(source, error)
        print_iteration_details(iteration + 1, source, new_source)
        try:
            compile_source(new_source)
            source = new_source
            write_file(filename, source)

        except SyntaxError as e:
            error = str(e)
            print_error(error)

    print(f"Formatted {filename}.")


def read_file(filename: str) -> str:
    with open(filename, "r") as file:
        return file.read()


def write_file(filename: str, source: str) -> None:
    with open(filename, "w") as file:
        file.write(source)


def compile_source(source: str) -> None:
    ast.parse(source)


def format_source(source: str, error: str) -> tuple[str, str]:
    prompt = create_prompt(source, error)
    response = call_openai(prompt)
    new_source = extract_code(response)

    return new_source, ""


def create_prompt(source: str, error: str) -> str:
    prompt = f"""
Please refactor the python code according to clean code principles:

## Design rules
1. Keep configurable data at high levels.
2. Prefer polymorphism to if/else or switch/case.
3. Separate multi-threading code.
4. Prevent over-configurability.
5. Use dependency injection.
6. Follow Law of Demeter. A class should know only its direct dependencies.

## Understandability tips
1. Be consistent. If you do something a certain way, do all similar things in the same way.
2. Use explanatory variables.
3. Encapsulate boundary conditions. Boundary conditions are hard to keep track of. Put the processing for them in one place.
4. Prefer dedicated value objects to primitive type.
5. Avoid logical dependency. Don't write methods which works correctly depending on something else in the same class.
6. Avoid negative conditionals.

## Names rules
1. Choose descriptive and unambiguous names.
2. Make meaningful distinction.
3. Use pronounceable names.
4. Use searchable names.
5. Replace magic numbers with named constants.
6. Avoid encodings. Don't append prefixes or type information.

## Functions rules
1. Small.
2. Do one thing.
3. Use descriptive names.
4. Prefer fewer arguments.
5. Have no side effects.
6. Don't use flag arguments. Split method into several independent methods that can be called from the client without the flag.

## Comments rules
1. Always try to explain yourself in code.
2. Don't be redundant.
3. Don't add obvious noise.
4. Don't use closing brace comments.
5. Don't comment out code. Just remove.
6. Use as explanation of intent.
7. Use as clarification of code.
8. Use as warning of consequences.

## Source code structure
1. Separate concepts vertically.
2. Related code should appear vertically dense.
3. Declare variables close to their usage.
4. Dependent functions should be close.
5. Similar functions should be close.
6. Place functions in the downward direction.
7. Keep lines short.
8. Don't use horizontal alignment.
9. Use white space to associate related things and disassociate weakly related.
10. Don't break indentation.

## Objects and data structures
1. Hide internal structure.
2. Prefer data structures.
3. Avoid hybrids structures (half object and half data).
4. Should be small.
5. Do one thing.
6. Small number of instance variables.
7. Base class should know nothing about their derivatives.
8. Better to have many functions than to pass some code into a function to select a behavior.
9. Prefer non-static methods to static methods.

## Tests
1. One assert per test.
2. Readable.
3. Fast.
4. Independent.
5. Repeatable.


Please return just the python code and nothing else.
Do not change places that have a comment that says "do not change".

{source}
    """

    if error:
        prompt += f"""
        The following error was raised when trying to compile a previous recommendation.
        So use that as a hint to fix the code:
        {error}
        """

    return prompt


def extract_code(response: str) -> str:
    script = response.strip()
    BACKTICKS = "```"
    # remove backticks at the start
    if script.startswith(BACKTICKS):
        script = script[len(BACKTICKS) :]
    # remove backticks at the end
    if script.endswith(BACKTICKS):
        script = script[: -(len(BACKTICKS))]
    return script


def call_openai(prompt: str) -> str:
    # call openai api, do not change this function
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    if completion.choices[0].finish_reason == "length":
        raise RuntimeError("Too large")
    return completion.choices[0].message.content


def print_iteration_details(iteration: int, source: str, new_source: str) -> None:
    print("=====================================")
    print(f"Iteration: {iteration}")
    print_diff(source, new_source)


def print_diff(string1: str, string2: str) -> None:
    lines1 = string1.splitlines()
    lines2 = string2.splitlines()
    diff = difflib.unified_diff(lines1, lines2)

    print("\n".join(diff))


def print_error(error: str) -> None:
    print(error)


if __name__ == "__main__":
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY", "")
    if len(sys.argv) > 2:
        filename = sys.argv[1]
        iterations = int(sys.argv[2])
        main(filename, iterations)
    elif len(sys.argv) > 1:
        filename = sys.argv[1]
        main(filename)
    else:
        print("No filename provided.")
