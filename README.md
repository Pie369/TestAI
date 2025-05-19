# Brave Search AI Agent with Pydantic AI and FastAPI

## Setup


```bash
1. Clone repository
git clone https://github.com/Pie369/TestAI.git
cd brave-search-ai-agent

2. Configure environment variables
Copy .env.example to .env and edit:

BRAVE_SEARCH_API_KEY=your_serpapi_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

3. Build Docker image
docker build -t brave-search-agent .

4. Run Docker container
docker run --env-file .env -p 8000:8000 brave-search-agent

5. Use in n8n
Create an HTTP Request node
Method: POST
URL: http://localhost:8000/search/
Body (JSON):
{
  "query": "Câu hỏi của bạn"
}

The server will respond with search results from Brave Search integrated AI Agent.
