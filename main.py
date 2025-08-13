from typing import Any
from fastapi import Body, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
import os
from langchain_openai import OpenAIEmbeddings

load_dotenv()

index_name = "recipes"

pinecone_api_key = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=pinecone_api_key)

index = pc.Index(index_name)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1024)

vectorstore = PineconeVectorStore.from_existing_index(
    index_name,
    embeddings,
)

app = FastAPI(
    title="ChefGPT. The best provider of Indian recipes in the world.",
    description="Give ChefGPT the name of an ingredient and it will give you multiple recipes to use that ingredient on in return.",
    servers=[
        {
            "url": "https://volunteers-africa-constitutional-rider.trycloudflare.com"
        }
    ]
)


class Document(BaseModel):
    page_content: str


@app.get(
    "/recipes",
    summary="Returns a list of recipes.",
    description="Upon receiving an ingredient, this endpoint will return a list of recipes that contain that ingredient.",
    response_description="A Document object that contains the recipe and preparation instructions",
    response_model=list[Document],
    openapi_extra={
        "x-openai-isConsequential": False
    }
)
def get_recipe(ingredient: str):
    docs = vectorstore.similarity_search(ingredient)
    return docs


# user_token_db = {
#     "ABCDEF": "haein"
# }


# @app.get(
#     "/authorize",
#     response_class=HTMLResponse
# )
# def handle_authorize(client_id: str, redirect_uri: str, state: str):
#     print(
#         client_id,
#         redirect_uri,
#         state,
#     )
#     return f"""
#     <html>
#         <head>
#             <title>Nicolacus Maximus Log In</title>
#         </head>
#         <body>
#             <h1>Log Into Nicolacus Maximus</h1>
#             <a href="{redirect_uri}?code=ABCDEF&state={state}">Authorize Nicolacus Maximus GPT</a>
#         </body>
#     </html>
#     """


# @app.post("/token")
# def handle_token(code=Form(...)):
#     return {
#         "access_token": user_token_db[code]
#     }

# Give me a indian recipe that uses tofu.
