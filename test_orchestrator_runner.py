import asyncio

from app import handle_user_input

# Run a test input
async def test():
    response = await handle_user_input("Check CPU usage")
    for line in response:
        print(line)

if __name__ == "__main__":
    asyncio.run(test())
