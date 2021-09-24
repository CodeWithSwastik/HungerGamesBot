from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from .battle import Battle

@dataclass
class Prompt:
    """
    type:   1 (Yes/No)
            2 (Multiple choice)
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
    battle: Battle = None

@dataclass
class Response:
    display_text: str
    emoji: str = None
    action: Callable[..., ActionResponse] = lambda: ActionResponse('Default')

    def __str__(self):
        return self.display_text

