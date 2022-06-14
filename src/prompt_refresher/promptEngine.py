from prompt_refresher.interaction import Interaction
from prompt_refresher.modelConfig import ModelConfig
from prompt_refresher.prompt import Prompt, Context

class PromptEngineConfig: 
    def __init__(self, modelConfig: ModelConfig = None, commentOperator: str = "#", commentCloseOperator: str = "", newlineOperator: str = "\n", startSequence: str = "##", stopSequence: str = ""):
        self.modelConfig = modelConfig
        self.commentOperator = commentOperator
        self.commentCloseOperator = commentCloseOperator
        self.newlineOperator = newlineOperator
        self.startSequence = startSequence
        self.stopSequence = stopSequence


class PromptEngine:
    def __init__(self, config: PromptEngineConfig, description: str, examples: list = [], dialog: list = []):
        self.config = config
        self.description = description
        self.examples = examples
        self.dialog = dialog

    # Builds the context from the input parameters
    def buildContext(self):
        self.context: str = ""

        if (self.config.modelConfig != None):
            promptEngineConfigMembers = [attr for attr in dir(self.config.modelConfig) if not callable(getattr(self.config.modelConfig, attr)) and not attr.startswith("__")]
            for member in promptEngineConfigMembers:
                self.context += self.config.commentOperator + " " + member + ": " + str(getattr(self.config.modelConfig, member)) + self.config.commentCloseOperator + self.config.newlineOperator
                self.context += self.config.newlineOperator

        if (self.description != ""):
            self.context += self.config.commentOperator + " " + self.description + self.config.newlineOperator + self.config.commentCloseOperator
            self.context += self.config.newlineOperator
        
        if (self.examples != []):
            for example in self.examples:
                self.context += self.config.startSequence + " " + example.naturalLanguage + self.config.stopSequence + self.config.newlineOperator
                self.context += example.code + self.config.newlineOperator
        
        if (self.config.modelConfig != None and self.__assert_token_limit(self.context, self.config.modelConfig.max_tokens)):
            raise Exception("Token limit exceeded, reduce the number of examples or size of description. Alternatively, you may increase the max_tokens in ModelConfig")
        
        if (self.dialog != []):
            for dialog in self.dialog:
                self.context += self.config.startSequence + " " + dialog.naturalLanguage + self.config.stopSequence + self.config.newlineOperator
                self.context += dialog.code + self.config.newlineOperator
        
        if (self.config.modelConfig != None and self.__assert_token_limit(self.context, self.config.modelConfig.max_tokens)):
            self.removeFirstInteraction()
            self.buildContext()

        return self.context

    # Builds the prompt with the given natural language
    def buildPrompt(self, naturalLanguage: str):
        return self.context + self.config.newlineOperator + naturalLanguage

    # Truncates the context when a new prompt is added
    def truncatePrompt(self, prompt: Prompt):
       pass
    
    def addInteraction(self, interaction: Interaction):
        self.dialog.append(interaction)

    def removeLastInteraction(self):
        if (len(self.dialog) > 0):
            self.dialog.pop()
        else:
            raise Exception("No interactions to remove")

    def removeFirstInteraction(self):
        if (len(self.dialog) > 0):
            self.dialog.pop(0)
        else:
            raise Exception("No interactions to remove")
    
    def __assert_token_limit(self, context: str, max_tokens: int):
        if context != "" or context != None:
            numTokens = len(context.split())
            if numTokens > max_tokens:
                return True
            else:
                return False
        else:
            return False
