# main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# transformers imports (no heavy work at import time)
from transformers import pipeline
from transformers.utils.logging import set_verbosity_error
set_verbosity_error()

app = FastAPI()

