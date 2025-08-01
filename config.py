"""
Configuration settings for AI Foundry API
"""
import os 
from foundry_sdk import FoundryClient
from sematic_kernel import Kernel 
from azure.identity import DefaultAzureCredential

AI_FOUNDRY = {
    "endpoint": "",
    "api_version": "2023-05-15",
    "api_key": ""
}