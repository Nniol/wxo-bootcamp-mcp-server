# Hospital Data MCP Server

A repo to manage an MCP server to enable access to the data set providing hospital data

The data is entirely made up and bears no linkage and or repsentation to any person.


### Running
Need two terminal:
>#### Terminal 1
> 1. ```cd src```
> 2. ```uv run -m hospital_data_server.app```   : Run the server
>#### Terminal 2
> 1. ```cd src```
> 2. ```npx @modelcontextprotocol/inspector```  : Run the inspector for testing


### Podman
You can do this for _Terminal 1_
 1. from root
 2. podman build .
 3. podman run -p 8080:8080 [Container ID]                              