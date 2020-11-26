# import database
from fastapi import FastAPI, Path, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")  # methodとendpointの指定
async def hello():
    return {"text": "hello world!"}


@app.get("/validation/{path}")
async def validation(
    string: str = Query(None, min_length=2, max_length=5, regex=r"[a-c]+."),
    integer: int = Query(..., gt=1, le=3),  # required
    alias_query: str = Query("default", alias="alias-query"),
    path: int = Path(10),
):
    return {
        "string": string,
        "integer": integer,
        "alias-query": alias_query,
        "path": path,
    }
