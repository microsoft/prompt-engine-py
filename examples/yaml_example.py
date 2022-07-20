from prompt_engine.code_engine import PromptEngine

prompt_engine = PromptEngine(yaml_file=r'C:\Users\amasand\Downloads\Github\prompt-engine-python\examples\test.yaml')

print (prompt_engine.build_context())

"""
Output of this example is:

Hello This is the description !

> Roam around Mars
This will be possible in a couple years

> Drive a car
This is possible after you get a learner drivers license

Hello This is the flow reset text !

> Drink water
Uhm...You don't do that 8 times a day?

> Walk on air
For that you'll need a special device

"""