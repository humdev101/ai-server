from langchain.prompts import ChatPromptTemplate
import json
from ..llms.llmSelector import getLLMFromModelName
import requests
from ..service.analysis import addAnalysis,AnalysisBase
from ..service.mobileService import getDevice
from ..service.collection import getCollection
# import asyncio
# joke_prompt = "Tell me a joke about {topic} in {lines} lines "
# prompt_template = ChatPromptTemplate.from_template(joke_prompt)

jsonValue = {
    "classification":"value classified based on query"
}

classification_prompt = """
Classify the following query : "{query}" into one of the following categories :
CONVERSATION: just a basic conversation going on
INTENT: The query aims to perform a task through the Agent
WEBSEARCH: No Information is provided so web search needs to be done
MOBILEPHONES: The query is based on mobile phones
WEB3: The query is based on Cryptocurrency

Please return response in JSON string format with the classification of the query in the {jsonValue} . Please do not add any other value and strictly adhere to the spellings. Also do not enclose JSON in ```json ``` 
"""


conversation_prompt ="""

"""

intent_prompt = """

"""

review_collection_prompt = """
Review the following NFT Collection and provide your opinion on it on whether it is a good investment or not.
Here is the collection data in JSON format:
{collectionData}

"""


async def getCollectionReview(key,chain,llmModel):
    try:
        llm = getLLMFromModelName(llmModel)
        collectionData = await getCollection(key,chain)
        classification_template = ChatPromptTemplate.from_template(review_collection_prompt)
        prompt = classification_template.invoke({"collectionData":collectionData})
        print(prompt)
        result = llm.invoke(prompt)
        print("LLM Response")
        print(result)
        if "gemini" in llmModel or "gpt-4o-mini" in llmModel:
            result = result.content
        apiResponse = {}
        apiResponse["data"] = result
        return apiResponse
    except Exception as e:
        print(str(e))
        return None


review_nft_prompt = """
You are a Crypto NFT expert who will review a specific NFT provided to you.
Here is the NFT data in JSON format:
{nftData}

"""

async def getNFTReview(key,chain,llmModel):
    try:
        llm = getLLMFromModelName(llmModel)
        nftData = await getCollection(key,chain)
        classification_template = ChatPromptTemplate.from_template(review_nft_prompt)
        prompt = classification_template.invoke({"nftData":nftData})
        print(prompt)
        result = llm.invoke(prompt)
        print("LLM Response")
        print(result)
        if "gemini" in llmModel or "gpt-4o-mini" in llmModel:
            result = result.content
        apiResponse = {}
        apiResponse["data"] = result
        return apiResponse
    except Exception as e:
        print(str(e))
        return None




websearch_prompt = """

"""

mobile_phone_review_prompt ="""
You are a Mobile Phones expert who finds out the best mobile phones based on the data provided in the JSON format.
Today you are provided with {mobile} to review it and give your opinion on it.
Below you will find all the data in JSON format:
{mobileData}
"""


async def getMobilePhoneReview(id,llmModel):
    try:
        llm = getLLMFromModelName(llmModel)
        mobile = await getDevice(id)
        classification_template = ChatPromptTemplate.from_template(mobile_phone_review_prompt)
        prompt = classification_template.invoke({"mobile":mobile["brand"],"mobileData": mobile})
        print(prompt)
        result = llm.invoke(prompt)
        print("LLM Response")
        print(result)
        if "gemini" in llmModel or "gpt-4o-mini" in llmModel:
            result = result.content
        apiResponse = {}
        apiResponse["data"] = result
        apiResponse["mobile"] = mobile["brand"]
        return apiResponse
    except Exception as e:
        print(str(e))
        return None


web3_prompt ="""

"""

article_prompt ="""


"""

crypto_analysis_prompt="""
You are a Crypto Plot Patterns expert who finds out patterns based on the data provided on a given timeframe and interval.
You are provided a {timeframe} data of {symbol} with each graph plot interval being {interval}:
Here is the graph plots list in JSON with the data given below:

{plotList}

Please find out all the patterns and finalize your answer if the price is Bullish , Bearish or neutral

Note: We are currently in April,2025 so please do not analyze before 2024
"""

classify_sentiment_prompt ="""
Classify the following response into bullish , bearish or neutral 

{analysis}

Give one word answer 
""" 

review_prompt = """
Review the response recieved from the LLM and put out a summary of 2-3 lines whether price is bullish or bearish. Here is the response recieved:

{response}
"""
# prompt = classification_prompt.invoke({"query": "What is the time"})
# llm = getLLMFromModelName("deepseek-llm:7b")
# result = llm.invoke(prompt)
# print(result)

def cryptoCoinsAnalysis(symbol,timeframe,interval,plotList,llmModel):
    try:
        llm = getLLMFromModelName(llmModel)
        classification_template = ChatPromptTemplate.from_template(crypto_analysis_prompt)
        prompt = classification_template.invoke({"symbol":symbol,"timeframe": timeframe,"interval":interval,"plotList":plotList})
        print(prompt)
        result = llm.invoke(prompt)
        print("LLM Response")
        print(result)
        sentiment_analysis = ChatPromptTemplate.from_template(classify_sentiment_prompt)
        sentiment_prompt = sentiment_analysis.invoke({"analysis":result})
        senti_result = llm.invoke(sentiment_prompt)
        if llmModel=="gpt-4o-mini" or llmModel=="gemini-1.5-flash" or llmModel=="gemini-2.0-flash":
            result = result.content
            senti_result = senti_result.content
        apiResponse = {}
        apiResponse["data"] = result
        apiResponse["sentiment"] = senti_result.lower()
        print("Sentiment ")
        print(senti_result)
        return apiResponse
    except Exception as e:
        print(str(e))
        return None


    # review_prompt_template = ChatPromptTemplate.from_template(review_prompt)
    # review= review_prompt_template.invoke({"response": result})
    # new_review = llm.invoke(review)
    # print("Final Answer :")
    # print(new_review)
    # jsonData = json.loads(result)
    # print(jsonData["classification"])

# cryptoCoinsAnalysis()

generalCryptoAnalysis = """
You are a Crypto Expert with the following Top Coins Data:
{topCoins} 
Consider USDT as USD for analysis.

Write a general analysis of crypto market of top crypto coins and provide your opinion if the market is bullish, bearish or neutral.

DONTS: 
1) Do not mention about JSON data in response
2) Do not talk about specific numbers unless it is specifically mentioned in the JSON Data
3) Do not talk about Market Capitilization as you haven't been provided any data for it now
4) Talk about time in relative terms like over the past year, month , day etc and not specifics



"""

backend_url = "https://api.humdev101.com/v1"


def getCoinData(symbol,timeframe):
    try:
        response = requests.post(backend_url+"/api/coin/getGraph", json={"symbol":symbol,"timeFrame":timeframe})
        jsonresp = response.json()
        print(jsonresp)
        return jsonresp
    except Exception as e:
        print(str(e))
        return None
# getCoinData("BTCUSDT","1h")

def getTopCoinsData():
    try:
        response = requests.post(backend_url+"/api/coin/getTopCoins", json={})
        jsonresp = response.json()
        # print(jsonresp)
        return jsonresp
    except Exception as e:
        print(str(e))
        return None

async def saveAnalysis(analysis,sentiment):
    try:
        newAnalysis = AnalysisBase(analysis=analysis,sentiment=sentiment)
        analysisResponse = await addAnalysis(newAnalysis)
        print("Mongo Analysis Object response "+str(analysisResponse))
    except Exception as e:
        print("Error occured "+str(e))
        return None

def generalCryptoAnalysisFunc(topCoins,llmModel):
    try:
        print("test")
        print(topCoins)
        llm = getLLMFromModelName(llmModel)
        classification_template = ChatPromptTemplate.from_template(generalCryptoAnalysis)
        prompt = classification_template.invoke({"topCoins": topCoins})
        print(prompt)
        result = llm.invoke(prompt)
        print("LLM Response")
        print(result)
        sentiment_analysis = ChatPromptTemplate.from_template(classify_sentiment_prompt)
        sentiment_prompt = sentiment_analysis.invoke({"analysis":result})
        senti_result = llm.invoke(sentiment_prompt)
        print("Sentiment ")
        print(senti_result)
        if llmModel=="gpt-4o-mini" or llmModel=="gemini-1.5-flash" or llmModel=="gemini-2.0-flash":
            result = result.content
            senti_result = senti_result.content
        
        apiResponse = {}
        apiResponse["data"] = result
        apiResponse["sentiment"] = senti_result
        print(apiResponse)
        return apiResponse
    except Exception as e:
        print("Error occured "+str(e))
        return None



def getCoinCryptoAnalsysFunc(symbol,timeframe,llmModel):
    data = getCoinData(symbol,timeframe)
    json_str = json.dumps(data["data"])
    print(json_str)
    result = cryptoCoinsAnalysis(symbol,timeframe,"1d",json_str,llmModel)
    return result

# getCoinCryptoAnalsysFunc("BTCUSDT","1h","llama3.1")


def generalCryptoAnalysisFull(llmModel):
    data = getTopCoinsData()
    json_str = json.dumps(data["data"])
    # print(json_str)
    result = generalCryptoAnalysisFunc(json_str,llmModel)
    return result


