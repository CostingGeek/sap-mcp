# SAP-Claude Integration via MCP (Model Context Protocol)

> Connect Claude AI capabilities directly to your SAP systems through a seamless MCP integration

This repository contains a Python-based solution that enables bidirectional communication between Claude (Anthropic's large language model) and SAP systems via the SAP Graph API. By leveraging the Model Context Protocol (MCP), this integration allows Claude to retrieve and process SAP business data in real-time.

## Features

- Connect Claude to SAP systems with minimal setup
- Retrieve real-time sales order data from SAP via Graph API
- Extend the integration with additional SAP entities (Customers, Products, etc.)
- Process SAP data with the full capabilities of Claude's LLM

## Prerequisites

- Python 3.8+
- SAP API key (sandbox or production)
- Claude Desktop 
- Basic understanding of MCP and SAP Graph API

This documentation is written for a Windows environment with administrator rights

## Documentation
- [Get started with the Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction)
- [Introduction to SAP Graph](https://community.sap.com/t5/technology-blogs-by-sap/part-1-introduction-to-sap-graph/ba-p/13503946)

## Installation

1. Get the SAP API Key
Log into the [SAP Graph Navigator](https://api.sap.com/graph).
You will find the API key in your profile, under Settings > API Settings.
Save that API key as system environment variable "SAP_API_KEY".
Make sure to restart your machine to load the new environment variable.

3. Set up your environment
Let's follow the [Documentation for Server Developers](https://modelcontextprotocol.io/quickstart/server#importing-packages-and-setting-up-the-instance).

First, let’s install `uv` and set up our Python project and environment:
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Make sure to restart your terminal afterwards to ensure that the `uv` command gets picked up.

Now, let’s create and set up our project:
```bash
# Create a new directory for our project
uv init saptools
cd saptools

# Create virtual environment and activate it
uv venv
.venv\Scripts\activate

# Install dependencies
uv add mcp[cli] httpx requests

# Create our server file
new-item saptools.py
```

3. Building the server

Clone the `saptools.py` file into your own file.

4. Connect Claude Desktop with the MCP Server

Open Claude Studio. Under File > Settings > Developer, click `Edit Config`.
Edit the file `claude_desktop_config.json` usually located in the %APPDATA%\Claude folder.
Make sure to replace the `C:\\PATH\\TO\\PARENT\\FOLDER` with your own.

```bash
{
    "mcpServers": {
		    "saptools": {
            "command": "uv",
            "args": [
                "--directory",
                "C:\\PATH\\TO\\PARENT\\FOLDER",
                "run",
                "saptools.py"
            ]
        }
    }
}
``` 

Now, restart Claude Desktop to load the configuration. 
Note that by default, closing the Claude window only minimizes it to the system tray.
You will need to close it completely by right-clicking on the icon in the system tray and selecting Quit.
After restarting Claude, a new hammer icon should show in the chat window, that displays the number of active MCP tools.
Click on it to show the information popup, which should show:
**get_sales_orders**
Retrieve sales orders from SAP Graph API sandbox.
Args: top: Number of sales orders to retrieve (default: 3).
api_key: SAP API key (optional, will use environment variable if not provided)
Returns:String containing formatted sales order information

5. Test the MCP Server

You should now be ready to chat with your SAP system from Claude with prompts like:
```bash
Give me the last 10 sales orders
What is the average amount of the last 5 sales orders
``` 
This is of course limited at this point, but extensions to this proof-of-concept should support more complex interations,
like getting the last sales orders for a given customer.


## 🛠️ How It Works

This solution uses the Model Context Protocol (MCP) to create a bidirectional communication channel between Claude and SAP systems:

1. An MCP server is initialized using the FastMCP library
2. The server exposes SAP functionality as "tools" that Claude can invoke
3. When Claude needs to access SAP data, it calls the appropriate tool function
4. The function connects to SAP Graph API and returns formatted results
5. Claude processes the returned data and generates relevant insights

## 📊 Current Available Tools

### `get_sales_orders`

Retrieves sales order information from SAP Graph API.

Parameters:
- `top` (int, optional): Number of sales orders to retrieve (default: 3)
- `api_key` (str, optional): SAP API key (uses environment variable if not provided)

Example response:
```
Found 3 sales orders:

Order ID: 123456
Display ID: SO-123456
Sold To Party: ACME Corp
Net Amount: 5000.00 USD
Created At: 2024-10-12T15:30:00Z
----------------------------------------
Order ID: 123457
Display ID: SO-123457
Sold To Party: TechInnovations
Net Amount: 7500.00 USD
Created At: 2024-10-13T09:15:00Z
----------------------------------------
``` 
