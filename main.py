import os

import uvicorn
from fastapi import FastAPI

os.popen("node index.js")

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, port=10002)
