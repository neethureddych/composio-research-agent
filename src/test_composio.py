from dotenv import load_dotenv
from composio import Composio
import os

load_dotenv()

if not os.getenv("COMPOSIO_API_KEY"):
    print("ERROR: API key not found. Check your .env file.")
else:
    print("API key found.")
    try:
        composio = Composio()
        result = composio.client.get("/api/v3/tools", cast_to=object)
        print("SUCCESS: Connected to Composio!")
        print("API response received.")
    except Exception as e:
        print("Connection failed:", type(e).__name__)
        print(str(e)[:300])
