from prompt_refresher.promptEngine import PromptEngine, PromptEngineConfig
from prompt_refresher.modelConfig import ModelConfig
from prompt_refresher.interaction import Interaction

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

config = PromptEngineConfig(ModelConfig(max_tokens=50), commentOperator = "###")
description = "This code takes in natural language utterance and generates code This code takes in natural language utterance and generates code"
examples = [Interaction("Hello", "print('Hello')"), Interaction("Goodbye", "print('Goodbye')")]
dialog = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
promptEngine = PromptEngineOverloaded(config, description, examples, dialog)

print (promptEngine.buildContext())