from prompt_engine.code_engine import PromptEngine

prompt_engine = PromptEngine(yaml_file='test.yaml')

print (prompt_engine.build_context())

"""
Output of this example is:

>> What is the possibility of an event happening? !

Human: Roam around Mars
Bot: This will be possible in a couple years

Human: Drive a car
Bot: This is possible after you get a learner drivers license

>> Starting a new conversation !

Human: Drink water
Bot: Uhm...You don't do that 8 times a day?

Human: Walk on air
Bot: For that you'll need a special device

"""