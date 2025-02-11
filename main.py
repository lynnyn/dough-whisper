import uvicorn
from fastapi import FastAPI
from routes import doughs

app = FastAPI()
app.include_router(doughs.router, prefix="/doughs", tags=["doughs"])
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
