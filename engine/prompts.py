from dataclasses import dataclass
from typing import Callable

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
        
@dataclass()
class Message:
    description: str = None 
    color: int = None       

@dataclass()
class ActionResponse:
    message: str
    public: Message = None

@dataclass()
class Response:
    display_text: str
    action: Callable[..., ActionResponse]
    id: int = 0

    def __str__(self):
        return self.display_text

