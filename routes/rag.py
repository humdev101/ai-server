from fastapi import APIRouter,Response
from ..helpers import embeddings
from pydantic import BaseModel

class Body(BaseModel):
    inputFileName:str
    outputFolderName:str

class RagRetrieval(BaseModel):
    query: str
    vector_store_name: str
    search_type: str
    search_kwargs: object
    llmModel: str

router = APIRouter(
    prefix="/rag"
)

@router.post("/generateEmbeddingsFromTextFile")
async def generateEmbeddingsTxtFile(body:Body,response:Response):
    print(body)
    generatedResponse = embeddings.generateEmbeddingsFromTextFile(body.inputFileName,body.outputFolderName)
    response.status_code=generatedResponse.httpCode
    return generatedResponse

@router.post("/retrieveRagDataFromVectorStore")
async def retrieveRagData(body:RagRetrieval,response:Response):
    print(body)
    generatedResponse = embeddings.retrieveDataFromEmbeddings(body.query,body.vector_store_name,body.search_type,body.search_kwargs)
    response.status_code=generatedResponse.httpCode
    return generatedResponse

@router.post("/generateResponseFromRag")
async def gpt4ominigeneration(body:RagRetrieval,response:Response):
    print(body)
    generatedResponse = embeddings.chatgptPlusRagRetriever(body.query,body.vector_store_name,body.search_type,body.search_kwargs,body.llmModel)
    response.status_code=generatedResponse.httpCode
    return generatedResponse

