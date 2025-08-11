# Challenge 01: Azure AI Foundry Setup Guide

This guide walks you through setting up your development environment and Azure subscription for working with Azure AI Foundry.

## Prerequisites

- Python (Version 3.7 or higher, Python 3.13 preferred)
- Pip (package installer for Python)
- Active Azure Subscription
- Azure Developer CLI

For more information, see the [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/azure-ai-foundry/overview)

## Step-by-Step Guide

### Step 1: Create Azure AI Foundry Resource

1. Log in to your Azure portal
2. Create a new Azure AI Foundry resource
3. Note down your resource endpoint URL (you'll need this later)

### Step 2: Set Up Python Virtual Environment

Choose your preferred code editor (e.g., VS Code) and follow these steps:

1. Create Virtual Environment:
   ```bash
   python3.13 -m venv .venv
   ```

2. Activate Virtual Environment:
   
   **Windows PowerShell:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   # or
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source .venv/bin/activate
   ```

### Step 3: Clone GitHub Repository

1. Clone the project repository:
   ```bash
   git clone https://github.com/esvin2661/Agentic-AI-WTH-Building-Agent-to-Agent-Systems-in-Azure
   ```
2. Follow prompts to sign in using your Azure credentials

### Step 4: Install Required Packages

Open a terminal and run:
```bash
pip install azure-ai-projects azure-identity
```

Verify installation:
```bash
pip list
```

### Step 5: Set Up Version Control

1. Create `.gitignore`:
   - Add virtual environment and other non-essential files
   - Ensure `venv/` and `__pycache__/` are included

2. Generate `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   ```

### Step 6: Install Project Dependencies

Ensure your virtual environment is activated, then run:
```bash
pip install -r requirements.txt
```

This will install:
- Azure AI Foundry SDK
- Azure Core libraries
- Authentication and storage dependencies

### Step 7: Test Azure AI Foundry Connection

1. Create a test script (e.g., `example.py`):
   ```python
   from azure.identity import DefaultAzureCredential
   from azure.ai.projects import AIProjectClient

   def test_connection():
       project = AIProjectClient(
           endpoint="your_foundry_endpoint",  # Replace with your endpoint
           credential=DefaultAzureCredential()
       )
       print("Successfully connected to Azure AI Foundry!")
   ```

2. Replace `your_foundry_endpoint` with your Azure AI Foundry endpoint URL
   - Format: `https://your-project.services.ai.azure.com/`
   - Find this in your Azure portal under your AI Foundry resource

3. Run the test script:
   ```bash
   python src/example.py
   ```

A successful connection confirms your environment is properly set up!

## Next Steps

Once setup is complete, you can proceed to Challenge 02 to begin working with the Azure AI Foundry agents.


