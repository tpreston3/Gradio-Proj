from google import genai
from google.genai import types
import asyncio
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()



# Import the Google Gemini client
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

configuration = types.GenerateContentConfig(system_instruction="You're a helpful assistant.",tools=[types.Tool(google_search=types.GoogleSearch())])

async def main():
    async for chunk in await client.aio.models.generate_content_stream(
        model='gemini-2.5-pro', contents='Tell me funny a story in 100 words.', config=configuration
    ):
        # Print the chunk of text as it is generated
        print(chunk.text, end='')

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())