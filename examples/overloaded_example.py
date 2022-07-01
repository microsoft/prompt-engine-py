from prompt_engine.prompt_engine import PromptEngine, PromptEngineConfig
from prompt_engine.model_config import ModelConfig
from prompt_engine.interaction import Interaction

class PromptEngineOverloaded(PromptEngine):
    def _insert_examples(self, context: str = "", user_input: str = ""):
        """
        Inserts the examples into the context
        """
        temp_examples_text = ""
        if (self.examples != []):
            for example in self.examples:

                #Original: temp_example_text = self.config.input_prefix + example.input + self.config.input_postfix + self.config.newline_operator
                #Replacing input_prefix and input_postfix with static values
                temp_example_text = "Example: " + example.input + self.config.newline_operator

                #Original: temp_example_text += self.config.output_prefix +  example.response + self.config.output_postfix +  self.config.newline_operator*2
                #Replacing output_prefix and output_postfix with static values
                temp_example_text += "Answer: " + example.response + self.config.newline_operator*2

                temp_examples_text += temp_example_text

            context += temp_examples_text
        
        return context

config = PromptEngineConfig(ModelConfig(max_tokens=1024), description_prefix = "->")
description = "I want to speak with a bot which replies in under 20 words each time"
examples = [Interaction("Hi", "I'm a chatbot. I can chat with you about anything you'd like."), 
            Interaction("Can you help me with the size of the universe?", "Sure. The universe is estimated to be around 93 billion light years in diameter.")]
dialog = [Interaction("What is the size of an SUV in general?", "An SUV typically ranges from 16 to 20 feet long."), 
        Interaction("What is the maximum speed an SUV from a performance brand can achieve?", "Some performance SUVs can reach speeds over 150mph.")]
prompt_engine = PromptEngineOverloaded(config = config, description = description, examples = examples, dialog = dialog)

print (prompt_engine.build_prompt("What's the most popular SUV in the world?"))


"""
Output of this example is:

-> I want to speak with a bot which replies in under 20 words each time                                                                                                                  
Example: Hi
Answer: I'm a chatbot. I can chat with you about anything you'd like.

Example: Can you help me with the size of the universe?
Answer: Sure. The universe is estimated to be around 93 billion light years in diameter.

What is the size of an SUV in general?
An SUV typically ranges from 16 to 20 feet long.

What is the maximum speed an SUV from a performance brand can achieve?
Some performance SUVs can reach speeds over 150mph.

What's the most popular SUV in the world?

"""