import asyncio

from hosptial_data_set_server import main


if __name__ == "__main__":
    print("Starting MCP server with SSE transport on http://localhost:8000")
    print("SSE endpoint: http://localhost:8000/sse")
    print("Messages endpoint: http://localhost:8000/messages")

    # Run the server
    asyncio.run(main())
