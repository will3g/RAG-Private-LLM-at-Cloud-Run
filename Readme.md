# Private LLM into Cloud Run

Deploy a secure, scalable and cost-efficient private Large Language Model (LLM) instance using Google Cloud Run.

## Project Overview

This project provisions a **fully private Ollama-based LLM inference server** (using models like LLaMA 3, Deepseek...) in **Google Cloud Run**, ideal for:
- Internal tools
- Private chatbots
- News analysis
- Content generation

## Architecture

- **Google Cloud Run**: Serverless deployment
- **Artifact Registry**: Stores Docker images
- **Cloud Build**: Builds the container image
- **IAM**: Configured for secure access
- **Min Scale: 0**: Pay only when in use
- **Concurrency: 8**: Handles multiple simultaneous requests

## Prerequisites

- Google Cloud account with billing enabled
- `gcloud` CLI installed
- **IAM permissions** to create and deploy resources
- **Dockerfile** and **deploy.yaml** available

## Quick Start

1. **Clone this repository**
   ```bash
   git clone https://github.com/YOUR-ORG/private-llm-cloudrun.git
   cd private-llm-cloudrun
   ```

2. **Update variables in Makefile**

    2.1 - Set your **PROJECT_ID**

    2.2 - Set your **EMAIL**
    
    2.3 - Set your final **ENDPOINT**

3. **Provision resources**
    ```bash
    make setup
    ```

4. **Deploy the service**
    ```bash
    make deploy
    ```

5. **Test the endpoint**
    ```bash
    make test
    ```

## Estimated Cost
- **~$23/month** with minimal usage (approx. **2h/day**).

- Costs scale automatically with demand.

- Full-time usage **(24/7) would be around ~$280/month**.

## Security
- Cloud Run services are private by default.

- Authentication via Identity Token.

- IAM roles strictly enforced for service accounts.

## Roadmap
1. Add automatic scaling configuration

2. Add optional HTTPS custom domain

3. Support for multiple models

4. Add vector database integration (e.g., ChromaDB, Pinecone)