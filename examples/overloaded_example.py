from prompt_refresher.prompt_engine import PromptEngine, PromptEngineConfig
from prompt_refresher.model_config import ModelConfig
from prompt_refresher.interaction import Interaction

class PromptEngineOverloaded(PromptEngine):
    def _insert_examples(self):
            """
            Inserts the examples into the context
            """
            if (self.examples != []):
                for example in self.examples:
                    self.context += self.config.start_sequence + "This is an example: " + example.natural_language + self.config.stop_sequence
                    self.context += self.config.newline_operator
                    self.context += example.code + self.config.newline_operator

config = PromptEngineConfig(ModelConfig(max_tokens=50), comment_operator = "###")
description = "This code takes in natural language utterance and generates code This code takes in natural language utterance and generates code"
examples = [Interaction("Hello", "print('Hello')"), Interaction("Goodbye", "print('Goodbye')")]
interactions = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
prompt_engine = PromptEngineOverloaded(config, description, examples, interactions)

print (prompt_engine.build_context())