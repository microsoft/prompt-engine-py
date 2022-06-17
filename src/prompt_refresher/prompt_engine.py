from prompt_refresher.interaction import Interaction
from prompt_refresher.model_config import ModelConfig

class PromptEngineConfig: 
    """
    This class provides the configuration for the Prompt Engine
    """
    def __init__(self, model_config: ModelConfig = None, comment_operator: str = "#", comment_close_operator: str = "", newline_operator: str = "\n", start_sequence: str = "##", stop_sequence: str = ""):
        self.model_config = model_config
        self.comment_operator = comment_operator
        self.comment_close_operator = comment_close_operator
        self.newline_operator = newline_operator
        self.start_sequence = start_sequence
        self.stop_sequence = stop_sequence


class PromptEngine(object):
    """
    Prompt Engine provides a reusable interface for the developer to construct prompts for large scale language model inference
    """
    def __init__(self, config: PromptEngineConfig, description: str, examples: list = [], flow_reset_text = "", interactions: list = []):
        self.config = config
        self.description = description
        self.examples = examples
        self.flow_reset_text = flow_reset_text
        self.interactions = interactions

    def build_context(self):
        """
        Builds the context from the description, examples, and interactions.
        """
        self.context: str = ""

        # Add the model config parameters to the context
        self._insert_model_config()

        # Add the description to the context
        self._insert_description()
        
        # Add the examples to the context
        self._insert_examples()
        
        # Checks if the number of tokens after adding the examples in the context is greater than the max_tokens
        if (self.config.model_config != None and self.__assert_token_limit(self.context, self.config.model_config.max_tokens)):
            raise Exception("Token limit exceeded, reduce the number of examples or size of description. Alternatively, you may increase the max_tokens in ModelConfig")
        
        # Add the flow reset text to the context
        self._insert_flow_reset_text()

        # Add the interactions to the context
        self._insert_interactions()
        
        # Checks if the number of tokens after adding the interactions in the context is greater than the max_tokens, and if so, starts removing the most historical interactions
        if (self.config.model_config != None and self.__assert_token_limit(self.context, self.config.model_config.max_tokens)):
            self.remove_first_interaction()
            self.build_context()

        return self.context

    def build_prompt(self, natural_language: str, newlineEnd: bool = True):
        """
        Builds the prompt from the parameters given to the Prompt Engine 
        """
        prompt: str = self.context + self.config.start_sequence + " " + natural_language + self.config.stop_sequence

        if (newlineEnd):
            prompt += self.config.newline_operator

        return prompt

    def truncate_prompt(self, prompt: str):
        """
        Truncates the prompt to the max_tokens in the model_config
        """
        if (self.config.model_config != None and self.__assert_token_limit(prompt, self.config.model_config.max_tokens)):
            prompt = prompt.split()[:self.config.model_config.max_tokens]
            prompt = " ".join(prompt)
            return prompt
        else:
            return prompt
    
    def add_example(self, example: Interaction):
        """
        Adds an interaction to the example
        """
        self.examples.append(example)
    
    def add_interaction(self, interaction: Interaction):
        """
        Adds an interaction to the interactions
        """
        self.interactions.append(interaction)

    def remove_last_interaction(self):
        """
        Removes the last interaction from the interactions
        """
        if (len(self.interactions) > 0):
            self.interactions.pop()
        else:
            raise Exception("No interactions to remove")

    def remove_first_interaction(self):
        """
        Removes the first interaction from the interactions
        """
        if (len(self.interactions) > 0):
            self.interactions.pop(0)
        else:
            raise Exception("No interactions to remove")

    def _insert_model_config(self):
        """
        Inserts the model config into the context
        """
        if (self.config.model_config != None):
            prompt_engine_config_members = [attr for attr in dir(self.config.model_config) if not callable(getattr(self.config.model_config, attr)) and not attr.startswith("__")]
            for member in prompt_engine_config_members:
                self.context += self.config.comment_operator + " " + member + ": " + str(getattr(self.config.model_config, member)) + self.config.comment_close_operator + self.config.newline_operator
                self.context += self.config.newline_operator

    def _insert_description(self):
        """
        Inserts the description into the context
        """
        if (self.description != ""):
            self.context += self.config.comment_operator + " " + self.description + self.config.comment_close_operator + self.config.newline_operator
            self.context += self.config.newline_operator

    def _insert_examples(self):
        """
        Inserts the examples into the context
        """
        if (self.examples != []):
            for example in self.examples:
                self.context += self.config.start_sequence + " " + example.natural_language + self.config.stop_sequence + self.config.newline_operator
                self.context += example.code + self.config.newline_operator

    def _insert_flow_reset_text(self):
        """
        Inserts the examples into the context
        """
        if (self.flow_reset_text != ""):
           self.context += self.config.comment_operator + " " + self.flow_reset_text + self.config.comment_close_operator + self.config.newline_operator
           self.context += self.config.newline_operator

    def _insert_interactions(self):
        """
        Inserts the interactions into the context
        """
        if (self.interactions != []):
            for interaction in self.interactions:
                self.context += self.config.start_sequence + " " + interaction.natural_language + self.config.stop_sequence + self.config.newline_operator
                self.context += interaction.code + self.config.newline_operator
    
    def __assert_token_limit(self, context: str, max_tokens: int):
        """
        Asserts that the number of tokens in the context is less than the max_tokens
        """
        if context != None:
            if context != "":
                num_tokens = len(context.split())
                if num_tokens > max_tokens:
                    return True
                else:
                    return False
            else:
                return False
        else:
            raise Exception("The string to assert is None")
