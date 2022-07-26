from prompt_engine.prompt_engine import PromptEngine, PromptEngineConfig
from prompt_engine.model_config import ModelConfig
from prompt_engine.interaction import Interaction
import yaml

class ChatEngineConfig(PromptEngineConfig):
    """
    This class provides the configuration for the Chat Engine
    """
    def __init__(self, model_config: ModelConfig = ModelConfig(max_tokens=1024),
                 user_name: str = "USER", bot_name: str = "BOT"):
        super().__init__(model_config = model_config, description_prefix = "", description_postfix = "", newline_operator = "\n",
                                input_prefix = user_name + ":", input_postfix = "", output_prefix = bot_name + ":", output_postfix = "")

class ChatEngine(PromptEngine):
    """
    Chat Engine provides a PromptEngine to construct chat-like prompts for large scale language model inference
    """
    def __init__(self, config: ChatEngineConfig = ChatEngineConfig(), description: str = "", examples: list = [], flow_reset_text = "", dialog: list = []):
        super().__init__(config = config, description = description, examples = examples, flow_reset_text = flow_reset_text, dialog = dialog)
    
    def _load_config_yaml(self, yaml_data):
        """
        Adds the engine yaml config to the prompt engine
        """

        if yaml_data["type"] == "chat-engine":
            if "config" in yaml_data:
                config_data = yaml_data["config"]
                config_data = {k.replace('-', '_'): v for k, v in config_data.items()}
                if "model_config" in config_data:
                    model_config_data = {k.replace('-', '_'): v for k, v in config_data["model_config"].items()}
                    self.model_config = ModelConfig(**model_config_data)
                    config_data.pop("model_config")
                    self.config = ChatEngineConfig(model_config = self.model_config, **config_data)
                else:
                    self.config = ChatEngineConfig(**config_data)
            else:
                self.config = ChatEngineConfig()
        else:
            raise Exception("Invalid yaml file type")

    def save_yaml(self):
    
        yaml_data = {}
        yaml_data['type'] = "chat-engine"
        yaml_data['description'] = self.description
        yaml_data['examples'] = [{'input': example.input, 'response': example.response} for example in self.examples]
        yaml_data['flow-reset-text'] = self.flow_reset_text
        yaml_data['dialog'] = [{'input': interaction.input, 'response': interaction.response} for interaction in self.dialog]
        yaml_data['config'] = {
            'model_config': {k: v for k, v in self.config.model_config.__dict__.items() if v != None},
            'user_name': self.config.input_prefix[:-2], # remove the colon and space
            'bot_name': self.config.output_prefix[:-2] # remove the colon and space
        }
        return yaml.dump(yaml_data, default_flow_style=False)