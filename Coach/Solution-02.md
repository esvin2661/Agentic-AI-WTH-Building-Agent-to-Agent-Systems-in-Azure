
Set up Semantic Kernel in Python so you can orchestrate your agents and enable intelligent planning and task execution.

 ✅ Step 1: Make Sure You’re in Your Virtual Environment
If you’re not already in your project folder and virtual environment:

```
cd agentic-wth
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
You should see (.venv) in your terminal prompt.

 ✅ Step 2: Install Semantic Kernel (if not already installed)
 ```
pip install semantic-kernel
```
 ✅ Step 3: Create a .env File for Your API Keys
This file will store your OpenAI or Azure OpenAI credentials securely.

In your project root, create a file named .env 
Add the following (replace with your actual keys): 
```
OPENAIAPIKEY=your-openai-key
OPENAIENDPOINT=https://your-endpoint.openai.azure.com/
OPENAIDEPLOYMENTNAME=your-deployment-name
OPENAIMODEL_NAME=gpt-35-turbo
```

📝 Tip: Never commit .env to GitHub. Add it to .gitignore.


 ✅ Step 4: Create a Basic Kernel Script
Let’s test that Semantic Kernel is working.
Create a file called test_kernel.py:
```
import os
from semantickernel import Kernel
from semantickernel.connectors.ai.openai import AzureChatCompletion
```
# Load environment variables
```
from dotenv import loaddotenv
loaddotenv()
```
```
# Initialize kernel
kernel = Kernel()
```
```
# Configure Azure OpenAI
apikey = os.getenv("OPENAIAPIKEY")
endpoint = os.getenv("OPENAIENDPOINT")
deployment = os.getenv("OPENAIDEPLOYMENTNAME")

kernel.addchatservice(
    "chatcompletion",
    AzureChatCompletion(deploymentname=deployment, endpoint=endpoint, apikey=apikey)
)
```
# Test a simple prompt
```
async def run():
    result = await kernel.chatcomplete("What is Semantic Kernel?")
    print(result)

import asyncio
asyncio.run(run())
  ```

 ✅ Step 5: Run the Script
python test_kernel.py
You should see a response from the model like:

```
“Semantic Kernel is an open-source SDK that lets you build AI-first apps…”
```


 ✅ Step 6: Create a skills/ Folder (Optional but Recommended)
This is where you’ll store your custom plugins and skills.
```
mkdir skills
```
You can later add folders like MonitorSkill, AnomalySkill, etc., each with a config.json and skprompt.txt.

 ✅ Challenge 002 Complete!
