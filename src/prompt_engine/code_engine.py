from prompt_engine.prompt_engine import PromptEngine, PromptEngineConfig
from prompt_engine.model_config import ModelConfig
from prompt_engine.interaction import Interaction

class CodeEngineConfig(PromptEngineConfig):
    def __init__(self, model_config: ModelConfig = None, description_comment_operator: str = "###", description_comment_close_operator: str = "", newline_operator: str = "\n",
                 comment_operator: str = "##", comment_close_operator: str = "", code_operator: str = "", code_close_operator: str = ""):
        super().__init__(model_config = model_config, description_prefix = description_comment_operator, description_postfix = description_comment_close_operator, newline_operator = newline_operator,
                                input_prefix = comment_operator, input_postfix = comment_close_operator, output_prefix = code_operator, output_postfix = code_close_operator)

class JavascriptCodeEngineConfig(CodeEngineConfig):
    """
    This class provides the configuration for the Javascript Code Engine
    """
    def __init__(self, model_config: ModelConfig = None, description_comment_operator: str = "/*/", description_comment_close_operator: str = "/*/", newline_operator: str = "\n",
                 comment_operator: str = "/*", comment_close_operator: str = "*/", code_operator: str = "", code_close_operator: str = ""):
        super().__init__(model_config = model_config, description_comment_operator = description_comment_operator, description_comment_close_operator = description_comment_close_operator, newline_operator = newline_operator,
                                comment_operator = comment_operator, comment_close_operator = comment_close_operator, code_operator = code_operator, code_close_operator = code_close_operator)

class PythonCodeEngineConfig(CodeEngineConfig):
    """
    This class provides the configuration for the Python Code Engine
    """
    def __init__(self, model_config: ModelConfig = None, description_comment_operator: str = "###", description_comment_close_operator: str = "", newline_operator: str = "\n",
                 comment_operator: str = "##", comment_close_operator: str = "", code_operator: str = "", code_close_operator: str = ""):
        super().__init__(model_config = model_config, description_comment_operator = description_comment_operator, description_comment_close_operator = description_comment_close_operator, newline_operator = newline_operator,
                                comment_operator = comment_operator, comment_close_operator = comment_close_operator, code_operator = code_operator, code_close_operator = code_close_operator)


class CodeEngine(PromptEngine):
    """
    Code Engine provides a PromptEngine to construct nl-to-code prompts for large scale language model inference
    """
    def __init__(self, config: CodeEngineConfig, description: str, examples: list = [], flow_reset_text = "", dialog: list = []):
        super().__init__(config = config, description = description, examples = examples, flow_reset_text = flow_reset_text, dialog = dialog)