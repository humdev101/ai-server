from langchain_ollama.llms import OllamaLLM

gemma3_llm = OllamaLLM(model="gemma3:latest")
gemma3_1b_llm = OllamaLLM(model="gemma3:1b")