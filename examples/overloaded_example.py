from prompt_engine.prompt_engine import PromptEngine, PromptEngineConfig
from prompt_engine.model_config import ModelConfig
from prompt_engine.interaction import Interaction

class PromptEngineOverloaded(PromptEngine):
    def _insert_examples(self):
            """
            Inserts the examples into the context
            """
            if (self.examples != []):
                for example in self.examples:
                    self.context += self.config.input_prefix + "This is an example: " + example.input + self.config.input_postfix
                    self.context += self.config.newline_operator
                    self.context += example.response + self.config.newline_operator

config = PromptEngineConfig(ModelConfig(max_tokens=1024), description_prefix = "###")
description = "This code takes in natural language utterance and generates code This code takes in natural language utterance and generates code"
examples = [Interaction("Hello", "print('Hello')"), Interaction("Goodbye", "print('Goodbye')")]
interactions = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
prompt_engine = PromptEngineOverloaded(config, description, examples, interactions)

print (prompt_engine.build_context())