from langchain.prompts import ChatPromptTemplate
import json
from ..llms.llmSelector import getLLMFromModelName
import requests
from ..service.analysis import addAnalysis,AnalysisBase
import asyncio
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

websearch_prompt = """

"""

mobile_phones_prompt ="""

"""

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
        if llmModel=="gpt-4o-mini" or llmModel=="gemini-1.5-flash" or llmModel=="gemini-2.0-flash":
            result = result.content
        return result
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



# generalCryptoAnalysisFunc("[{\"name\":\"Bitcoin\",\"symbol\":\"BTC\",\"price\":\"91890.47000000\",\"coinImage\":\"images/btc.webp\",\"_id\":\"6729071803b0123da40fa7dd\",\"analytics\":{\"_id\":\"67eb04b0e6843b1e62bcbd01\",\"coinSymbol\":\"BTCUSDT\",\"name\":\"Bitcoin\",\"image\":\"images/btc.webp\",\"one_day_change\":\"-1.50\",\"three_day_change\":\"5.72\",\"seven_day_change\":\"8.82\",\"one_month_change\":\"12.25\",\"three_month_change\":\"-9.29\",\"one_year_change\":\"31.83\",\"createdAt\":\"2025-03-31T21:10:08.350Z\",\"updatedAt\":\"2025-04-24T09:18:07.694Z\",\"__v\":0,\"price\":\"92347.82000000\"}},{\"name\":\"Ethereum\",\"symbol\":\"ETH\",\"price\":\"1737.75000000\",\"coinImage\":\"images/eth.webp\",\"_id\":\"6729071803b0123da40fa7de\",\"analytics\":{\"_id\":\"67eb195717ec8a517ecd7e61\",\"coinSymbol\":\"ETHUSDT\",\"name\":\"Ethereum\",\"image\":\"images/eth.webp\",\"one_day_change\":\"-1.59\",\"three_day_change\":\"6.69\",\"seven_day_change\":\"9.68\",\"one_month_change\":\"-0.34\",\"three_month_change\":\"-79.43\",\"one_year_change\":\"-74.09\",\"createdAt\":\"2025-03-31T22:38:15.722Z\",\"updatedAt\":\"2025-04-24T08:57:24.554Z\",\"__v\":0,\"price\":\"1733.96000000\"}},{\"name\":\"BNB\",\"symbol\":\"BNB\",\"price\":\"601.80000000\",\"coinImage\":\"images/bnb.webp\",\"_id\":\"6729071803b0123da40fa7df\",\"analytics\":{\"_id\":\"67eb18f517ec8a517ecd7e3e\",\"coinSymbol\":\"BNBUSDT\",\"name\":\"BNB\",\"image\":\"images/bnb.webp\",\"one_day_change\":\"-2.09\",\"three_day_change\":\"0.09\",\"seven_day_change\":\"3.11\",\"one_month_change\":\"0.86\",\"three_month_change\":\"-9.87\",\"one_year_change\":\"2.54\",\"createdAt\":\"2025-03-31T22:36:37.525Z\",\"updatedAt\":\"2025-04-24T08:57:24.887Z\",\"__v\":0,\"price\":\"595.05000000\"}},{\"name\":\"Solana\",\"symbol\":\"SOL\",\"price\":\"146.40000000\",\"coinImage\":\"images/sol.webp\",\"_id\":\"6729071803b0123da40fa7e0\",\"analytics\":{\"_id\":\"67eb19dd884a50c319d4df5a\",\"coinSymbol\":\"SOLUSDT\",\"name\":\"Solana\",\"image\":\"images/sol.webp\",\"one_day_change\":\"-2.34\",\"three_day_change\":\"5.37\",\"seven_day_change\":\"10.13\",\"one_month_change\":\"17.66\",\"three_month_change\":\"-58.64\",\"one_year_change\":\"3.87\",\"createdAt\":\"2025-03-31T22:40:29.423Z\",\"updatedAt\":\"2025-04-24T08:57:25.218Z\",\"__v\":0,\"price\":\"146.49000000\"}},{\"name\":\"Ripple\",\"symbol\":\"XRP\",\"price\":\"2.14640000\",\"coinImage\":\"images/xrp.webp\",\"_id\":\"6729071803b0123da40fa7e1\",\"analytics\":{\"_id\":\"67eb19df884a50c319d4df75\",\"coinSymbol\":\"XRPUSDT\",\"name\":\"Ripple\",\"image\":\"images/xrp.webp\",\"one_day_change\":\"-3.44\",\"three_day_change\":\"2.55\",\"seven_day_change\":\"3.64\",\"one_month_change\":\"4.59\",\"three_month_change\":\"-34.94\",\"one_year_change\":\"76.35\",\"createdAt\":\"2025-03-31T22:40:31.211Z\",\"updatedAt\":\"2025-04-24T08:57:25.550Z\",\"__v\":0,\"price\":\"2.13280000\"}},{\"name\":\"Dogecoin\",\"symbol\":\"DOGE\",\"price\":\"0.17116000\",\"coinImage\":\"images/doge.webp\",\"_id\":\"6729071803b0123da40fa7e2\",\"analytics\":{\"_id\":\"67eb19e0884a50c319d4df90\",\"coinSymbol\":\"DOGEUSDT\",\"name\":\"Dogecoin\",\"image\":\"images/doge.webp\",\"one_day_change\":\"-5.23\",\"three_day_change\":\"6.45\",\"seven_day_change\":\"9.60\",\"one_month_change\":\"7.79\",\"three_month_change\":\"-86.08\",\"one_year_change\":\"10.86\",\"createdAt\":\"2025-03-31T22:40:32.952Z\",\"updatedAt\":\"2025-04-24T08:57:25.887Z\",\"__v\":0,\"price\":\"0.17127000\"}},{\"name\":\"TRON\",\"symbol\":\"TRX\",\"price\":\"0.24260000\",\"coinImage\":\"images/trx.webp\",\"_id\":\"6729071803b0123da40fa7e3\",\"analytics\":{\"_id\":\"67eb19e4884a50c319d4dfab\",\"coinSymbol\":\"TRXUSDT\",\"name\":\"TRON\",\"image\":\"images/trx.webp\",\"one_day_change\":\"-1.56\",\"three_day_change\":\"-1.03\",\"seven_day_change\":\"-2.06\",\"one_month_change\":\"5.58\",\"three_month_change\":\"-0.24\",\"one_year_change\":\"50.70\",\"createdAt\":\"2025-03-31T22:40:36.663Z\",\"updatedAt\":\"2025-04-24T08:57:26.218Z\",\"__v\":0,\"price\":\"0.24260000\"}},{\"name\":\"Toncoin\",\"symbol\":\"TON\",\"price\":\"3.08600000\",\"coinImage\":\"images/ton.webp\",\"_id\":\"6729071803b0123da40fa7e4\",\"analytics\":{\"_id\":\"67eb19e7884a50c319d4dfc6\",\"coinSymbol\":\"TONUSDT\",\"name\":\"Toncoin\",\"image\":\"images/ton.webp\",\"one_day_change\":\"0.51\",\"three_day_change\":\"2.50\",\"seven_day_change\":\"5.41\",\"one_month_change\":\"-21.57\",\"three_month_change\":\"-53.92\",\"one_year_change\":\"-93.88\",\"createdAt\":\"2025-03-31T22:40:39.982Z\",\"updatedAt\":\"2025-04-24T08:57:26.557Z\",\"__v\":0,\"price\":\"3.08400000\"}},{\"name\":\"Cardano\",\"symbol\":\"ADA\",\"price\":\"0.67660000\",\"coinImage\":\"images/ada.webp\",\"_id\":\"6729071803b0123da40fa7e5\",\"analytics\":{\"_id\":\"67ec04579b26d90e342bc91f\",\"coinSymbol\":\"ADAUSDT\",\"name\":\"Cardano\",\"image\":\"images/ada.webp\",\"one_day_change\":\"-2.64\",\"three_day_change\":\"5.83\",\"seven_day_change\":\"9.39\",\"one_month_change\":\"6.49\",\"three_month_change\":\"-34.78\",\"one_year_change\":\"35.23\",\"createdAt\":\"2025-04-01T15:20:55.281Z\",\"updatedAt\":\"2025-04-24T08:57:26.893Z\",\"__v\":0,\"price\":\"0.67330000\"}},{\"name\":\"Shiba Inu\",\"symbol\":\"SHIB\",\"price\":\"0.00001302\",\"coinImage\":\"images/shiba.webp\",\"_id\":\"6729071803b0123da40fa7e6\",\"analytics\":{\"_id\":\"67eb1a2fa59788c39bb0f1a8\",\"coinSymbol\":\"SHIBUSDT\",\"name\":\"Shiba Inu\",\"image\":\"images/shiba.webp\",\"one_day_change\":\"-4.24\",\"three_day_change\":\"3.79\",\"seven_day_change\":\"10.00\",\"one_month_change\":\"8.92\",\"three_month_change\":\"-39.65\",\"one_year_change\":\"-80.76\",\"createdAt\":\"2025-03-31T22:41:51.793Z\",\"updatedAt\":\"2025-04-24T08:57:27.225Z\",\"__v\":0,\"price\":\"0.00001296\"}},{\"name\":\"Wrapped Bitcoin\",\"symbol\":\"WBTC\",\"price\":\"91838.72000000\",\"coinImage\":\"images/wbtc.webp\",\"_id\":\"6729071803b0123da40fa7e7\",\"analytics\":{\"_id\":\"67eb1a08884a50c319d4e0ec\",\"coinSymbol\":\"WBTCUSDT\",\"name\":\"Wrapped Bitcoin\",\"image\":\"images/wbtc.webp\",\"one_day_change\":\"-1.58\",\"three_day_change\":\"5.65\",\"seven_day_change\":\"8.76\",\"one_month_change\":\"12.39\",\"three_month_change\":\"-9.27\",\"one_year_change\":\"31.83\",\"createdAt\":\"2025-03-31T22:41:12.306Z\",\"updatedAt\":\"2025-04-24T08:57:27.563Z\",\"__v\":0,\"price\":\"91901.63000000\"}},{\"name\":\"Avalanche\",\"symbol\":\"AVAX\",\"price\":\"21.76000000\",\"coinImage\":\"images/avax.webp\",\"_id\":\"6729071803b0123da40fa7e8\",\"analytics\":{\"_id\":\"67eb1a43a59788c39bb0f1db\",\"coinSymbol\":\"AVAXUSDT\",\"name\":\"Avalanche\",\"image\":\"images/avax.webp\",\"one_day_change\":\"-4.28\",\"three_day_change\":\"6.06\",\"seven_day_change\":\"12.31\",\"one_month_change\":\"16.03\",\"three_month_change\":\"-59.17\",\"one_year_change\":\"-66.30\",\"createdAt\":\"2025-03-31T22:42:11.637Z\",\"updatedAt\":\"2025-04-24T08:57:27.894Z\",\"__v\":0,\"price\":\"21.72000000\"}},{\"name\":\"Bitcoin Cash\",\"symbol\":\"BCH\",\"price\":\"357.40000000\",\"coinImage\":\"images/bch.webp\",\"_id\":\"6729071803b0123da40fa7e9\",\"analytics\":{\"_id\":\"67ec04679b26d90e342bc98d\",\"coinSymbol\":\"BCHUSDT\",\"name\":\"Bitcoin Cash\",\"image\":\"images/bch.webp\",\"one_day_change\":\"0.80\",\"three_day_change\":\"6.22\",\"seven_day_change\":\"8.29\",\"one_month_change\":\"17.69\",\"three_month_change\":\"-16.97\",\"one_year_change\":\"-29.02\",\"createdAt\":\"2025-04-01T15:21:11.806Z\",\"updatedAt\":\"2025-04-24T08:57:28.233Z\",\"__v\":0,\"price\":\"356.00000000\"}},{\"name\":\"Polkadot\",\"symbol\":\"DOT\",\"price\":\"3.96000000\",\"coinImage\":\"images/dot.webp\",\"_id\":\"6729071803b0123da40fa7ea\",\"analytics\":{\"_id\":\"67ec046c9b26d90e342bc9bf\",\"coinSymbol\":\"DOTUSDT\",\"name\":\"Polkadot\",\"image\":\"images/dot.webp\",\"one_day_change\":\"-2.76\",\"three_day_change\":\"0.88\",\"seven_day_change\":\"8.70\",\"one_month_change\":\"2.20\",\"three_month_change\":\"-49.46\",\"one_year_change\":\"-76.68\",\"createdAt\":\"2025-04-01T15:21:16.267Z\",\"updatedAt\":\"2025-04-24T08:57:28.564Z\",\"__v\":0,\"price\":\"3.94400000\"}},{\"name\":\"Sui\",\"symbol\":\"SUI\",\"price\":\"2.97140000\",\"coinImage\":\"images/sui.webp\",\"_id\":\"6729071803b0123da40fa7eb\",\"analytics\":{\"_id\":\"67ec007367a67b6e53a31c0f\",\"coinSymbol\":\"SUIUSDT\",\"name\":\"Sui\",\"image\":\"images/sui.webp\",\"one_day_change\":\"1.46\",\"three_day_change\":\"24.90\",\"seven_day_change\":\"29.71\",\"one_month_change\":\"22.78\",\"three_month_change\":\"-27.09\",\"one_year_change\":\"64.03\",\"createdAt\":\"2025-04-01T15:04:19.618Z\",\"updatedAt\":\"2025-04-24T08:57:28.897Z\",\"__v\":0,\"price\":\"2.98500000\"}},{\"name\":\"Litecoin\",\"symbol\":\"LTC\",\"price\":\"81.41000000\",\"coinImage\":\"images/ltc.webp\",\"_id\":\"6729071803b0123da40fa7ec\",\"analytics\":{\"_id\":\"67ec04739b26d90e342bc9f1\",\"coinSymbol\":\"LTCUSDT\",\"name\":\"Litecoin\",\"image\":\"images/ltc.webp\",\"one_day_change\":\"-2.83\",\"three_day_change\":\"2.29\",\"seven_day_change\":\"8.54\",\"one_month_change\":\"-2.43\",\"three_month_change\":\"-39.32\",\"one_year_change\":\"3.26\",\"createdAt\":\"2025-04-01T15:21:23.672Z\",\"updatedAt\":\"2025-04-24T08:57:29.229Z\",\"__v\":0,\"price\":\"81.25000000\"}},{\"name\":\"NEAR Protocol\",\"symbol\":\"NEAR\",\"price\":\"2.37300000\",\"coinImage\":\"images/near.webp\",\"_id\":\"6729071803b0123da40fa7ed\",\"analytics\":{\"_id\":\"67ec008767a67b6e53a31cd0\",\"coinSymbol\":\"NEARUSDT\",\"name\":\"NEAR Protocol\",\"image\":\"images/near.webp\",\"one_day_change\":\"-4.01\",\"three_day_change\":\"4.13\",\"seven_day_change\":\"15.31\",\"one_month_change\":\"-3.31\",\"three_month_change\":\"-89.60\",\"one_year_change\":\"-198.41\",\"createdAt\":\"2025-04-01T15:04:39.533Z\",\"updatedAt\":\"2025-04-24T08:57:29.565Z\",\"__v\":0,\"price\":\"2.38000000\"}},{\"name\":\"Uniswap\",\"symbol\":\"UNI\",\"price\":\"5.69900000\",\"coinImage\":\"images/uni.webp\",\"_id\":\"6729071803b0123da40fa7ee\",\"analytics\":{\"_id\":\"67eb1a4da59788c39bb0f226\",\"coinSymbol\":\"UNIUSDT\",\"name\":\"Uniswap\",\"image\":\"images/uni.webp\",\"one_day_change\":\"-1.49\",\"three_day_change\":\"6.61\",\"seven_day_change\":\"11.04\",\"one_month_change\":\"3.13\",\"three_month_change\":\"-88.62\",\"one_year_change\":\"-25.18\",\"createdAt\":\"2025-03-31T22:42:21.819Z\",\"updatedAt\":\"2025-04-24T08:57:29.901Z\",\"__v\":0,\"price\":\"5.67100000\"}},{\"name\":\"Aptos\",\"symbol\":\"APT\",\"price\":\"5.21500000\",\"coinImage\":\"images/apt.webp\",\"_id\":\"6729071803b0123da40fa7ef\",\"analytics\":{\"_id\":\"67eb1a50a59788c39bb0f241\",\"coinSymbol\":\"APTUSDT\",\"name\":\"Aptos\",\"image\":\"images/apt.webp\",\"one_day_change\":\"-0.62\",\"three_day_change\":\"1.91\",\"seven_day_change\":\"12.98\",\"one_month_change\":\"1.30\",\"three_month_change\":\"-45.86\",\"one_year_change\":\"-72.13\",\"createdAt\":\"2025-03-31T22:42:24.566Z\",\"updatedAt\":\"2025-04-24T08:57:35.365Z\",\"__v\":0,\"price\":\"5.20500000\"}},{\"name\":\"Pepe\",\"symbol\":\"PEPE\",\"price\":\"0.00000840\",\"coinImage\":\"images/pepe.webp\",\"_id\":\"6729071803b0123da40fa7f0\",\"analytics\":{\"_id\":\"67eb1a0e884a50c319d4e122\",\"coinSymbol\":\"PEPEUSDT\",\"name\":\"Pepe\",\"image\":\"images/pepe.webp\",\"one_day_change\":\"-6.95\",\"three_day_change\":\"7.30\",\"seven_day_change\":\"14.25\",\"one_month_change\":\"22.63\",\"three_month_change\":\"-56.30\",\"one_year_change\":\"4.91\",\"createdAt\":\"2025-03-31T22:41:18.187Z\",\"updatedAt\":\"2025-04-24T08:57:35.696Z\",\"__v\":0,\"price\":\"0.00000839\"}},{\"name\":\"Internet Computer\",\"symbol\":\"ICP\",\"price\":\"4.98600000\",\"coinImage\":\"images/icp.webp\",\"_id\":\"6729071803b0123da40fa7f1\",\"analytics\":{\"_id\":\"67eb1a0b884a50c319d4e107\",\"coinSymbol\":\"ICPUSDT\",\"name\":\"Internet Computer\",\"image\":\"images/icp.webp\",\"one_day_change\":\"-2.99\",\"three_day_change\":\"1.66\",\"seven_day_change\":\"7.36\",\"one_month_change\":\"-1.76\",\"three_month_change\":\"-70.05\",\"one_year_change\":\"-150.76\",\"createdAt\":\"2025-03-31T22:41:15.272Z\",\"updatedAt\":\"2025-04-24T08:57:36.032Z\",\"__v\":0,\"price\":\"4.99100000\"}}]","qwen2.5")