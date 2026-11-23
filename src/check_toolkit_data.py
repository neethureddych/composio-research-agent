from dotenv import load_dotenv
from composio import Composio

load_dotenv()

client = Composio()
response = client.toolkits.list(limit=5)

for toolkit in response.items:
    print("\nRAW TOOLKIT DATA:")
    print(toolkit)

    if hasattr(toolkit, "model_dump"):
        print("\nALL FIELDS:")
        print(toolkit.model_dump())

    print("=" * 60)