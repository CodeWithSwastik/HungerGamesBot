import os

try:
    from dotenv import load_dotenv
except ImportError:
    pass
else:
    load_dotenv()


class Config:
    def __init__(self):
        self.bot_token = os.getenv("TOKEN")
        self.default_prefix = os.getenv("PREFIX", "h!")
        self.version = "0.0.1"
