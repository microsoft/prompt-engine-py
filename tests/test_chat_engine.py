from src.prompt_engine.chat_engine import ChatEngine, ChatEngineConfig
from src.prompt_engine.model_config import ModelConfig
from src.prompt_engine.interaction import Interaction

def test_pass():
    config = ChatEngineConfig(ModelConfig(max_tokens=1024))
    description = "Convert the given english to french"
    examples = [Interaction("Hello", "Bonjour"), Interaction("Goodbye", "Au revoir")]
    interactions = [Interaction("I am going", "Je vais"), Interaction("great", "génial")]
    chat_engine = ChatEngine(config=config, description=description, examples=examples, interactions=interactions)
    assert chat_engine.build_context() == "Convert the given english to french\n\nYou:  Hello\nBot:  Bonjour\n\nYou:  Goodbye\nBot:  Au revoir\n\nYou:  I am going\nBot:  Je vais\n\nYou:  great\nBot:  génial\n\n"