import requests
from routers import main
from fastapi import FastAPI
from uvicorn import run as run_uvicorn
from yaml import dump

if __name__ == "__main__":
    open("./knowledge/mapping.yml","w")
    
    app = FastAPI()

    app.include_router(main)
    
    run_uvicorn(app, port=5000, log_level="info", host="0.0.0.0")