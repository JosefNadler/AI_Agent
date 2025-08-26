import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_openai_tools_agent, AgentExecutor
from todoist_api_python.api import TodoistAPI


load_dotenv()

todoist_api_key = os.getenv("TODOIST_API_KEY")
gemini_api_key = os.getenv("GEMENI_API_KEY")


todoist = TodoistAPI(todoist_api_key)

@tool
def add_task(task: str, description=None):
    """Add a new task to the user's task list. Use this when the user wants to add or create a task"""
    print(f"AI just added a new task: {task} with description: {description}")
    todoist.add_task(content=task, description=description)

@tool
def show_tasks():
    """Show all tasks from Todoist. Use this tool when the user wants to see their tasks."""
    tasks = []
    first = True
    results_paginator = todoist.get_tasks()
    for tasks_list in results_paginator:
        for task in tasks_list:
            if first:
                first = False
            else:
                tasks.append(task.content)
    return tasks


tools = [add_task, show_tasks]

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash', google_api_key=gemini_api_key, temperature=0.3)

system_prompt = """You are a helpful assistant. 
You will help the user add tasks.
You will help the user show existing tasks. Print them in bullet list format.
"""
#system_prompt = "You are a helpful assistant."
#user_input ="add a new task to buy a new car with the description: Buy it from the local dealer."
#user_input = "what is the meaning of life."


prompt = ChatPromptTemplate([
    ('system', system_prompt), 
    MessagesPlaceholder('history'),    
    ('user', "{input}" ), 
    MessagesPlaceholder('agent_scratchpad')
    ])

# chain = prompt | llm | StrOutputParser()
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
   
history = []

while True:
    user_input = input("You: ")

    response = agent_executor.invoke({'input': user_input, 'history': history})
    print(response['output'])
    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=response['output']))

