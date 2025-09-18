# # main.py
# from fastapi import FastAPI, Request
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import JSONResponse, HTMLResponse
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import uvicorn

# # transformers imports (no heavy work at import time)
# from transformers import pipeline
# from transformers.utils.logging import set_verbosity_error
# set_verbosity_error()

# app = FastAPI()

# # allow the simple UI to call the API (adjust origins for production)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# templates = Jinja2Templates(directory="templates")

# # Globals that will hold the pipelines (initialized at startup)
# summarization_pipeline = None
# refinement_pipeline = None
# qa_pipeline = None

# class SummarizeRequest(BaseModel):
#     text: str
#     length: str = "medium"

# class QARequest(BaseModel):
#     question: str
#     context: str

# def _get_length_params(length: str):
#     length = (length or "medium").lower()
#     if length == "short":
#         return {"max_length": 60, "min_length": 20}
#     if length == "long":
#         return {"max_length": 300, "min_length": 120}
#     return {"max_length": 150, "min_length": 60}

# @app.on_event("startup")
# async def load_models():
#     """
#     Load heavy models here — this runs in the server process after import,
#     avoiding multiprocessing spawn/import issues on Windows.
#     """
#     global summarization_pipeline, refinement_pipeline, qa_pipeline
#     print("Loading models (this may take a while)...")
#     # You can change device argument if you have GPU: device=0
#     summarization_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")
#     refinement_pipeline = pipeline("summarization", model="facebook/bart-large")
#     qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")
#     print("Models loaded.")

# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.post("/api/summarize")
# async def summarize(req: SummarizeRequest):
#     text = req.text
#     params = _get_length_params(req.length)

#     if summarization_pipeline is None:
#         return JSONResponse({"error": "models not loaded yet"}, status_code=503)

#     try:
#         first = summarization_pipeline(text, **params)
#         first_summary = first[0]["summary_text"]
#     except Exception as e:
#         return JSONResponse({"error": f"summarization failed: {e}"}, status_code=500)

#     try:
#         refined = refinement_pipeline(first_summary, **params)
#         refined_summary = refined[0]["summary_text"]
#     except Exception:
#         refined_summary = first_summary

#     return {"summary": refined_summary}

# @app.post("/api/qa")
# async def answer_qa(req: QARequest):
#     if qa_pipeline is None:
#         return JSONResponse({"error": "models not loaded yet"}, status_code=503)
#     try:
#         out = qa_pipeline({"question": req.question, "context": req.context})
#         return {"answer": out.get("answer"), "score": out.get("score")}
#     except Exception as e:
#         return JSONResponse({"error": f"qa failed: {e}"}, status_code=500)

# if __name__ == "__main__":
#     # run via python main.py (not required if you run via `uvicorn main:app --reload`)
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
