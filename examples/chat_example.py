from prompt_engine.prompt_engine import PromptEngine, PromptEngineConfig
from prompt_engine.model_config import ModelConfig
from prompt_engine.interaction import Interaction

config = PromptEngineConfig(ModelConfig(max_tokens=50), description_prefix = "###")
description = "This code takes in natural language utterance and generates code This code takes in natural language utterance and generates code"
examples = [Interaction("Hello", "print('Hello')"), Interaction("Goodbye", "print('Goodbye')")]
flow_reset_text = "Delete the previous objects and start afresh"
interactions = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
prompt_engine = PromptEngine(config, description, examples, flow_reset_text, interactions)

print (prompt_engine.build_context())