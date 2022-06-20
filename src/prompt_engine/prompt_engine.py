from prompt_engine.interaction import Interaction
from prompt_engine.model_config import ModelConfig

class PromptEngineConfig: 
    """
    This class provides the configuration for the Prompt Engine
    """
    def __init__(self, model_config: ModelConfig = None, description_prefix: str = "#", description_postfix: str = "", newline_operator: str = "\n",
                 input_prefix: str = "##", input_postfix: str = "", output_prefix: str = "", output_postfix: str = ""):
        self.model_config = model_config
        self.description_prefix = description_prefix
        self.description_postfix = description_postfix
        self.newline_operator = newline_operator
        self.input_prefix = input_prefix
        self.input_postfix = input_postfix
        self.output_prefix = output_prefix
        self.output_postfix = output_postfix


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
        prompt: str = self.context + self.config.input_prefix + " " + natural_language + self.config.input_postfix

        if (newlineEnd):
            prompt += self.config.newline_operator

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

    def _insert_description(self):
        """
        Inserts the description into the context
        """
        temp_description_text = ""
        if (self.description != ""):
            temp_description_text += self.config.description_prefix + " " + self.description + self.config.description_postfix + self.config.newline_operator
            temp_description_text += self.config.newline_operator

            if (self.__assert_token_limit(self.context + temp_description_text, self.config.model_config.max_tokens)):
                raise Exception("Token limit exceeded, reduce the number of examples or size of description. Alternatively, you may increase the max_tokens in ModelConfig")
            
            self.context += temp_description_text

    def _insert_examples(self):
        """
        Inserts the examples into the context
        """
        temp_examples_text = ""
        if (self.examples != []):
            for example in self.examples:
                temp_example_text = self.config.input_prefix + " " + example.natural_language + self.config.input_postfix + self.config.newline_operator
                temp_example_text += example.code + self.config.newline_operator*2
            
                if (self.__assert_token_limit(self.context + temp_example_text, self.config.model_config.max_tokens)):
                    raise Exception("""Token limit exceeded, reduce the number of examples or size of description. Alternatively, you may increase the max_tokens in ModelConfig
                    It is highly recommended to lowering the number of examples to have more room for interactions""")

                temp_examples_text += temp_example_text

            self.context += temp_examples_text

    def _insert_flow_reset_text(self):
        """
        Inserts the examples into the context
        """
        temp_flow_reset_text = ""
        if (self.flow_reset_text != ""):
            temp_flow_reset_text += self.config.description_prefix + " " + self.flow_reset_text + self.config.description_postfix + self.config.newline_operator
            temp_flow_reset_text += self.config.newline_operator
           
            if (self.__assert_token_limit(self.context + temp_flow_reset_text, self.config.model_config.max_tokens)):
                raise Exception("Token limit exceeded, reduce the number of examples or size of description. Alternatively, you may increase the max_tokens in ModelConfig")
                
            self.context += temp_flow_reset_text


    def _insert_interactions(self):
        """
        Inserts the interactions into the context
        """
        temp_interactions_text = ""
        if (self.interactions != []):
            for interaction in self.interactions[::-1]:
                temp_interaction_text = self.config.input_prefix + " " + interaction.natural_language + self.config.input_postfix + self.config.newline_operator
                temp_interaction_text += interaction.code + self.config.newline_operator*2

                if (self.__assert_token_limit(self.context + temp_interaction_text, self.config.model_config.max_tokens)):
                    raise Warning("Token limit exceeded, skipping the least recent interaction")
                
                temp_interactions_text += temp_interaction_text

            self.context += temp_interactions_text + self.config.newline_operator
    
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