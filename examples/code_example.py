from prompt_engine.code_engine import CodeEngine, PythonCodeEngineConfig
from prompt_engine.model_config import ModelConfig
from prompt_engine.interaction import Interaction

config = PythonCodeEngineConfig(ModelConfig(max_tokens=1024))
description = "This code takes in natural language utterance and generates code This code takes in natural language utterance and generates code"
examples = [Interaction("Hello", "print('Hello')"), Interaction("Goodbye", "print('Goodbye')")]
interactions = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
code_engine = CodeEngine(config=config, description=description, examples=examples, interactions=interactions)

print (code_engine.build_context())