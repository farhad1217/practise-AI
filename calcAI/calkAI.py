from dotenv import load_dotenv
from rich import print
from langchain.tools import tool
from langchain.messages import AIMessage, SystemMessage, HumanMessage
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

load_dotenv()

@tool
def addition(a:int|float, b:int|float)->int|float:
    "get two integer or float a and b and return their addition"
    return a+b

@tool
def subtraction(a:int|float, b:int|float)->int|float:
    "get two integer or float a and b and return their subtraction"
    return a-b

@tool
def multiplication(a:int|float, b:int|float)->int|float:
    "get two integer or float a and b and return their multiplication"
    return a*b

@tool
def divition(a:int|float, b:int|float)->int|float:
    "get two integer or float a and b and return their divition"
    return a/b

tools = [addition, subtraction, multiplication, divition]
model = init_chat_model("google_genai:gemini-3.1-flash-lite")
agent = create_agent(model=model, tools=tools)
messages = [SystemMessage(content="you are a modern calculator. Your will be given a math expression. solve this with BODMAS rule, with the help of four tool i have given to you. [addition, subtraction, multiplication, divition]. Give simple one liner answer. No explanation. If expression is invalid the say: Invalid expression.")]

print("Welcome to my calcAI. give a expression to solve or type exit to quite.")

while True:
    prompt = input("YOU: ")
    if prompt.lower() == "exit":
        break
    messages.append(HumanMessage(content=prompt))
    result = agent.invoke({"messages": messages})
    messages = result["messages"]
    print(f"BOT: {result["messages"][-1].content[0]["text"]}")
    
print(messages)