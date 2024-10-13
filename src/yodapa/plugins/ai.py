import ollama
import typer

app = typer.Typer(help="AI command. Allows you to communicate with your local LLMs")


def _communicate_with_ollama(prompt: str):
    try:
        response = ollama.chat(
            model="codellama",
            messages=[{"role": "system", "content": "You should talk like Yoda from star wars"},
                      {"role": "user", "content": prompt}],
            stream=False,
        )
        # typer.echo(f"Received response from Ollama: {response['message']['content'].strip()}")
        return response['message']['content'].strip()
    except ollama.ResponseError as e:
        typer.echo(f"Error communicating with Ollama: {e}", err=True)
        typer.echo(f"Failed to communicate with Ollama: {e}", err=True)

        typer.echo("If you don't have ollama installed, you can install it by going through the instructions on "
                   "their website: https://ollama.com/ and installing the codellama model")
        raise


@app.command()
def chat(prompt: str):
    """
    Chat with the AI model based on the provided prompt.

    Args:
        prompt (str): The prompt to start the conversation.
    """
    # typer.echo(f"Starting chat with prompt: {prompt}")

    try:
        # Interact with the Ollama LLM
        response = _communicate_with_ollama(prompt)
        typer.echo(f"🤖 AI response:\n{response}")

    except Exception as e:
        typer.echo(f"Error chatting with AI: {e}", err=True)
        typer.echo(f"Failed to chat with AI: {e}", err=True)


@app.command()
def generate_command(plugin_name: str, prompt: str):
    """
    Generate code for a new plugin command based on the provided prompt.

    Args:
        prompt (str): The description or functionality of the desired command.
        plugin_name (str): The name for the new plugin.
    """
    typer.echo(f"Generating command for plugin: {plugin_name} with prompt: {prompt}")

    # Construct the prompt for the AI model
    ai_prompt = f"""
Generate a Python Typer app named "{plugin_name}" with multiple commands as required based on the following description:

{prompt}.
    """
    try:
        response = ollama.chat(
            model="codellama",
            messages=[{"role": "system", "content": """You are an expert python programmer. You must use all the python best practices to write the most efficient python code. Provide complete working code for all the subcommands. Provide full working code. If the plugin requires storage, use local storage like files or sqlite, whichever is easier to use.
You need to generate a typer command line app. An example app can be found below:
```python
import typer

app = typer.Typer(help=\"\"\"
    Hi plugin. Say hello.

    Example:

        $ yoda hi hello --name MP

        $ yoda hi hello
    \"\"\")


@app.command()
def hello(name: str = None):
    \"\"\"Say hello.\"\"\"
    name = name or "Padawan"
    typer.echo(f"Hello {{name}}!")
```   

You must only return the generated code for the plugin class. All the details for the plugin class should be added in the docstring.
When the user provides a description for their requirement, you must use all the best practices required to implement what they need.
            """},
                      {"role": "user", "content": prompt}],
            stream=False,
        )
        # typer.echo(f"Received response from Ollama: {response['message']['content'].strip()}")
        generated_code = response['message']['content'].strip()
        typer.echo(f"🤖 Generated code:\n{generated_code}")
    except ollama.ResponseError as e:
        typer.echo(f"Error communicating with Ollama: {e}", err=True)
        typer.echo(f"Failed to communicate with Ollama: {e}", err=True)

        typer.echo("If you don't have ollama installed, you can install it by going through the instructions on "
                   "their website: https://ollama.com/ and installing the codellama model")
