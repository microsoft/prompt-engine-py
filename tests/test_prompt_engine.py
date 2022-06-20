from src.prompt_refresher.prompt_engine import PromptEngine, PromptEngineConfig
from src.prompt_refresher.model_config import ModelConfig
from src.prompt_refresher.interaction import Interaction

def test_pass():
    config = PromptEngineConfig(ModelConfig(max_tokens=32), description_prefix = "###")
    description = "This code takes in nl"
    examples = [Interaction("Hello", "print('Hello')"), Interaction("Goodbye", "print('Goodbye')")]
    interactions = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
    prompt_engine = PromptEngine(config = config, description = description, examples = examples, interactions = interactions)
    assert prompt_engine.build_context() == "### max_tokens: 32\n\n### This code takes in nl\n\n## Hello\nprint('Hello')\n## Goodbye\nprint('Goodbye')\n## Hi\nprint('Hi')\n## Bye\nprint('Bye')\n"

def test_pass_no_paramters():
    config = PromptEngineConfig()
    description = ""
    prompt_engine = PromptEngine(config, description)
    assert prompt_engine.build_context() == ""

def test_pass_remove_last_interaction():
    config = PromptEngineConfig()
    description = ""
    interactions = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
    prompt_engine = PromptEngine(config, description, interactions=interactions)
    prompt_engine.remove_last_interaction()
    assert prompt_engine.build_context() == "## Hi\nprint('Hi')\n"

def test_fail_remove_last_interaction():
    config = PromptEngineConfig()
    description = ""
    prompt_engine = PromptEngine(config, description)
    prompt_engine.build_context()
    try:
        prompt_engine.remove_last_interaction()
    except Exception as e:
        assert str(e) == "No interactions to remove"

def test_pass_remove_first_interaction():
    config = PromptEngineConfig()
    description = ""
    interactions = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
    prompt_engine = PromptEngine(config, description, interactions=interactions)
    prompt_engine.remove_first_interaction()
    assert prompt_engine.build_context() == "## Bye\nprint('Bye')\n"

def test_fail_remove_first_interaction():
    config = PromptEngineConfig()
    description = ""
    prompt_engine = PromptEngine(config, description)
    prompt_engine.build_context()
    try:
        prompt_engine.remove_first_interaction()
    except Exception as e:
        assert str(e) == "No interactions to remove"

def test_pass_add_interaction():
    config = PromptEngineConfig()
    description = ""
    interactions = [Interaction("Hi", "print('Hi')")]
    prompt_engine = PromptEngine(config, description, interactions=interactions)
    prompt_engine.add_interaction(Interaction("Bye", "print('Bye')"))
    assert prompt_engine.build_context() == "## Hi\nprint('Hi')\n## Bye\nprint('Bye')\n"

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
                    self.context += self.config.input_prefix + "This is an example: " + example.natural_language + self.config.input_postfix
                    self.context += self.config.newline_operator
                    self.context += example.code + self.config.newline_operator

    prompt_engineOverloaded = PromptEngineOverloaded(config, description, examples=examples)
    assert prompt_engineOverloaded.build_context() == "##This is an example: Hi\nprint('Hi')\n"

def test_pass_build_prompt():
    config = PromptEngineConfig()
    description = ""
    interactions = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
    prompt_engine = PromptEngine(config, description, interactions=interactions)
    prompt_engine.build_context()
    assert prompt_engine.build_prompt("Hello") == "## Hi\nprint('Hi')\n## Bye\nprint('Bye')\n## Hello\n"

def test_pass_add_example():
    config = PromptEngineConfig()
    description = ""
    examples = [Interaction("Hello", "print('Hello')"), Interaction("Goodbye", "print('Goodbye')")]
    interactions = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
    prompt_engine = PromptEngine(config, description, interactions=interactions, examples=examples)
    prompt_engine.add_example(Interaction("Hello there", "print('Hello there')"))
    assert prompt_engine.build_context() == "## Hello\nprint('Hello')\n## Goodbye\nprint('Goodbye')\n## Hello there\nprint('Hello there')\n## Hi\nprint('Hi')\n## Bye\nprint('Bye')\n"

def test_pass_flow_reset_text():
    config = PromptEngineConfig()
    description = "Trial Description"
    examples = [Interaction("Hello", "print('Hello')"), Interaction("Goodbye", "print('Goodbye')")]
    interactions = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
    flow_reset_text = "This is the flow reset text"
    prompt_engine = PromptEngine(config, description, interactions=interactions, flow_reset_text=flow_reset_text, examples=examples)
    assert prompt_engine.build_context() == "# Trial Description\n\n## Hello\nprint('Hello')\n## Goodbye\nprint('Goodbye')\n# This is the flow reset text\n\n## Hi\nprint('Hi')\n## Bye\nprint('Bye')\n"

def test_pass_masterIntegrationTest():
    config = PromptEngineConfig()
    description = ""
    interactions = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
    examples = [Interaction("Hello", "print('Hello')"), Interaction("Goodbye", "print('Goodbye')")]
    flow_reset_text = "This is the flow reset text"
    prompt_engine = PromptEngine(config, description, interactions=interactions, flow_reset_text=flow_reset_text, examples=examples)
    prompt_engine.add_interaction(Interaction("Bye", "print('Bye')"))
    prompt_engine.remove_first_interaction()
    prompt_engine.add_interaction(Interaction("Hello there", "print('Hello there')"))
    prompt_engine.remove_last_interaction()
    prompt_engine.add_example(Interaction("Hello there", "print('Hello there')"))
    prompt_engine.build_context()
    assert prompt_engine.build_prompt("Hello") == "## Hello\nprint('Hello')\n## Goodbye\nprint('Goodbye')\n# This is the flow reset text\n\n## Bye\nprint('Bye')\n## Bye\nprint('Bye')\n## Hello\n"