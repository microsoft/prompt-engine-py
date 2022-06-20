from prompt_engine.prompt_engine import PromptEngine, PromptEngineConfig
from prompt_engine.model_config import ModelConfig
from prompt_engine.interaction import Interaction

class CodeEngineConfig(PromptEngineConfig):
    def __init__(self, model_config: ModelConfig = None, description_prefix: str = "### ", description_postfix: str = "###", newline_operator: str = "\n",
                 input_prefix: str = "##", input_postfix: str = "", output_prefix: str = "", output_postfix: str = ""):
        super().__init__(model_config = model_config, description_prefix = description_prefix, description_postfix = description_postfix, newline_operator = newline_operator,
                                input_prefix = input_prefix, input_postfix = input_postfix, output_prefix = output_prefix, output_postfix = output_postfix)

class JavaScriptCodeEngineConfig(CodeEngineConfig):
    """
    This class provides the configuration for the Code Engine
    """
    def __init__(self, model_config: ModelConfig = None, description_prefix: str = "/*/", description_postfix: str = "/*/", newline_operator: str = "\n",
                 input_prefix: str = "/*", input_postfix: str = "*/", output_prefix: str = "", output_postfix: str = ""):
        super().__init__(model_config = model_config, description_prefix = description_prefix, description_postfix = description_postfix, newline_operator = newline_operator,
                                input_prefix = input_prefix, input_postfix = input_postfix, output_prefix = output_prefix, output_postfix = output_postfix)

class PythonCodeEngineConfig(CodeEngineConfig):
    """
    This class provides the configuration for the Code Engine
    """
    def __init__(self, model_config: ModelConfig = None, description_prefix: str = "### ", description_postfix: str = "###", newline_operator: str = "\n",
                 input_prefix: str = "##", input_postfix: str = "", output_prefix: str = "", output_postfix: str = ""):
        super().__init__(model_config = model_config, description_prefix = description_prefix, description_postfix = description_postfix, newline_operator = newline_operator,
                                input_prefix = input_prefix, input_postfix = input_postfix, output_prefix = output_prefix, output_postfix = output_postfix)


class CodeEngine(PromptEngine):
    """
    Code Engine provides a PromptEngine to construct nl-to-code prompts for large scale language model inference
    """
    def __init__(self, config: CodeEngineConfig, description: str, examples: list = [], flow_reset_text = "", interactions: list = []):
        super().__init__(config = config, description = description, examples = examples, flow_reset_text = flow_reset_text, interactions = interactions)