# Minitel


Introduction and demo at [maxf.github.io/minitel](maxf.github.io/minitel)

# Setup

You need:
- a minitel
- a DIN-to-USB cable. See [Pila's page](https://pila.fr/wordpress/?p=361)
- a computer with python3 installed, as well as [poetry](https://python-poetry.org/) for package management.
- an key for the [OpenAI API](https://openai.com/blog/openai-api)

Run `poetry install` to install the packages needed.

Set the `OPENAI_API_KEY` environment variable to the value of your API key and run the application. For instance:

```
OPENAI_API_KEY=abcdef01239wskdfo338y poetry run python 3615-gpt.py
```

and the intro page should display on your Minitel.
