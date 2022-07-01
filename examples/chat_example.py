from prompt_engine.chat_engine import ChatEngine, ChatEngineConfig
from prompt_engine.model_config import ModelConfig
from prompt_engine.interaction import Interaction

config = ChatEngineConfig(ModelConfig(max_tokens=1024))
description = "Convert the given english to french"
examples = [Interaction("Hello", "Bonjour"), Interaction("Goodbye", "Au revoir")]
dialog = [Interaction("I am going", "Je vais"), Interaction("great", "génial")]
chat_engine = ChatEngine(config=config, description=description, examples=examples, dialog=dialog)

print (chat_engine.build_prompt("I am going"))