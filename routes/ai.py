from fastapi import APIRouter,Response
from pydantic import BaseModel
from ..models.response import APIResponse
from ..agents.simpleConversational import chatWithAgentsConversational
from ..helpers.prompts import generalCryptoAnalysisFull,saveAnalysis,getCoinCryptoAnalsysFunc
from datetime import datetime, timezone, timedelta
from .analysis import stack_analysis
from ..service.coinAnalysisService import stack_analysis_coin_analysis,addAnalysis

router = APIRouter(
    prefix="/ai"
)

# Route to get all , models , tools, llm
class Body(BaseModel):
    type: str


class LLMBody(BaseModel):
    llmModel: str

class CoinAnalysisBody(BaseModel):
    symbol: str
    timeframe: str
    interval: str
    llmModel: str

class ConversationBody(BaseModel):
    messagesList: list
    llmModel: str


allData = [
      {
        "image":"/static/images/deepseekRound.png",
        "name": "DeepSeek 7b",
        "description": "Introducing DeepSeek LLM, an advanced language model comprising 7 billion parameters. It has been trained from scratch on a vast dataset of 2 trillion tokens in both English and Chinese. This model is designed to excel in various tasks, including coding, math, and reasoning, making it a versatile tool for developers and researchers alike.",
        "type": "llm",
        "modelName": "deepseek-llm:7b",
        "id":"6"
    },
    #   {
    #     "image":"/static/images/researcher.svg",
    #     "name": "Wiki Research Agent",
    #     "description": "Introducing DeepSeek LLM, an advanced language model comprising 7 billion parameters. It has been trained from scratch on a vast dataset of 2 trillion tokens in both English and Chinese. This model is designed to excel in various tasks, including coding, math, and reasoning, making it a versatile tool for developers and researchers alike.",
    #     "type": "agent",
    #     "modelName": "deepseek-llm:7b",
    #     "id":"6"
    # },
    #  {
    #     "image":"/static/images/web3Agent.png",
    #     "name": "Web3 AI Agent",
    #     "description": "Web3-AI-Agent is an intelligent AI-driven agent that queries real-time blockchain data using predefined tools. It follows the Reason + Action (ReAct) model, allowing it to analyze user queries, determine the right tool, fetch data, validate accuracy, and iterate until it produces a precise response.",
    #     "type": "agent",
    #     "modelName": "web3-ai-agent",
    #     "id":"5"
    # },
     {
        "image":"/static/images/qwenSquare.jpeg",
        "name": "qwen2.5",
        "description": "Qwen2.5 is the large language model series developed by Qwen team, Alibaba Cloud. ",
        "type": "llm",
        "modelName": "qwen2.5",
        "id":"1"
    },
     {
        "image":"/static/images/phi4.png",
        "name": "Phi-4",
        "description": "Phi-4 is a 14B parameter, state-of-the-art open model built upon a blend of synthetic datasets, data from filtered public domain websites, and acquired academic books and Q&A datasets.",
        "type": "llm",
        "modelName": "phi4",
        "id":"6"
    },
    #   {
    #     "image":"/static/images/cryptoAnalyst.webp",
    #     "name": "Crypto Analysis Agent",
    #     "description": "Introducing DeepSeek LLM, an advanced language model comprising 7 billion parameters. It has been trained from scratch on a vast dataset of 2 trillion tokens in both English and Chinese. This model is designed to excel in various tasks, including coding, math, and reasoning, making it a versatile tool for developers and researchers alike.",
    #     "type": "agent",
    #     "modelName": "crypto-analyst",
    #     "id":"6"
    # },
    {
        "image":"/static/images/mistral.jpeg",
        "name": "Mistral 7b",
        "description": "Mistral 7B is a dense transformer model with 7 billion parameters, designed for high performance in various natural language processing tasks, including text generation, comprehension, and classification. It is known for its efficiency and effectiveness in handling complex language tasks.",
        "type": "llm",
        "modelName": "mistral",
        "id":"1"
    },
    {
        "image":"/static/images/geminiSquare.png",
        "name": "Gemini 2.0 Flash",
        "description": "Gemini 2.0 Flash is Google's latest generally available model in the Gemini family, designed for everyday tasks and features enhanced performance, including multimodal capabilities, a 1 million token context window, and native tool use, with faster speeds and improved quality compared to its predecessors. ",
        "type": "llm",
        "modelName": "gemini-2.0-flash",
        "id":"1"
    },
      {
        "image":"/static/images/chatgptSquare.png",
        "name": "ChatGPT 4o-mini",
        "description": "GPT‑4o mini surpasses GPT‑3.5 Turbo and other small models on academic benchmarks across both textual intelligence and multimodal reasoning, and supports the same range of languages as GPT‑4o. It also demonstrates strong performance in function calling, which can enable developers to build applications that fetch data or take actions with external systems, and improved long-context performance compared to GPT‑3.5 Turbo.",
        "type": "llm",
        "modelName": "gpt-4o-mini",
        "id":"3"
    },
     {
        "image":"/static/images/llamaSquare.png",
        "name": "LLama 3:8b",
        "description": "Llama 3 is a large language model developed by Meta AI, positioned as a competitor to models like OpenAI's GPT series. It's designed to be a highly capable text-based AI, similar to other large language models, but with notable improvements and unique features.",
        "type": "llm",
        "modelName": "llama3",
        "id":"4"
    },
      {
        "image": "/static/images/gemmaSquare.png",
        "name": "Gemma 3: 4b",
        "description": "Gemma 3 is a family of lightweight, state-of-the-art open models from Google, built from the same research and technology used to create the Gemini models, offering multimodal capabilities, a large context window, and multilingual support, making it suitable for a variety of text generation and image understanding tasks. ",
        "type": "llm",
        "modelName": "gemma3:4b",
        "id":"2"
    },
      {
        "image": "/static/images/geminiSquare.png",
        "name": "Gemini 1.5 Flash",
        "description": "Gemini 1.5 Flash is Google's fastest and most cost-efficient multimodal model, designed for high-volume, diverse tasks, featuring a 1-million token context window and excels at tasks like summarization, chat, and multimodal reasoning.  ",
        "type": "llm",
        "modelName": "gemini-1.5-flash",
        "id":"2"
    },
    {
        "image":"/static/images/deepseekRound.png",
        "name": "DeepSeek R1",
        "description": "DeepSeek-R1 is a reasoning-focused large language model (LLM) developed by DeepSeek AI, known for its strong performance in math, coding, and reasoning tasks, achieving results comparable to OpenAI's o1 model, but at a lower cost and with a focus on open-source accessibility",
        "type": "llm",
        "modelName": "deepseek-r1",
        "id":"5"
    },
    # {
    #     "image":"/static/images/gta.webp",
    #     "name": "GTA Agent",
    #     "description": "DeepSeek-R1 is a reasoning-focused large language model (LLM) developed by DeepSeek AI, known for its strong performance in math, coding, and reasoning tasks, achieving results comparable to OpenAI's o1 model, but at a lower cost and with a focus on open-source accessibility",
    #     "type": "agent",
    #     "modelName": "deepseek-r1",
    #     "id":"5"
    # },
      {
        "image":"/static/images/llamaSquare.png",
        "name": "LLama 3.1",
        "description": "Llama 3 is a large language model developed by Meta AI, positioned as a competitor to models like OpenAI's GPT series. It's designed to be a highly capable text-based AI, similar to other large language models, but with notable improvements and unique features.",
        "type": "llm",
        "modelName": "llama3.1",
        "id":"4"
    },
    #   {
    #     "image":"/static/images/comedyAgent.svg",
    #     "name": "Joke Generator Agent",
    #     "description": "Llama 3 is a large language model developed by Meta AI, positioned as a competitor to models like OpenAI's GPT series. It's designed to be a highly capable text-based AI, similar to other large language models, but with notable improvements and unique features.",
    #     "type": "agent",
    #     "modelName": "comedy-agent",
    #     "id":"4"
    # },
       {
        "image": "/static/images/gemmaSquare.png",
        "name": "Gemma 3: 1b",
        "description": "Gemma 3 is a family of lightweight, state-of-the-art open models from Google, built from the same research and technology used to create the Gemini models, offering multimodal capabilities, a large context window, and multilingual support, making it suitable for a variety of text generation and image understanding tasks. ",
        "type": "llm",
        "modelName": "gemma3:1b",
        "id":"2"
    },
    
   
    
]

@router.post("/getCarouselAiData")
async def getCarouselAiData(body:Body,response:Response):
    print(body)
    if(body.type == "all"):
        response.status_code = 200
        return APIResponse(200,"Successfully Fetched Data",allData)
 
    filteredData = [data for data in allData if data["type"] == body.type]
    if not filteredData:
        response.status_code = 404
        return APIResponse(404,"No Data Found","")
    else:
        response.status_code = 200
        return APIResponse(200,"Successfully Fetched Data",filteredData)
    
@router.post("/getConversationalLLM")
async def getConversationalData(body:ConversationBody,response:Response):
    try:
        resp = chatWithAgentsConversational(messagesList=body.messagesList,llmModel=body.llmModel)
        response.status_code = resp.httpCode
        return resp
    except Exception as e:
        print(f"{str(e)}")
        response.status_code=500
        return APIResponse(500,"Error occured ",""+str(e))
    
@router.post("/generalCryptoAnalysis")
async def getConversationalData(body:LLMBody,response:Response):
    try:
        # get current analysis
        curr_analysis = await stack_analysis()
        if not curr_analysis:
            print("No analysis found")
            resp =  generalCryptoAnalysisFull(body.llmModel)
            coin_analysis_obj = CoinAnalys
            apiResponse = APIResponse(200,"Successfully Generated ",resp)
            response.status_code = apiResponse.httpCode
            return apiResponse
        print(f"Current Analysis: {curr_analysis}")
        apiResponse = APIResponse(200,"Successfully Generated ",{"data":curr_analysis["analysis"],"sentiment":curr_analysis["sentiment"]})
        created_at = curr_analysis["created_at"]
        created_at = created_at.replace(tzinfo=timezone.utc)
        print(f"Created At: {created_at}")

        now = datetime.now(timezone.utc)
        print(f"Current Time: {now}")
        time_difference = now - created_at
        if time_difference > timedelta(days=1):
            print("The document is older than 1 day.")
            resp =  generalCryptoAnalysisFull(body.llmModel)
            await saveAnalysis(resp["data"],resp["sentiment"])
            apiResponse = APIResponse(200,"Successfully Generated ",resp)
        else:
            print("The document is newer than 1 day.")
        # Check if already analysis is generated for the day

        # resp =  generalCryptoAnalysisFull(body.llmModel)
        # await saveAnalysis(resp["data"],resp["sentiment"])
        # apiResponse = APIResponse(200,"Successfully Generated ",resp)
        response.status_code = apiResponse.httpCode
        return apiResponse
    except Exception as e:
        print(f"{str(e)}")
        response.status_code=500
        return APIResponse(500,"Error occured ",""+str(e))
    
@router.post("/coinCryptoAnalysis")
async def getCoinAnalysisData(body:CoinAnalysisBody,response:Response):
    try:
        # get current analysis
        # analysis =await stack_analysis_coin_analysis()
        analysis = getCoinCryptoAnalsysFunc(body.symbol,body.interval,body.llmModel)
        apiResponse = APIResponse(200,"Successfully Generated ",analysis)
        print(f"Current Analysis: {analysis}")
        # if not analysis:
        #     print("No analysis found")
        #     resp =  generalCryptoAnalysisFull(body.llmModel)
        #     await saveAnalysis(resp["data"],resp["sentiment"])
        #     apiResponse = APIResponse(200,"Successfully Generated ",resp)
        #     response.status_code = apiResponse.httpCode
        #     return apiResponse
        response.status_code = apiResponse.httpCode
        return apiResponse

        # curr_analysis = await stack_analysis_coin_analysis()
        # if not curr_analysis:
        #     print("No analysis found")
        #     resp =  getCoinCryptoAnalsysFunc(body.symbol,body.interval,body.llmModel)
        #     # await saveAnalysis(resp["data"])
        #     await addAnalysis(resp["data"])
        #     apiResponse = APIResponse(200,"Successfully Generated ",resp)
        #     response.status_code = apiResponse.httpCode
        #     return apiResponse
        # print(f"Current Analysis: {curr_analysis}")
        # apiResponse = APIResponse(200,"Successfully Generated ",{"data":curr_analysis["analysis"],"sentiment":curr_analysis["sentiment"]})
        # created_at = curr_analysis["created_at"]
        # created_at = created_at.replace(tzinfo=timezone.utc)
        # print(f"Created At: {created_at}")

        # now = datetime.now(timezone.utc)
        # print(f"Current Time: {now}")
        # time_difference = now - created_at
        # if time_difference > timedelta(days=1):
        #     print("The document is older than 1 day.")
        #     resp =  generalCryptoAnalysisFull(body.llmModel)
        #     await saveAnalysis(resp["data"],resp["sentiment"])
        #     apiResponse = APIResponse(200,"Successfully Generated ",resp)
        # else:
        #     print("The document is newer than 1 day.")
        # # Check if already analysis is generated for the day

        # # resp =  generalCryptoAnalysisFull(body.llmModel)
        # # await saveAnalysis(resp["data"],resp["sentiment"])
        # # apiResponse = APIResponse(200,"Successfully Generated ",resp)
        # response.status_code = apiResponse.httpCode
        # return apiResponse
    except Exception as e:
        print(f"{str(e)}")
        response.status_code=500
        return APIResponse(500,"Error occured ",""+str(e))