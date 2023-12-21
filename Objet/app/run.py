from random import randint
from Object import Object
from fastapi import FastAPI
from uvicorn import run as run_uvicorn
from routers import main

if __name__ == "__main__":
    objects = []
    max = randint(1,5)
    for i in range(max):
        objects.append(Object())

    for o in objects:
        if isinstance(o, Object):
            o.start()

    app = FastAPI()

    app.include_router(main)
    
    run_uvicorn(app, port=8000, log_level="info", host="0.0.0.0")