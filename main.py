import os

import uvicorn
from fastapi import FastAPI

from routes import auth, jwt

os.popen("node index.js")

app = FastAPI()
app.include_router(auth.router)
app.include_router(jwt.router)

if __name__ == "__main__":
    uvicorn.run(app, port=10002)
