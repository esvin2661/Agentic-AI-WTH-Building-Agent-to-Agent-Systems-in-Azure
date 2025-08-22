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
- Build Web Application to communicate with Agents.

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
- Python and Flask for implementation.

## Challenges

### Challenge 01: Setup
Prepare your development environment and Azure subscription.

### Challenge 02: Deploy Core Agents
Deploy the Monitor Agent, Anomaly Detector, Resource Optimizer, and Alert Manager using Durable Functions.

### Challenge 03: Enable Agentic Communication
Implement A2A protocols to allow agents to share state and delegate tasks.

### Challenge 04: Integrate Semantic Kernel
Use Semantic Kernel to enhance agent reasoning and decision-making.

### Challenge 05: Monitor and Visualize
Configure Azure Monitor and Application Insights to track agent activity and system health.

### Challenge 06: Simulate Anomalies
Trigger simulated anomalies and observe how agents respond and coordinate remediation.

## Technologies

This solution leverages the following Azure services and tools:

- Azure Durable Functions  
- Azure Monitor  
- Semantic Kernel  
- Application Insights  
- Python / Flask  

## Repository Structure

> *(Add your folders and file descriptions here, e.g., `/agents`, `/workflows`, `/docs`, etc.)*

## Prerequisites

- Active Azure Subscription with permissions to deploy resources.
- Familiarity with Python and Flask.
- Familiarity with Github and Github codespace

## Contributors

- Esvin Ruiz  

## License

MIT License. See `LICENSE` file for details.
