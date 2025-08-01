Challenge 01:Setup

Introduction:


Challenge: 

### Configure AI Foundry Endpoint

1. Open `config.py` and update the AI Foundry settings:
   ```python
   AI_FOUNDRY = {
       "endpoint": "your-endpoint-url",
       "api_version": "2023-05-15", 
       "api_key": "your-api-key"
   }
   ```

2. Or use environment variables:
   ```bash
   # Windows
   set AI_FOUNDRY_ENDPOINT=your-endpoint-url
   set AI_FOUNDRY_KEY=your-api-key

   # PowerShell
   $env:AI_FOUNDRY_ENDPOINT="your-endpoint-url"
   $env:AI_FOUNDRY_KEY="your-api-key"
   ```


Sucess Criteria:

