from ..llms.llmSelector import getLLMFromModelName
from langchain_core.messages import HumanMessage, SystemMessage
from ..models.response import APIResponse

def convertMessagesListToLangchainMessages(messagesList):
    newMessageList = []
    for message in messagesList:
        if(message["sender"]=="ai"):
            newMessageList.append(SystemMessage(content=message["text"]))
        else:
            newMessageList.append(HumanMessage(content=message["text"]))
    
    return newMessageList
def chatWithAgentsConversational(messagesList,llmModel):
    try:
        llm = getLLMFromModelName(llmModel)
        convertedList = convertMessagesListToLangchainMessages(messagesList=messagesList)
        result = llm.invoke(convertedList)
        if llmModel=="gpt-4o-mini" or llmModel=="gemini-1.5-flash" or llmModel=="gemini-2.0-flash":
                result = result.content
        apiResponse = APIResponse(200,"Successfully Generated Response", result)
        return apiResponse
    except Exception as e:
        print(f'Exception {str(e)}')
        apiResponse = APIResponse(500,"Error ="+str(e),{})
        return apiResponse