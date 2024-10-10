import ollama
import typer

from yodapa.plugin_manager.decorator import yoda_plugin


@yoda_plugin("ai")
class AICommandGenerator:
    def _communicate_with_ollama(self, prompt: str):
        try:
            response = ollama.chat(
                model="codellama",
                messages=[{"role": "user", "content": prompt}],
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

    def chat(self, prompt: str):
        """
        Chat with the AI model based on the provided prompt.

        Args:
            prompt (str): The prompt to start the conversation.
        """
        # typer.echo(f"Starting chat with prompt: {prompt}")

        try:
            # Interact with the Ollama LLM
            response = self._communicate_with_ollama(prompt)
            typer.echo(f"🤖 AI response:\n{response}")

        except Exception as e:
            typer.echo(f"Error chatting with AI: {e}", err=True)
            typer.echo(f"Failed to chat with AI: {e}", err=True)

    def generate_command(self, plugin_name: str, prompt: str):
        """
        Generate code for a new plugin command based on the provided prompt.

        Args:
            prompt (str): The description or functionality of the desired command.
            plugin_name (str): The name for the new plugin.
        """
        typer.echo(f"Generating command for plugin: {plugin_name} with prompt: {prompt}")

        # Construct the prompt for the AI model
        ai_prompt = f"""
        Generate a Python Typer plugin class named "{plugin_name}" with a single command and multiple subcommands as required based on the following description:

        {prompt}.

        The plugin should follow the existing structure, using the 'yoda_plugin' decorator and include appropriate docstrings. An example of the expected output is provided below:
        ```python
        import typer
        
        from yodapa.plugin_manager.decorator import yoda_plugin
        
        
        @yoda_plugin(name="hi")
        class HiPlugin:
            \"\"\"
            Hi plugin. Say hello.
        
            Example:
                $ yoda hi hello --name MP
                $ yoda hi hello
            \"\"\"
        
            def hello(self, name: str = None):
                \"\"\"Say hello.\"\"\"
                name = name or "Padawan"
                typer.echo(f"Hello {{name}}!")
        
            def how_are_you(self, name: str = None):
                \"\"\"Respond to How are you.\"\"\"
                name = name or "Padawan"
                typer.echo(f"I'm good, how are you, {{name}}?")
        ```   
        
        You must only return the generated code for the plugin class. All the details for the plugin class should be added in the docstring.
        You must use all the python best practices to write the most efficient python code. Provide complete working code for all the subcommands.
        """

        try:
            # Interact with the Ollama LLM
            generated_code = self._communicate_with_ollama(ai_prompt)
            typer.echo(f"🤖 Generated code:\n{generated_code}")

            # Define the plugin file path
            # plugin_file = self.output_dir / f"{plugin_name.lower()}_plugin.py"
            #
            # # Write the generated code to the plugin file
            # with open(plugin_file, "w") as f:
            #     f.write(generated_code)
            # typer.echo(f"Generated plugin saved to {plugin_file}")
            #
            # typer.echo(f"Plugin '{plugin_name}' has been generated and saved to {plugin_file}")

        except Exception as e:
            typer.echo(f"Error generating plugin: {e}", err=True)
            typer.echo(f"Failed to generate plugin: {e}", err=True)
