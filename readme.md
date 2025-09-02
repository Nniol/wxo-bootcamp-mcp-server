# Hospital Data MCP Server

A repo to manage an MCP server to enable access to the data set providing hospital data

The data is entirely made up and bears no linkage and or repsentation to any person.


### Running: SSE
Need two terminal:
>#### Terminal 1
> 1. ```cd src```
> 3. ```uv run -m hospital_data_server.app_sse```   : Run the SSE server
>#### Terminal 2
> 1. ```cd src```
> 2. ```npx @modelcontextprotocol/inspector```  : Run the inspector for testing

### Running: STDIO
#### Terminal
 1. ```npx @modelcontextprotocol/inspector```  : Run the inspector for testing
 2. Use the following setup:
    - Transport Type: ```STDIO```  
    - Command: ```uv run -m hospital_data_server.app_stdio```
    - Arguments: ```--no-banner``` 



### Podman
You can do this for _Terminal 1_
 1. from root
 2. podman build .
 3. podman run -p 8080:8080 [Container ID]                              


# Deploy to a TechZone zone Code Engine  

Pre Reqs:
> - You will need to build the image locally
> - You will need a cloud account with a container registry you can write too
> - Install ibmcloud cli (https://cloud.ibm.com/docs/containers?topic=containers-cli-install)
> - Run the following commands:
>   - ibmcloud plugin install container-registry -r 'IBM Cloud'   
>   - ibmcloud plugin install ce

## Use an external IBM Cloud Container Registry

### Account A (The one with the Container Registry)
- $ibmcloud login -a https://cloud.ibm.com --sso
  - Choose the account with the Container Registry
- $ibmcloud cr login
- $ibmcloud cr namespace-add [NAMESPACE]
- $podman tag wxo-bootcamp-mcp-sever us.icr.io/[NAMESPACE]/[IMAGE_NAME]:[TAG] 
- $podman push us.icr.io/[NAMESPACE]/[IMAGE_NAME]:[TAG] 
- $ibmcloud iam service-id-create [SERVICE_ID_NAME] --description "Service ID for cross-account Container Registry access"
- $ibmcloud iam service-policy-create [SERVICE_ID_NAME] --roles Reader --service-name container-registry
- $ibmcloud iam service-api-key-create [API_KEY_NAME] [SERVICE_ID_NAME] --description "API key for cross-account registry access" --file api-key.json
- To view the API Key and get [API_KEY_VALUE]
  - $cat api-jey.json

### Account B (The techzone one with the Code Engine)
- $ibmcloud login -a https://cloud.ibm.com --sso
  - Choose the account with the Techzone Account
- $ibmcloud ce login
- $ibmcloud ce project select -n [PROJECT NAME]
  - The project name is visible in the Code Engine page
- $ibmcloud ce registry create --name [REGISTRY_SECRET_NAME]  --server us.icr.io --username iamapikey --password [API_KEY_VALUE]
- $ibmcloud ce application create --name [APP_NAME] --image us.icr.io/[NAMESPACE]/[IMAGE_NAME]:[TAG] --registry-secret [REGISTRY_SECRET_NAME] 

## Use everything on the Techzone instance
- $ibmcloud login -a https://cloud.ibm.com --sso
  - Choose the account with the Techzone Account
- $ibmcloud ce login
- $ibmcloud cr login
- $podman tag wxo-bootcamp-mcp-sever us.icr.io/[NAMESPACE]/[IMAGE_NAME]:[TAG] 
  - The [NAMESPACE] is the only one available when you look at Container Registry in the techzone instance. You do not need to create one
- $podman push us.icr.io/[NAMESPACE]/[IMAGE_NAME]:[TAG] 
- $ibmcloud iam api-key-create [API_KEY_NAME] --d "Tech Zone Code Engine registry access"                                
- $ibmcloud ce registry create -name [REGISTRY_SECRET_NAME] --server us.icr.io --username iamapikey --password [API_KEY_VALUE]
  - THE [API_KEY_VALUE] will be available from the previous command
- $ibmcloud ce application create --name [APP_NAME] --image us.icr.io/[NAME_SPACE]/[IMAGE_NAME]:[TAG] --registry-secret [REGISTRY_SECRET_NAME]  
- $ibmcloud ce project select -n [PROJECT NAME]


# Test using MCP Inspector
 - $npx @modelcontextprotocol/inspector
 - Use the URL for the application (from Code Endgine) and append /sse as the URL
  - https://[APP_NAME].[IBM_CLOUD_URL_PART]/sse

