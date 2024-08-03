import bot
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def run():
    bot.Run()