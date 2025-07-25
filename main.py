import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI,Response,status
from pydantic import BaseModel
from .models.response import APIResponse
from .llms.llmSelector import getLLMFromModelName
from .routes import rag,ai,analysis,coinanalysis,mobile,collection
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .agents.reactAgent import get_agent_executor
from .helpers import prompts

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")

origins = [
    "https://humdev101.com"
    "http://localhost",
    "http://localhost:3000", 
    "http://localhost:4000",
    "http://localhost:4001",
    "http://localhost:3001"
    "http://humdev101.com",
    "https://humdev101.com" # If you're using React/Vue/etc
    "https://www.humdev101.com",
    "http://humdev101.com",
    "https://api.humdev101.com",
    "https://ai.humdev101.com"
]

class Body(BaseModel):
    query: str
    llmModel:str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Can also be ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Allow all headers
)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.post("/ask")
async def askQuestion(body:Body,response:Response):
    try:
        agent_executor = get_agent_executor(body.llmModel)
        if not agent_executor:
            apiResponse = APIResponse(status.HTTP_500_INTERNAL_SERVER_ERROR,"Response recieved from get_agent_executor is None",{})
            print(apiResponse.data)
            response.status_code = apiResponse.httpCode
            return apiResponse
        else:
            agentResponse = agent_executor.invoke({"input":body.query})
            print(agentResponse)
            apiResponse = APIResponse(status.HTTP_200_OK,"Successfully Generated Response",agentResponse)
            return apiResponse
    except Exception as e:
        print("Error " + str(e))
        apiResponse = APIResponse(status.HTTP_500_INTERNAL_SERVER_ERROR,"Unexpected Error occured",{})
        response.status_code = apiResponse.httpCode
        return apiResponse
    
@app.post("/query")
async def askQuery(body:Body,response:Response):
    try:
        llm = getLLMFromModelName(body.llmModel)
        if not llm:
            apiResponse = APIResponse(status.HTTP_500_INTERNAL_SERVER_ERROR,"Response recieved from LLM is None",{})
            response.status_code = apiResponse.httpCode
            return apiResponse
        else:
            llmResponse = llm.invoke(body.query)
            print(f"LLM Response: {llmResponse}")
            if body.llmModel=="gpt-4o-mini" or body.llmModel=="gemini-1.5-flash" or body.llmModel=="gemini-2.0-flash":
                llmResponse = llmResponse.content
            apiResponse = APIResponse(status.HTTP_200_OK,"Successfully Generated Response",llmResponse)
            return apiResponse
    except Exception as e:
        print(f"Error occured inside askQuery {e}")
        apiResponse = APIResponse(status.HTTP_500_INTERNAL_SERVER_ERROR,"Unexpected Error occured",{})
        response.status_code = apiResponse.httpCode
        return apiResponse


@app.get("/")
async def root():
    return {"message": "server started on port 8000"}

app.include_router(rag.router)
app.include_router(ai.router)
app.include_router(analysis.router)
app.include_router(coinanalysis.router)
app.include_router(mobile.router)
app.include_router(collection.router)