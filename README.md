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




Copyright 2023 Max Froumentin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
