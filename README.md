# Prompt-Refresher

This package provides an easy and reusable interface to build prompts for large scale language models (LLMs). 

## Requirements
* [Python 3.7.1+](https://www.python.org/downloads/)  

## Install

```bash
pip install prompt_refresher
```

## Simple Demo

### Code
```python
from prompt_refresher.promptEngine import PromptEngine, PromptEngineConfig
from prompt_refresher.modelConfig import ModelConfig
from prompt_refresher.interaction import Interaction

config = PromptEngineConfig(ModelConfig(max_tokens=50), commentOperator = "###")
description = "This code takes in natural language utterance and generates code This code takes in natural language utterance and generates code"
examples = [Interaction("Hello", "print('Hello')"), Interaction("Goodbye", "print('Goodbye')")]
interactions = [Interaction("Hi", "print('Hi')"), Interaction("Bye", "print('Bye')")]
promptEngine = PromptEngine(config, description, examples, interactions)

print (promptEngine.buildContext())
```

### Output
```
### max_tokens: 50

### This code takes in natural language utterance and generates code This code takes in natural language utterance and generates code

## Hello
print('Hello')
## Goodbye
print('Goodbye')
## Hi
print('Hi')
## Bye
print('Bye')
```


## Prompt Engineering and Context Files

To generate meaningful output output out of a large scale language model, you need to provide it with an equally descriptive prompt to coax the intended behaviour. 

A good way to achieve that is by providing helpful examples to the LLM in the form of query-answer interaction pairs. 

This is an example from the [Codex-CLI](https://github.com/microsoft/Codex-CLI) library following the above principle
```powershell
# what's the weather in New York?
(Invoke-WebRequest -uri "wttr.in/NewYork").Content

# make a git ignore with node modules and src in it
"node_modules
src" | Out-File .gitignore

# open it in notepad
notepad .gitignore
```

## Available Functions

These are the prebuilt functions that are provided by the prompt_refresher library

| Command | Parameters | Description |
|--|--|--|
| `buildContext` | None | Constructs and return the context with parameters provided to the Prompt Engine |
| `buildPrompt` | Prompt: str | Uses the context constructed by the build context function and generates a prompt to query  |
| `truncatePrompt` | max_tokens: int |Truncates the prompt to the max_tokens limit|
| `addInteraction` | interaction: Interaction(naturalLanguage: str, code: str) | Adds the given natural language - code interaction to the interactionss |
| `removeFirstInteraction` | None | Removes the first/most historical interaction added to the interactionss |
| `removeLastInteraction` | None | Removes the last interaction added to the interactionss |

## Adding more info to your contexts

This project comes pre-loaded with a single technique for making contexts. That doesn't mean its the best technique or the only one you should use.

Beyond these, you can build your own contexts to coax other behaviors out of the model. To change the prompt making behaviour or adding more info to the context you can inherit the PromptEngine class and change the behaviour for making the prompts. For example, 

If you want to change the behaviour for adding examples to the model:
```python
class PromptEngineOverloaded(PromptEngine):
    def _insert_examples(self):
            """
            Inserts the examples into the context
            """
            if (self.examples != []):
                for example in self.examples:
                    self.context += self.config.startSequence + "This is an example: " + example.naturalLanguage + self.config.stopSequence
                    self.context += self.config.newlineOperator
                    self.context += example.code + self.config.newlineOperator
.
.
.

pr = PromptEngineOverloaded(...)
pr.buildContext()

```
The Prompt Engine will now use the updated logic of the insert examples logic for building the context.

For in-depth look into all the functions available, please have a look at the [PromptEngine](https://github.com/amasandMS/Prompt-Refresher/blob/main/src/prompt_refresher/promptEngine.py) class. 
