import os
from bot import bot

os.environ.setdefault("JISHAKU_HIDE", "1")
os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1")

if __name__ == "__main__":
    bot.run()
