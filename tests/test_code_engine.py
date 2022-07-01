from src.prompt_engine.code_engine import CodeEngine, PythonCodeEngineConfig
from src.prompt_engine.model_config import ModelConfig
from src.prompt_engine.interaction import Interaction

def test_pass():
    config = PythonCodeEngineConfig(ModelConfig(max_tokens=1024))
    description = "Convert the given natural language to code"
    examples = [Interaction("open window", "executeCommand.open('window')"), Interaction("show window", "executeCommand.show('window')")]
    dialog = [Interaction("hide window", "executeCommand.hide('window')"), Interaction("hide sidebar", "executeCommand.hide('sidebar')")]
    code_engine = CodeEngine(config=config, description=description, examples=examples, dialog=dialog)
    assert code_engine.build_context() == "### Convert the given natural language to code\n\n## open window\nexecuteCommand.open('window')\n\n## show window\nexecuteCommand.show('window')\n\n## hide window\nexecuteCommand.hide('window')\n\n## hide sidebar\nexecuteCommand.hide('sidebar')\n\n"