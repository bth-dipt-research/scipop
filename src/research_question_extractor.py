import pickle
import csv
import time
from datetime import datetime
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.documents import Document
from typing_extensions import Annotated, List, TypedDict
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential
)
from keys import OPENAI_KEY


class ResearchQuestion(TypedDict):
    """Research Question extracted from a paper"""

    explicit: Annotated[bool,..., "Explicitly stated research question"]
    research_question: Annotated[str, ..., "Research question"]

class ResearchQuestions(TypedDict):
    research_questions: List[ResearchQuestion]

def pdf_to_text(pdf_file: Path):
    loader = PyPDFLoader(pdf_file)
    pages = loader.load()
    return ' '.join(page.page_content for page in pages)

def get_file_names(path: Path):
    directory = Path(path)
    return [file for file in directory.iterdir() if file.is_file()]

@retry(wait=wait_random_exponential(min=10, max=60), stop=stop_after_attempt(5))
def completion_with_backoff(messages):
    return llm.invoke(messages)

data_dir = Path("../data/dipt_papers_2024/")

paper_dir = data_dir / Path("pdfs")

output_dir = data_dir / Path("research_questions")
output_dir.mkdir(parents=True, exist_ok=True)

model = "gpt-4o-mini"
temperature = 0.3

llm = ChatOpenAI(
    model = model,
    temperature = temperature,
    api_key = OPENAI_KEY
).with_structured_output(ResearchQuestions, include_raw=True)

instructions = """This GPT is a research assistant focused on analyzing scientific articles to identify and extract explicitly stated research questions verbatim from the text. If no explicit research questions are found, the GPT will infer potential research questions based on the content provided. The output shall be structured according to the provided format. The field "explicit" shall be used to indicate explicit (TRUE) or inferred (FALSE) research questions. If no explicit or inferred research questions can be generated, the result shall be empty. This behavior is strictly enforced in the output to maintain clarity and consistency.
"""

files = get_file_names(paper_dir)

results = []

for file_name in files:
    document = Document(
        page_content = pdf_to_text(file_name),
        metadata = {
            "paper_id": file_name.stem
        }
    )

    paper_id = document.metadata['paper_id']

    print(f'Analyzing {paper_id}')

    messages = [
        SystemMessage(
            content = instructions
        ),
        HumanMessage(
            content = document.page_content
        )
    ]

    response = completion_with_backoff(messages)

    results.append(
        {
            "paper_id": paper_id,
            "response": response
        }
    )

extraction = {
    "parameters": {
        "paper_directory": str(paper_dir.resolve()),
        "model": model,
        "temperature": temperature
    },
    "instructions": instructions,
    "results": results
}

with open(output_dir / Path("extraction.pkl"), "wb") as file:
    pickle.dump(extraction, file)

with open(output_dir / Path("results.csv"), "w") as file:
    writer = csv.writer(file)
    writer.writerow(["paper_id", "research_question", "explicit"])

    for result in extraction["results"]:
        research_questions = result['response']['parsed']['research_questions']
        for research_question in research_questions:
            row = []
            row.append(result['paper_id'])
            row.append(research_question['research_question'])
            row.append(research_question['explicit'])
            writer.writerow(row)
