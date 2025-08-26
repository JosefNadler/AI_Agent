from todoist_api_python.api import TodoistAPI
import os
from dotenv import load_dotenv

load_dotenv()

todoist_api_key = os.getenv("TODOIST_API_KEY")

todoist = TodoistAPI(todoist_api_key)
todoist.add_task("Buy milk from the shop")