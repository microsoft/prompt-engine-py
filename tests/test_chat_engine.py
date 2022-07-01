from src.prompt_engine.chat_engine import ChatEngine, ChatEngineConfig
from src.prompt_engine.model_config import ModelConfig
from src.prompt_engine.interaction import Interaction

def test_pass():
    config = ChatEngineConfig(ModelConfig(max_tokens=1024))
    description = "Convert the given english to french"
    examples = [Interaction("Hello", "Bonjour"), Interaction("Goodbye", "Au revoir")]
    dialog = [Interaction("I am going", "Je vais"), Interaction("great", "génial")]
    chat_engine = ChatEngine(config=config, description=description, examples=examples, dialog=dialog)
    assert chat_engine.build_context() == "Convert the given english to french\n\nUSER: Hello\nBOT: Bonjour\n\nUSER: Goodbye\nBOT: Au revoir\n\nUSER: I am going\nBOT: Je vais\n\nUSER: great\nBOT: génial\n\n"