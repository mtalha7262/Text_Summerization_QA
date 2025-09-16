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

summary_template = PromptTemplate.from_template("Summarize the following text in a {length} way :\n\n{text}\n\nSummary:")

summarization_chain = summary_template | summerizer | refiner

text_to_summarize = input("Enter text to summarize: \n")
length = input("Enter summary length (short/medium/long): \n")

summary = summarization_chain.invoke({"text": text_to_summarize, "length": length})

print("\n* **Generated Summary:**\n")
print(summary)