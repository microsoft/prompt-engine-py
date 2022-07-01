from prompt_engine.code_engine import CodeEngine, PythonCodeEngineConfig
from prompt_engine.model_config import ModelConfig
from prompt_engine.interaction import Interaction

config = PythonCodeEngineConfig(ModelConfig(max_tokens=1024))
description = "Natural Language Commands to JavaScript Math Code. The code should log the result of the command to the console."
examples = [Interaction("what's 10 plus 18", "print(10 + 18)"), Interaction("what's 10 times 18", "print(10 * 18)")]
dialog = [Interaction("what's 10 to the power of 18", "print (10 ** 18)")]
code_engine = CodeEngine(config = config, description = description, examples = examples, dialog = dialog)

print (code_engine.build_prompt("What's 1018 times the ninth power of four?"))

"""
Output of this example is:

### Natural Language Commands to JavaScript Math Code. The code should log the result of the command to the console.

## what's 10 plus 18
print(10 + 18)

## what's 10 times 18
print(10 * 18)

## what's 10 to the power of 18
print (10 ** 18)

## What's 1018 times the ninth power of four?

"""