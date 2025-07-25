from ..llms.chatGPT import gpt4ominiLLM,gpt4LLM
from ..llms.deepseek import deepseek_r1_llm,deepseek_7b_llm,deepseek_coder_llm
from ..llms.gemini import gemini_one_point_five_flash_llm,gemini_one_point_five_pro_llm,gemini_two_flash_llm,gemini_two_flash_lite_preview
from ..llms.llama import  llama3_point_3_1_llm,llama3_point_3_2_llm,llama3_llm
from ..llms.gemma import gemma3_llm,gemma3_1b_llm
from ..llms.mistral import mistral_llm
from ..llms.qwen import qwen2_point5
from ..llms.phi import phi4_llm

def getLLMFromModelName(modelname:str):
    if(modelname=="gpt-4o-mini"):
        return gpt4ominiLLM
    elif (modelname=="gpt-4"):
        return gpt4LLM
    elif (modelname=="deepseek-r1"):
        return deepseek_r1_llm
    elif (modelname=="deepseek-llm:7b"):
        return deepseek_7b_llm
    elif (modelname=="deepseek-coder"):
        return deepseek_coder_llm
    elif (modelname=="gemini-1.5-flash"):
        return gemini_one_point_five_flash_llm
    elif (modelname=="gemini-1.5-pro"):
        return gemini_one_point_five_pro_llm
    elif (modelname=="gemini-2.0-flash"):
        return gemini_two_flash_llm
    elif (modelname=="gemini-2.0-flash-lite"):
        return gemini_two_flash_lite_preview
    elif (modelname=="deepseek-llm:7b"):
        return deepseek_7b_llm
    elif (modelname=="llama3"):
        return llama3_llm
    elif (modelname=="llama3.1"):
        return llama3_point_3_1_llm
    elif (modelname=="llama3.2"):
        return llama3_point_3_2_llm
    elif (modelname=="gemma3:4b"):
        return gemma3_llm
    elif (modelname=="gemma3:1b"):
        return gemma3_1b_llm
    elif (modelname=="mistral"):
        return mistral_llm
    elif (modelname=="qwen2.5"):
        return qwen2_point5
    elif (modelname=="phi4"):
        return phi4_llm
    else:
        return None
    
    