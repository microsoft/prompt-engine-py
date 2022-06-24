class Interaction:
    """
    Interaction class is used to store natural natural language and code pairs to be used in the prompt engine
    """
    def __init__(self, input, response):
        self.input = input
        self.response = response