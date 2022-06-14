from prompt_refresher.promptEngine import PromptEngine, PromptEngineConfig
from prompt_refresher.modelConfig import ModelConfig
from prompt_refresher.interaction import Interaction

config = PromptEngineConfig(ModelConfig(max_tokens=50), commentOperator = "###")
description = "This code takes in natural language utterance and generates code This code takes in natural language utterance and generates code"
examples = [Interaction("Hello", "print('Hello')"), Interaction("Goodbye", "print('Goodbye')")]
dialog = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
promptEngine = PromptEngine(config, description, examples, dialog)

print (promptEngine.buildContext())


config = PromptEngineConfig(ModelConfig(max_tokens=50), commentOperator = "###")
description = "This code takes in natural language utterance and generates code This code takes in natural language utterance and generates code"
promptEngine = PromptEngine(config, description)

promptEngine.addExample(Interaction("Hello", "print('Hello')"))
promptEngine.addExample(Interaction("Goodbye", "print('Goodbye')"))
promptEngine.addInteraction(Interaction("Hi", "print('Hi')"))
promptEngine.addInteraction(Interaction("Bye", "print('Bye')"))

print(promptEngine.buildContext())
