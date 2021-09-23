from dataclasses import dataclass
from typing import Callable

@dataclass
class Prompt:
    """
    type:   1 (Yes/No)
            2 (Multiple choice)
            3 (Battle)
    """
    display_text: str
    responses: list
    type: int = 2
    delay: int = None

    def __str__(self):
        return self.display_text
        
@dataclass
class Message:
    description: str = None 
    color: int = None       

@dataclass
class ActionResponse:
    message: str
    public: Message = None
    followup: Prompt = None

@dataclass
class Response:
    display_text: str
    action: Callable[..., ActionResponse]
    id: int = 0

    def __str__(self):
        return self.display_text

