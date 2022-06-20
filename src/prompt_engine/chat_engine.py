from prompt_engine.prompt_engine import PromptEngine, PromptEngineConfig
from prompt_engine.model_config import ModelConfig
from prompt_engine.interaction import Interaction

class ChatEngineConfig(PromptEngineConfig):
    """
    This class provides the configuration for the Code Engine
    """
    def __init__(self, model_config: ModelConfig = None,
                 firstUserName: str = "You", secondUserName: str = "Bot"):
        super().__init__(model_config = model_config, description_prefix = "", description_postfix = "", newline_operator = "\n",
                                input_prefix = firstUserName + ": ", input_postfix = "", output_prefix = secondUserName + ": ", output_postfix = "")

class ChatEngine(PromptEngine):
    """
    Chat Engine provides a PromptEngine to construct chat-like prompts for large scale language model inference
    """
    def __init__(self, config: ChatEngineConfig, description: str, examples: list = [], flow_reset_text = "", interactions: list = []):
        super().__init__(config = config, description = description, examples = examples, flow_reset_text = flow_reset_text, interactions = interactions)

"""
Example Usage:

config = ChatEngineConfig(ModelConfig(max_tokens=50))
description = "Convert the given english to french"
examples = [Interaction("Hello", "Bonjour"), Interaction("Goodbye", "Au revoir")]
interactions = [Interaction("I am going", "Je vais"), Interaction("great", "génial")]
code_engine = ChatEngine(config=config, description=description, examples=examples, interactions=interactions)

print (code_engine.build_context())

"""