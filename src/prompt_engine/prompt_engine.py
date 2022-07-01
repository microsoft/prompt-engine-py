from prompt_engine.interaction import Interaction
from prompt_engine.model_config import ModelConfig
from typing import List

class PromptEngineConfig: 
    """
    This class provides the configuration for the Prompt Engine
    """
    def __init__(self, model_config: ModelConfig = ModelConfig(max_tokens=1024), description_prefix: str = "#", description_postfix: str = "", newline_operator: str = "\n",
                 input_prefix: str = "##", input_postfix: str = "", output_prefix: str = "", output_postfix: str = ""):
                 
        self.model_config = model_config
        self.newline_operator = newline_operator

        self.description_prefix = description_prefix + " " if description_prefix != "" else ""
        self.description_postfix = " " + description_postfix if description_postfix != "" else ""

        self.input_prefix = input_prefix + " " if input_prefix != "" else ""
        self.input_postfix = " " + input_postfix if input_postfix != "" else ""

        self.output_prefix = output_prefix + " " if output_prefix != "" else ""
        self.output_postfix = " " + output_postfix if output_postfix != "" else ""

class PromptEngine(object):
    """
    Prompt Engine provides a reusable interface for the developer to construct prompts for large scale language model inference
    """
    def __init__(self, config: PromptEngineConfig = PromptEngineConfig(), description: str = "", examples: List[Interaction] = [], flow_reset_text: str = "", interactions: List[Interaction] = []):
        self.config = config
        self.description = description
        self.examples = examples
        self.flow_reset_text = flow_reset_text
        self.dialog = interactions

    def build_context(self, user_input: str = ""):
        """
        Builds the context from the description, examples, and interactions.
        """
        context: str = ""

        # Add the description to the context
        context = self._insert_description(context)
        
        # Add the examples to the context
        context = self._insert_examples(context)
        
        # Checks if the number of tokens after adding the examples in the context is greater than the max_tokens
        if (self.config.model_config != None and self._assert_token_limit(context, user_input, self.config.model_config.max_tokens)):
            raise Exception("Token limit exceeded, reduce the number of examples or size of description. Alternatively, you may increase the max_tokens in ModelConfig")
        
        # Add the flow reset text to the context
        context = self._insert_flow_reset_text(context)

        # Add the interactions to the context
        context = self._insert_interactions(context)

        return context

    def build_prompt(self, user_input: str, newline_end: bool = True):
        """
        Builds the prompt from the parameters given to the Prompt Engine 
        """
        context = self.build_context(user_input)
        prompt: str = context + self.config.input_prefix + user_input + self.config.input_postfix + self.config.newline_operator

        return prompt

    def add_example(self, input: str, response: str):
        """
        Adds an interaction to the example
        """
        example = Interaction(input, response)
        self.examples.append(example)
    
    def add_interaction(self, input: str, response: str):
        """
        Adds an interaction to the interactions
        """
        interaction = Interaction(input, response)
        self.dialog.append(interaction)

    def remove_last_interaction(self):
        """
        Removes the last interaction from the interactions
        """
        if (len(self.dialog) > 0):
            return self.dialog.pop()
        else:
            raise Exception("No interactions to remove")

    def remove_first_interaction(self):
        """
        Removes the first interaction from the interactions
        """
        if (len(self.dialog) > 0):
            return self.dialog.pop(0)
        else:
            raise Exception("No interactions to remove")

    def _insert_description(self, context: str = "", user_input: str = ""):
        """
        Inserts the description into the context
        """
        temp_description_text = ""
        if (self.description != ""):
            temp_description_text += self.config.description_prefix + self.description + self.config.description_postfix +  self.config.newline_operator
            temp_description_text += self.config.newline_operator

            if (self._assert_token_limit(context + temp_description_text, user_input, self.config.model_config.max_tokens)):
                raise Exception("Token limit exceeded, reduce the number of examples or size of description. Alternatively, you may increase the max_tokens in ModelConfig")
            
            context += temp_description_text

        return context

    def _insert_examples(self, context: str = "", user_input: str = ""):
        """
        Inserts the examples into the context
        """
        temp_examples_text = ""
        if (self.examples != []):
            for example in self.examples:
                temp_example_text = self.config.input_prefix + example.input + self.config.input_postfix + self.config.newline_operator
                temp_example_text += self.config.output_prefix +  example.response + self.config.output_postfix +  self.config.newline_operator*2
            
                if (self._assert_token_limit(context + temp_example_text, user_input, self.config.model_config.max_tokens)):
                    raise Exception("""Token limit exceeded, reduce the number of examples or size of description. Alternatively, you may increase the max_tokens in ModelConfig
                    It is highly recommended to lowering the number of examples to have more room for interactions""")

                temp_examples_text += temp_example_text

            context += temp_examples_text
        
        return context

    def _insert_flow_reset_text(self, context: str = "", user_input: str = ""):
        """
        Inserts the examples into the context
        """
        temp_flow_reset_text = ""
        if (self.flow_reset_text != ""):
            temp_flow_reset_text += self.config.description_prefix + self.flow_reset_text + self.config.description_postfix + self.config.newline_operator
            temp_flow_reset_text += self.config.newline_operator
           
            if (self._assert_token_limit(context + temp_flow_reset_text, user_input, self.config.model_config.max_tokens)):
                raise Exception("Token limit exceeded, reduce the number of examples or size of description. Alternatively, you may increase the max_tokens in ModelConfig")
                
            context += temp_flow_reset_text

        return context

    def _insert_interactions(self, context: str = "", user_input: str = ""):
        """
        Inserts the interactions into the context
        """
        temp_interactions_list = []
        if (self.dialog != []):
            for interaction in self.dialog[::-1]:
                temp_interaction_text = self.config.input_prefix + interaction.input + self.config.input_postfix + self.config.newline_operator
                temp_interaction_text += self.config.output_prefix +  interaction.response + self.config.output_postfix +  self.config.newline_operator*2

                if (self._assert_token_limit(context + temp_interaction_text, user_input, self.config.model_config.max_tokens)):
                    break
                
                temp_interactions_list.append(temp_interaction_text)

            if (len(temp_interactions_list) > 0):
                context += "".join(temp_interactions_list[::-1])
        
        return context
    
    def reset_context(self):
        self.dialog = []
        return self.build_context()

    def _assert_token_limit(self, context: str, user_input: str = "", max_tokens: int = 1024):
        """
        Asserts that the number of tokens in the context is less than the max_tokens
        """
        if context != None and user_input != None:
            if context != "":
                num_tokens = len(context.split())
                if user_input != "":
                    num_tokens += len(user_input.split())
                if num_tokens > max_tokens:
                    return True
                else:
                    return False
            else:
                return False
        else:
            raise Exception("The string to assert is None")