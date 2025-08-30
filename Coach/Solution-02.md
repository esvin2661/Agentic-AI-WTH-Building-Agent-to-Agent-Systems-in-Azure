
🧠 Challenge 002: Semantic Kernel Setup & Configuration (Updated)
🎯 Objective
Set up Semantic Kernel in Python using Azure OpenAI services so you can orchestrate your agents and enable intelligent planning and task execution.

🪜 Step-by-Step Instructions
✅ Step 1: Activate Your Virtual Environment
Make sure you're in your project folder and virtual environment:


###Shell
cd agentic-wth
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
You should see (.venv) in your terminal prompt.

✅ Step 2: Install Semantic Kernel
If not already installed:

pip install semantic-kernel


✅ Step 3: Create a .env File for Your API Keys
This file securely stores your Azure OpenAI credentials.

Create a .env file in your project root and add:




Shell
env isn’t fully supported. Syntax highlighting is based on Shell.

OPENAIAPIKEY=your-openai-key
OPENAIENDPOINT=https://your-endpoint.openai.azure.com/
OPENAIDEPLOYMENTNAME=your-deployment-name
OPENAIMODEL_NAME=gpt-35-turbo

📝 Tips
Never commit .env to GitHub. Add it to .gitignore.
Avoid white spaces around = to ensure keys are read correctly.

✅ Step 4: Create a Basic Kernel Script
Create a file called test_kernel.py and paste the following code:




///Python
import os
import asyncio
from dotenv import load_dotenv
from semantic_kernel.kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# Load environment variables
load_dotenv()

# Retrieve credentials
api_key = os.getenv("OPENAIAPIKEY")
endpoint = os.getenv("OPENAIENDPOINT")
deployment_name = os.getenv("OPENAIDEPLOYMENTNAME")

# Initialize Semantic Kernel
kernel = Kernel()

# Add Azure OpenAI chat completion service
kernel.add_service(
    AzureChatCompletion(
        service_id="chatcompletion",
        deployment_name=deployment_name,
        endpoint=endpoint,
        api_key=api_key
    )
)

# Run a test prompt
async def run():
    result = await kernel.invoke_prompt_async("What is Semantic Kernel?")
    print(result)

asyncio.run(run())

Show more lines
✅ Step 5: Run the Script
Run the script to verify your setup:




Shell
python test_kernel.py
Expected output:




Shell
“Semantic Kernel is an open-source SDK that lets you build AI-first apps…”
✅ Step 6: Create a skills/ Folder (Optional but Recommended)
This is where you’ll store your custom plugins and skills:




Shell
mkdir skills
You can later add folders like MonitorSkill, AnomalySkill, etc., each with a config.json and skprompt.txt.

🏁 Challenge 002 Complete!
Let me know if you’d like help updating your GitHub README or creating a markdown version of this documentation!
