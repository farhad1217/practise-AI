from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from rich import print
load_dotenv()

model = init_chat_model("google_genai:gemini-3.1-flash-lite")


messages = [SystemMessage(content="you are a school support assistan. only answer school related question. If any question than school related question simply say: i cannot help with that. anwser will be plain text. max 10 lines of text. no bullet, decoratol bold or any fancy design")]

print("Welcome to my first chatbot. Ask any school related question. Type exit to quit.")

while True:
    prompt = input("YOU: ")
    if prompt.lower() == "exit":
        break
    messages.append(HumanMessage(prompt))
    result = model.invoke(messages)
    messages.append(result)
    print(f"BOT: {result.content[0]["text"]}")