from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "ok",
        "app": "p2p-x",
        "message": "Fly.io deployment successful!"
    }
