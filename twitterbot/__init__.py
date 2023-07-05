import uvicorn
from typing import Optional, Union
from fastapi import FastAPI, Request,responses
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


app = FastAPI()

templates = Jinja2Templates(directory="templates")