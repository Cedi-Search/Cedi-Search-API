from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from json import load
from rank_bm25 import BM25Okapi


app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


with open("index.json") as index_file:
    corpus = load(index_file)

tokenized_corpus = [doc.lower().split(" ") for doc in corpus]

bm25 = BM25Okapi(tokenized_corpus)


@app.get("/")
def read_root(query: str = Query()):

    tokenized_query = query.split(" ")

    suggestions = bm25.get_top_n(tokenized_query, corpus, n=10)

    return suggestions
