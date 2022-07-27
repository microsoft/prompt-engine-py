class ModelConfig:
    """
    Interaction class is used to store the model config to be used in the prompt engine
    """
    def __init__(self, max_tokens, **kwargs):
        self.max_tokens = max_tokens
        self.__dict__.update(kwargs)