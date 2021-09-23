from dataclasses import dataclass


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


class Action:
    def execute(self):
        pass

@dataclass()
class Response:
    display_text: str
    action: Action

@dataclass()
class ActionResponse:
    message: str
    private: str = None