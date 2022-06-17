from prompt_refresher.prompt_engine import PromptEngine, PromptEngineConfig
from prompt_refresher.model_config import ModelConfig
from prompt_refresher.interaction import Interaction

config = PromptEngineConfig(ModelConfig(max_tokens=50), comment_operator = "###")
description = "This code takes in natural language utterance and generates code This code takes in natural language utterance and generates code"
high_level_context = ["Hi", "Bye"]
examples = [Interaction("Hello", "print('Hello')"), Interaction("Goodbye", "print('Goodbye')")]
interactions = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
prompt_engine = PromptEngine(config, description, high_level_context, examples, interactions)

print (prompt_engine.build_context())