# pyGPTify

pyGPTify is a Python code formatter that uses OpenAI's GPT-3.5 Turbo model to improve code readability and adherence to clean code principles. The script accepts a Python source code file and formats it iteratively, printing the differences between the original and the newly formatted code after each iteration.

## Installation

1. Make sure you have Python 3.6 or higher installed.
2. Install the required libraries:

```
pip install ast difflib python-dotenv openai
```


3. Set up an API key for OpenAI. You can get one by signing up at [OpenAI](https://beta.openai.com/signup/).

4. Create a `.env` file in the project folder and add the following line, replacing `your_openai_api_key` with your actual API key:

OPENAI_API_KEY=your_openai_api_key


## Usage

To use pyGPTify, run the following command:

```
python pyGPTify.py <filename> [iterations]
```

- `<filename>`: The path to the Python source code file you want to format.
- `[iterations]` (optional): The number of iterations you want to run the formatting process. If not provided, the default value is 1.

## Example

```
python pyGPTify.py my_script.py 3
```


This command will format the `my_script.py` file three times, printing the differences between the original and the newly formatted code after each iteration.

## Note

This script is designed for formatting Python code and may not work as expected for other programming languages. It relies on OpenAI's GPT-3.5 Turbo model for formatting, so you'll need a valid API key to use the service.
