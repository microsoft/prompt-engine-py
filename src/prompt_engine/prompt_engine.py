from prompt_engine.interaction import Interaction
from prompt_engine.model_config import ModelConfig
from typing import List
from prompt_engine.utils.encoder import Encoder, get_encoder
import yaml

class PromptEngineConfig: 
    """
    This class provides the configuration for the Prompt Engine
    """
    def __init__(self, model_config: ModelConfig = ModelConfig(max_tokens=1024), description_prefix: str = "", description_postfix: str = "", newline_operator: str = "\n",
                 input_prefix: str = "", input_postfix: str = "", output_prefix: str = "", output_postfix: str = ""):
                 
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
    def __init__(self, config: PromptEngineConfig = PromptEngineConfig(), description: str = "", examples: List[Interaction] = [], flow_reset_text: str = "", dialog: List[Interaction] = []):
        
        self.config = config
        self.description = description
        self.examples = examples
        self.flow_reset_text = flow_reset_text
        self.dialog = dialog
        self.encoder = get_encoder()

    def load_yaml(self, yaml_config: str):
        """
        Loads the yaml file and initializes the Prompt Engine
        """

        yaml_data = yaml.load(yaml_config, Loader=yaml.FullLoader)
        
        if "type" in yaml_data:
            self._load_config_yaml(yaml_data)
        else:
            raise Exception("Invalid yaml file type")
        
        if "description" in yaml_data:        
            self.description = yaml_data["description"]
        else:
            self.description = ""

        if "examples" in yaml_data:
            self.examples = [Interaction(data["input"], data["response"]) for data in yaml_data["examples"]]
        else:
            self.examples = []

        if "flow-reset-text" in yaml_data:
            self.flow_reset_text = yaml_data["flow-reset-text"]
        else:
            self.flow_reset_text = ""

        if "dialog" in yaml_data:
            self.dialog = [Interaction(data["input"], data["response"]) for data in yaml_data["dialog"]]
        else:
            self.dialog = []

    def _load_config_yaml(self, yaml_data):
        """
        Adds the engine yaml config to the prompt engine
        """

        if yaml_data["type"] == "prompt-engine":
            if "config" in yaml_data:
                config_data = yaml_data["config"]
                config_data = {k.replace('-', '_'): v for k, v in config_data.items()}
                if "model_config" in config_data:
                    model_config_data = {k.replace('-', '_'): v for k, v in config_data["model_config"].items()}
                    self.model_config = ModelConfig(**model_config_data)
                    config_data.pop("model_config")
                    self.config = PromptEngineConfig(model_config = self.model_config, **config_data)
                else:
                    self.config = PromptEngineConfig(**config_data)
            else:
                self.config = PromptEngineConfig()
        else:
            raise Exception("Invalid yaml file type")

    def save_yaml(self):

        yaml_data = {}
        yaml_data['type'] = "prompt-engine"
        yaml_data['description'] = self.description
        yaml_data['examples'] = [{'input': example.input, 'response': example.response} for example in self.examples]
        yaml_data['flow-reset-text'] = self.flow_reset_text
        yaml_data['dialog'] = [{'input': interaction.input, 'response': interaction.response} for interaction in self.dialog]
        yaml_data['config'] = {
            'model_config': {k: v for k, v in self.config.model_config.__dict__.items() if v != None},
            'description_prefix': self.config.description_prefix[:-1],
            'description_postfix': self.config.description_postfix[1:],
            'input_prefix': self.config.input_prefix[:-1],
            'input_postfix': self.config.input_postfix[1:],
            'output_prefix': self.config.output_prefix[:-1],
            'output_postfix': self.config.output_postfix[1:],
            'newline_operator': self.config.newline_operator
        }

        return yaml.dump(yaml_data, default_flow_style=False)
    

    def build_context(self, user_input: str = "", multi_turn: bool = True):
        """
        Builds the context from the description, examples, and interactions.
        """
        context: str = ""

        # Add the description to the context
        context = self._insert_description(context, user_input)
        
        # Add the examples to the context
        context = self._insert_examples(context, user_input)
        
        # Checks if the number of tokens after adding the examples in the context is greater than the max_tokens
        if (self.config.model_config != None and self._assert_token_limit(context, user_input, self.config.model_config.max_tokens)):
            raise Exception("Token limit exceeded, reduce the number of examples or size of description. Alternatively, you may increase the max_tokens in ModelConfig")
        
        # Add the flow reset text to the context
        context = self._insert_flow_reset_text(context, user_input)

        if multi_turn:
            # Add the interactions to the context
            context = self._insert_interactions(context, user_input)

        return context

    def build_prompt(self, user_input: str, multi_turn: bool = True, newline_end: bool = True):
        """
        Builds the prompt from the parameters given to the Prompt Engine 
        """
        formatted_input = self.format_input(user_input, newline_end)
        prompt = self.build_context(formatted_input, multi_turn)
        prompt += formatted_input

        return prompt

    def build_dialog(self):
        temp_interactions = ""
        if (self.dialog != []):
            for interaction in self.dialog:
                temp_interaction_text = self.config.input_prefix + interaction.input + self.config.input_postfix + self.config.newline_operator
                temp_interaction_text += self.config.output_prefix +  interaction.response + self.config.output_postfix +  self.config.newline_operator*2

                temp_interactions += temp_interaction_text

        return temp_interactions

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
            
                if (self._assert_token_limit(context + temp_examples_text + temp_example_text, user_input, self.config.model_config.max_tokens)):
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
        temp_interactions_text = ""
        if (self.dialog != []):
            for interaction in self.dialog[::-1]:
                temp_interaction_text = self.config.input_prefix + interaction.input + self.config.input_postfix + self.config.newline_operator
                temp_interaction_text += self.config.output_prefix +  interaction.response + self.config.output_postfix +  self.config.newline_operator*2

                if (self._assert_token_limit(context + temp_interactions_text + temp_interaction_text, user_input, self.config.model_config.max_tokens)):
                    break
                
                temp_interactions_text = temp_interaction_text + temp_interactions_text

            context += temp_interactions_text
        
        return context
    
    def format_input(self, user_input: str = "", newline_end: bool = True):
        """
        Inserts the prompt into the context
        """
        temp_prompt_text = ""
        if (user_input != ""):
            temp_prompt_text += self.config.input_prefix + user_input + self.config.input_postfix
            if (newline_end):
                temp_prompt_text += self.config.newline_operator

        return temp_prompt_text
    
    def reset_context(self):
        self.dialog = []
        return self.build_context()

    def _assert_token_limit(self, context: str, user_input: str = "", max_tokens: int = 1024):
        """
        Asserts that the number of tokens in the context is less than the max_tokens
        """
        if context != None and user_input != None:
            if context != "":
                num_tokens = len(self.encoder.encode(context))
                if user_input != "":
                    num_tokens = len(self.encoder.encode(context + user_input))
                if num_tokens > max_tokens:
                    return True
                else:
                    return False
            else:
                return False
        else:
            raise Exception("The string to assert is None")