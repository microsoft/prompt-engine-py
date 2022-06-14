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

def test_pass_buildPrompt():
    config = PromptEngineConfig()
    description = ""
    dialog = [Interaction("Hi", "print('Hi')")]
    promptEngine = PromptEngine(config, description, dialog=dialog)
    promptEngine.buildContext()
    assert promptEngine.buildPrompt("Hello") == "## Hi\nprint('Hi')\n## Hello\n"

def test_pass_overriding_insert_examples():
    config = PromptEngineConfig()
    description = ""
    examples = [Interaction("Hi", "print('Hi')")]

    class PromptEngineOverloaded(PromptEngine):
        def _insert_examples(self):
            """
            Inserts the examples into the context
            """
            if (self.examples != []):
                for example in self.examples:
                    self.context += self.config.startSequence + "This is an example: " + example.naturalLanguage + self.config.stopSequence
                    self.context += self.config.newlineOperator
                    self.context += example.code + self.config.newlineOperator

    promptEngine = PromptEngineOverloaded(config, description, examples=examples)
    assert promptEngine.buildContext() == "##This is an example: Hi\nprint('Hi')\n"