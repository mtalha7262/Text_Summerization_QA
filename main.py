from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers.utils.logging import set_verbosity_error
set_verbosity_error()

summarization_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")
summerizer = HuggingFacePipeline(pipeline=summarization_pipeline)

refinement_pipeline = pipeline(task="summarization", model="facebook/bart-large")
refiner = HuggingFacePipeline(pipeline=refinement_pipeline)

qa_pipeline = pipeline(task="question-answering", model="deepset/roberta-base-squad2")
qa = HuggingFacePipeline(pipeline=qa_pipeline)