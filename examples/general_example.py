from prompt_engine.prompt_engine import PromptEngine, PromptEngineConfig
from prompt_engine.model_config import ModelConfig
from prompt_engine.interaction import Interaction

config = PromptEngineConfig(ModelConfig(max_tokens=1024), description_prefix = "->")
description = "I want to speak with a bot which replies in under 20 words each time"
examples = [Interaction("Hi", "I'm a chatbot. I can chat with you about anything you'd like."), 
            Interaction("Can you help me with the size of the universe?", "Sure. The universe is estimated to be around 93 billion light years in diameter.")]
flow_reset_text = "Forget the earlier conversation and start afresh"
dialog = [Interaction("What is the size of an SUV in general?", "An SUV typically ranges from 16 to 20 feet long."), 
        Interaction("What is the maximum speed an SUV from a performance brand can achieve?", "Some performance SUVs can reach speeds over 150mph.")]
prompt_engine = PromptEngine(config = config, description = description, examples = examples, flow_reset_text = flow_reset_text, dialog = dialog)

print (prompt_engine.build_context())

"""
Output of this example is:

-> I want to speak with a bot which replies in under 20 words each time

Hi
I'm a chatbot. I can chat with you about anything you'd like.

Can you help me with the size of the universe?
Sure. The universe is estimated to be around 93 billion light years in diameter.

-> Forget the earlier conversation and start afresh

What is the size of an SUV in general?
An SUV typically ranges from 16 to 20 feet long.

What is the maximum speed an SUV from a performance brand can achieve?
Some performance SUVs can reach speeds over 150mph.

"""

config = PromptEngineConfig(ModelConfig(max_tokens=1024), input_prefix = "->", output_postfix="<-", )
description = "I want to speak with a bot which replies in under 20 words each time"
prompt_engine = PromptEngine(config, description)

prompt_engine.add_example("Hi", "I'm a chatbot. I can chat with you about anything you'd like.")
prompt_engine.add_example("Can you help me with the size of the universe?", "Sure. The universe is estimated to be around 93 billion light years in diameter.")

prompt_engine.add_interaction("What is a light year?", "A light year is the distance that light can travel in one year.")

print(prompt_engine.build_prompt("Can any spacecraft travel at the speed of light?"))

"""
Output of this example is:

I want to speak with a bot which replies in under 20 words each time

-> Hi
I'm a chatbot. I can chat with you about anything you'd like. <-

-> Can you help me with the size of the universe?
Sure. The universe is estimated to be around 93 billion light years in diameter. <-

-> What is a light year?
A light year is the distance that light can travel in one year. <-

-> Can any spacecraft travel at the speed of light?

"""

print (prompt_engine.reset_context())

"""
Output after resetting the context but without any prompt:

I want to speak with a bot which replies in under 20 words each time

-> Hi
I'm a chatbot. I can chat with you about anything you'd like. <-

-> Can you help me with the size of the universe?
Sure. The universe is estimated to be around 93 billion light years in diameter. <-

"""