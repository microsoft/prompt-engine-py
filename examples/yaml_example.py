from prompt_engine.code_engine import PromptEngine

prompt_engine = PromptEngine(yaml_file='test.yaml')

print (prompt_engine.build_context())

"""
Output of this example is:

>> What is the possibility of an event happening? !

> Roam around Mars
This will be possible in a couple years

> Drive a car
This is possible after you get a learner drivers license

>> Starting a new conversation !

> Drink water
Uhm...You don't do that 8 times a day?

> Walk on air
For that you'll need a special device

"""