class Interaction:
    """
    Interaction class is used to store natural natural language and code pairs to be used in the prompt engine
    """
    def __init__(self, natural_language, code):
        self.natural_language = natural_language
        self.code = code