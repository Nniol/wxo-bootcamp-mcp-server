import asyncio

from src.hospital_data_server.hospital_data_tools import main


if __name__ == "__main__":
    print("Starting MCP server with SSE transport on http://localhost:8000")
    print("SSE endpoint: http://localhost:8000/sse")
    print("Messages endpoint: http://localhost:8000/messages")

    # Run the server
    asyncio.run(main())
