from src.prompt_refresher.promptEngine import PromptEngine, PromptEngineConfig
from src.prompt_refresher.modelConfig import ModelConfig
from src.prompt_refresher.interaction import Interaction

def test_pass_1():
    config = PromptEngineConfig(ModelConfig(max_tokens=32), commentOperator = "###")
    description = "This code takes in natural language utterance and generates code This code takes in natural language utterance and generates code"
    examples = [Interaction("Hello", "print('Hello')"), Interaction("Goodbye", "print('Goodbye')")]
    dialog = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
    promptEngine = PromptEngine(config, description, examples, dialog)
    assert promptEngine.buildContext() != ""

def test_pass_2():
    config = PromptEngineConfig(ModelConfig(max_tokens=32), commentOperator = "###")
    description = ""
    promptEngine = PromptEngine(config, description)
    assert promptEngine.buildContext() != ""


def test_pass_3():
    config = PromptEngineConfig()
    description = ""
    dialog = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
    promptEngine = PromptEngine(config, description, dialog=dialog)
    promptEngine.buildContext()
    promptEngine.removeLastInteraction()
    assert promptEngine.buildContext() == "## Hi\nprint('Hi')\n"



def test_fail_1():
    config = PromptEngineConfig()
    description = ""
    promptEngine = PromptEngine(config, description)
    assert promptEngine.buildContext() == ""
