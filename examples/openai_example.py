from statistics import mode
from prompt_engine.code_engine import CodeEngine, PythonCodeEngineConfig
from prompt_engine.model_config import ModelConfig
from prompt_engine.interaction import Interaction
import openai

# This is an example to showcase the capabilities of the prompt-engine and how it can be easily integrated
# into OpenAI's API for code generation

# Creating OpenAI configuration
api_key = ""
openai.api_key = api_key

# Creating a new code engine
config = PythonCodeEngineConfig(ModelConfig(max_tokens=1024))
description = "Natural Language Commands to Math Code"
examples = [Interaction("what's 10 plus 18", "print(10 + 18)"), 
            Interaction("what's 10 times 18", "print(10 * 18)")]
code_engine = CodeEngine(config = config, description = description, examples = examples)

# Creating a new readline interface
while True:
    user_query = input("Enter your query: ")
    if (user_query == "exit"):
         break
    codex_query = code_engine.build_prompt(user_query)

    response = openai.Completion.create(engine="code-davinci-002", prompt=codex_query, temperature=0.3, max_tokens=code_engine.config.model_config.max_tokens, stop=[config.input_prefix, config.description_prefix])

    completion_all = response['choices'][0]['text'].strip()
    print (codex_query + completion_all)
    print ("----------------------------------------------------------------------------------------------------------------")

    if (completion_all != ""):
      code_engine.add_interaction(user_query, completion_all)