from prompt_engine.chat_engine import ChatEngine

prompt_engine = ChatEngine()

with open("./examples/yaml_examples/chat.yaml") as f:
    prompt_engine.load_yaml(yaml_config=f.read())

print (prompt_engine.build_context())

"""
Output for this example is:

What is the possibility of an event happening?

Abhishek: Roam around Mars
Bot: This will be possible in a couple years

Abhishek: Drive a car
Bot: This is possible after you get a learner drivers license

Starting a new conversation

Abhishek: Drink water
Bot: Uhm...You don't do that 8 times a day?

Abhishek: Walk on air
Bot: For that you'll need a special device

"""