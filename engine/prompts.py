class Prompt:
    def __init__(self, display_text, responses, type = 2):
        """
        type: 1 (Yes/No)
              2 (Multiple choice)
        """
        self.type = type
        self.display_text = display_text
        self.responses = responses
    
    def __str__(self):
        return self.display_text

class Response:
    def __init__(self, display_text, actions):
        self.display_text = display_text
        self.actions = actions

class Action:
    def execute(self):
        pass