from src.prompt_refresher.promptEngine import PromptEngine, PromptEngineConfig
from src.prompt_refresher.modelConfig import ModelConfig
from src.prompt_refresher.interaction import Interaction

def test_pass():
    config = PromptEngineConfig(ModelConfig(max_tokens=32), commentOperator = "###")
    description = "This code takes in natural language utterance and generates code This code takes in natural language utterance and generates code"
    examples = [Interaction("Hello", "print('Hello')"), Interaction("Goodbye", "print('Goodbye')")]
    dialog = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
    promptEngine = PromptEngine(config, description, examples, dialog)
    assert promptEngine.buildContext() != ""

def test_pass_model_config():
    config = PromptEngineConfig(ModelConfig(max_tokens=32), commentOperator = "###")
    description = ""
    promptEngine = PromptEngine(config, description)
    assert promptEngine.buildContext() != ""


def test_pass_no_paramters():
    config = PromptEngineConfig()
    description = ""
    promptEngine = PromptEngine(config, description)
    assert promptEngine.buildContext() == ""

def test_pass_removeLastInteraction():
    config = PromptEngineConfig()
    description = ""
    dialog = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
    promptEngine = PromptEngine(config, description, dialog=dialog)
    promptEngine.buildContext()
    promptEngine.removeLastInteraction()
    assert promptEngine.buildContext() == "## Hi\nprint('Hi')\n"

def test_fail_removeLastInteraction():
    config = PromptEngineConfig()
    description = ""
    promptEngine = PromptEngine(config, description)
    promptEngine.buildContext()
    try:
        promptEngine.removeLastInteraction()
    except Exception as e:
        assert str(e) == "No interactions to remove"

def test_pass_removeFirstInteraction():
    config = PromptEngineConfig()
    description = ""
    dialog = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
    promptEngine = PromptEngine(config, description, dialog=dialog)
    promptEngine.buildContext()
    promptEngine.removeFirstInteraction()
    assert promptEngine.buildContext() == "## Bye\nprint('Bye')\n"

def test_fail_removeFirstInteraction():
    config = PromptEngineConfig()
    description = ""
    promptEngine = PromptEngine(config, description)
    promptEngine.buildContext()
    try:
        promptEngine.removeFirstInteraction()
    except Exception as e:
        assert str(e) == "No interactions to remove"

def test_pass_addInteraction():
    config = PromptEngineConfig()
    description = ""
    dialog = [Interaction("Hi", "print('Hi')")]
    promptEngine = PromptEngine(config, description, dialog=dialog)
    promptEngine.buildContext()
    promptEngine.addInteraction(Interaction("Bye", "print('Bye')"))
    assert promptEngine.buildContext() == "## Hi\nprint('Hi')\n## Bye\nprint('Bye')\n"