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


config = PromptEngineConfig(ModelConfig(max_tokens=50), comment_operator = "###")
description = "This code takes in natural language utterance and generates code This code takes in natural language utterance and generates code"
high_level_context = ["Hi", "Bye"]
prompt_engine = PromptEngine(config, description, high_level_context)

prompt_engine.add_example(Interaction("Hello", "print('Hello')"))
prompt_engine.add_example(Interaction("Goodbye", "print('Goodbye')"))
prompt_engine.add_interaction(Interaction("Hi", "print('Hi')"))
prompt_engine.add_interaction(Interaction("Bye", "print('Bye')"))

print(prompt_engine.build_context())
