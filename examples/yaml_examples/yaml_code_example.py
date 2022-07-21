from prompt_engine.code_engine import CodeEngine

prompt_engine = CodeEngine()

with open("./examples/yaml_examples/code.yaml") as f:
    prompt_engine.load_yaml(yaml_config=f.read())

print (prompt_engine.build_prompt("what's 10 times 18 mutliplied by 18"))

"""
Output for this example is:

### Natural Language Commands to Math Code

## what's 10 plus 18
console.log(10 + 18)

## what's 10 times 18
console.log(10 * 18)

## what's 18 divided by 10
console.log(10 / 18)

## what's 18 factorial 10
console.log(10 % 18)

## what's 10 times 18 mutliplied by 18

"""

