from prompt_engine.prompt_engine import PromptEngine, PromptEngineConfig
from prompt_engine.model_config import ModelConfig
from prompt_engine.interaction import Interaction

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