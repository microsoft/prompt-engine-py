from prompt_engine.prompt_engine import PromptEngineConfig
from prompt_engine.interaction import Interaction 
from prompt_engine.model_config import ModelConfig
from prompt_engine.dynamic_prompt_engine import DynamicPromptEngine, PromptBank
import openai

api_key = ""
openai.api_key = api_key

config = PromptEngineConfig(ModelConfig(max_tokens=1024), description_prefix = "###")

description1 = "The following prompts tell you the urgency of a notification"
examples1 = [Interaction("Your flight is going to be delayed! Please check your Delta app for updated schedules", "Urgent"),
    Interaction("Your daughter was just taken to the emergency room. Please call us back immediately.", "Urgent"),
    Interaction("Hey how are you? We should get lunch sometime.", "Low"),
    Interaction("What is the project status? Please send it to me today.", "High"),
    Interaction("Liverpool is now leading in their game vs Aston Villa.", "Medium")]
dynamic_engine = DynamicPromptEngine(openai_key = api_key, config = config, description = description1, examples=examples1, prompt_bank = PromptBank())
del dynamic_engine

description2 = "Extract the monuments from the given text"
examples2 = [Interaction("Can we go to Taj Mahal?", "Taj Mahal"),
Interaction("How old is the Stonehenge?", "Stonehenge"),
Interaction("The Statue of Liberty is such a massive statue, I wonder how they built it", "Statue of Liberty"),
Interaction("What is the name of that big Buddha statue in Asia?", "Big Buddha Statue"),
Interaction("I want to see the Eiffel Tower!", "Eiffel Tower"),
Interaction("Where is The Vatican located in italy?", "The Vatican"),
Interaction("How many steps are there to the top of the Great Pyramid of Giza?", "Great Pyramid of Giza")]
dynamic_engine = DynamicPromptEngine(openai_key = api_key, config = config, description = description2, examples=examples2, prompt_bank = PromptBank())
del dynamic_engine


description = "I want to classify the importance for the notifications"
flow_reset_text = "Ignore the previous queries, start afresh"
dynamic_engine = DynamicPromptEngine(openai_key = api_key, config = config, description = description, flow_reset_text = flow_reset_text, prompt_bank = PromptBank())

while True:
    user_query = input("Enter your query: ")
    if (user_query == "exit"):
         break
    codex_query = dynamic_engine.build_prompt(user_query)

    response = openai.Completion.create(engine="code-davinci-002", 
                                        prompt=codex_query, 
                                        temperature=0.3, 
                                        max_tokens=dynamic_engine.config.model_config.max_tokens, 
                                        stop=[dynamic_engine.config.newline_operator])

    completion_all = response['choices'][0]['text'].strip()
    print (codex_query+completion_all)
    print ("----------------------------------------------------------------------------------------------------------------")

    if (completion_all != ""):
      dynamic_engine.add_interaction(user_query, completion_all)