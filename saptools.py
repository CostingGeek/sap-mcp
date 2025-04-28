from typing import Any
import httpx
import requests
import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("saptools")

@mcp.tool()
def get_sales_orders(top: int = 3, api_key: str = None) -> str:
    """
    Retrieve sales orders from SAP Graph API sandbox.
    
    Args:
        top: Number of sales orders to retrieve (default: 3)
        api_key: SAP API key (optional, will use environment variable if not provided)
    
    Returns:
        String containing formatted sales order information
    """
    try:
        # Get API key from parameter or environment variable
        SAP_API_KEY = api_key or os.environ.get('SAP_API_KEY')
        
        if not SAP_API_KEY:
            return "Error: No API key provided and SAP_API_KEY environment variable not set"
        
        # Sandbox URL with correct namespace
        API_URL = "https://sandbox.api.sap.com/sapgraph/sap.graph/SalesOrder"
        
        # Set up headers with API key authentication
        headers = {
            "apikey": SAP_API_KEY,  # Key name must be "apikey" (lowercase)
            "Accept": "application/json"
        }
        
        # Set up query parameters
        params = {
            "$top": top,
            "$select": "id,displayId,soldToParty,netAmount,netAmountCurrency,createdAt"
        }
        
        # Make the API request
        response = requests.get(API_URL, headers=headers, params=params)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Get JSON response
        sales_orders = response.json()
        
        if not sales_orders or "value" not in sales_orders:
            return "No sales orders found or invalid response"
        
        # Format the results
        result = f"Found {len(sales_orders['value'])} sales orders:\n\n"
        
        for order in sales_orders["value"]:
            result += f"Order ID: {order.get('id', 'N/A')}\n"
            result += f"Display ID: {order.get('displayId', 'N/A')}\n"
            result += f"Sold To Party: {order.get('soldToParty', 'N/A')}\n"
            result += f"Net Amount: {order.get('netAmount', 'N/A')} {order.get('netAmountCurrency', 'N/A')}\n"
            result += f"Created At: {order.get('createdAt', 'N/A')}\n"
            result += "-" * 40 + "\n"
        
        return result
        
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}\nResponse content: {http_err.response.text}"
    except requests.exceptions.RequestException as err:
        return f"Error occurred during request: {err}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')