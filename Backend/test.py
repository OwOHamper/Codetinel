from src.api.routes.project import get_vulnerabilities
import json

async def test():
    result = await get_vulnerabilities("6741fc16f70ec7742e21e03b")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    import asyncio
    asyncio.run(test())