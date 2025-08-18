# What The Hack – Esvin: Agentic AI in Microsoft Azure

## Introduction

The Agentic AI What The Hack will guide you through designing and deploying multi-agent systems on Microsoft Azure. This systems autonomously monitors cloud infrastructure, detects anomalies, optimizes resources, and coordinates actions through Agent-to-Agent (A2A) communication.

This is a challenge-based hack. It's not step-by-step. Whether you're new to Azure or an experienced cloud architect, you'll find opportunities to learn, experiment, and innovate.

You’ll implement a distributed, intelligent system using Durable Functions, Semantic Kernel, and Azure Monitor, all orchestrated through a graph-based workflow of specialized agents.

And remember—coaches are here to help. Don’t hesitate to raise your hand!

## Learning Objectives

In this hack, you will:

- Design and deploy multi-agents architecture using Azure services.
- Implement autonomous monitoring and anomaly detection.
- Optimize cloud resource usage through intelligent scaling.
- Enable agent-to-agent communication for distributed decision-making.
- Monitor and visualize system behavior using Azure Monitor and Application Insights.

## Solution Architecture

The solution is composed of four core agents, each with a specific responsibility:

- Monitor Agent: Continuously observes cloud metrics and service health.
- Anomaly Detector: Uses statistical or ML models to identify unusual patterns.
- Resource Optimizer: Recommends or triggers scaling actions to improve efficiency.
- Alert Manager: Notifies stakeholders and initiates remediation workflows.

These agents communicate via A2A protocols, sharing insights and delegating tasks to maintain system resilience and performance.

The architecture is built using:

- Durable Functions for orchestrating agent workflows.
- Semantic Kernel for intelligent decision-making.
- Azure Monitor and Application Insights for observability.
- Python and TypeScript for implementation.

## Challenges

### Challenge 001: Setup
Prepare your development environment and Azure subscription.

#### Development Environment Setup

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

This will install all necessary packages including:
- Azure AI Foundry SDK and its components
- Azure Core libraries
- Required authentication and storage modules

### Challenge 002: Semantic Kernel Setup & Configuration

### Challenge 003: Build and Deploy Core Agents

### Challenge 004: Enable Agentic Communication (A2A)

### Challenge 005: Orchestrating Agent Collaboration with Semantic Kernel 

### Challenge 006: Monitor and Visualize

### Challenge 007: Simulate Anomalies  


## Technologies

This solution leverages the following Azure services and tools:

- Azure Durable Functions  
- Azure Monitor  
- Semantic Kernel  
- Application Insights  
- Python 

## Repository Structure

> *(Add your folders and file descriptions here, e.g., `/agents`, `/workflows`, `/docs`, etc.)*

## Prerequisites

- Active Azure Subscription with permissions to deploy resources.
- Familiarity with Python or TypeScript.
- Visual Studio Code with Azure Functions and Python extensions.

## Contributors

- Esvin Ruiz  

## License

MIT License. See `LICENSE` file for details.
