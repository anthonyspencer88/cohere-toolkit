import logging
import os
from distutils.util import strtobool
from enum import StrEnum

from backend.schemas.tool import Category, ManagedTool
from backend.tools import (
    Calculator,
    GoogleDrive,
    GoogleDriveAuth,
    LangChainWikiRetriever,
    PythonInterpreter,
    ReadFileTool,
    SearchFileTool,
    WebScrapeTool,
    TavilyInternetSearch,
    OktaDocumentRetriever,
    SearchPendingOrders,
    ExtractVerificationSteps,
    SendReminderEmails
)

"""
List of available tools. Each tool should have a name, implementation, is_visible and category. 
They can also have kwargs if necessary.

You can switch the visibility of a tool by changing the is_visible parameter to True or False. 
If a tool is not visible, it will not be shown in the frontend.

If you want to add a new tool, check the instructions on how to implement a retriever in the documentation.
Don't forget to add the implementation to this AVAILABLE_TOOLS dictionary!
"""


class ToolName(StrEnum):
    Okta_Retriever = OktaDocumentRetriever.NAME
    Wiki_Retriever_LangChain = LangChainWikiRetriever.NAME
    Tavily_Internet_Search = TavilyInternetSearch.NAME
    Search_File = SearchFileTool.NAME
    Read_File = ReadFileTool.NAME
    Python_Interpreter = PythonInterpreter.NAME
    Calculator = Calculator.NAME
    Google_Drive = GoogleDrive.NAME
    Web_Scrape = WebScrapeTool.NAME
    Search_Pending_Orders = SearchPendingOrders.NAME
    Extract_Verification_Steps = ExtractVerificationSteps.NAME
    Send_Reminder_Emails = SendReminderEmails.NAME


ALL_TOOLS = {
    ToolName.Send_Reminder_Emails: ManagedTool(
        display_name="Send Reminder Emails",
        implementation=SendReminderEmails,
        parameter_definitions={
            "customer_info": {
            "description": "List of customer information including their names and email addresses.",
            "type": "list",
            "required": True
            },
            "verification_steps": {
            "description": "List of steps required for account verification.",
            "type": "list",
            "required": True
            },
            "summary": {
            "description": "Summary of the verification process.",
            "type": "str",
            "required": True
            }
        },
        is_visible=True,
        is_available=SendReminderEmails.is_available(),
        error_message="SendReminderEmails is not available.",
        category=Category.DataLoader,
        description="Sends reminder emails to customers with pending orders, including instructions on how to complete their verification.",
    ),

    ToolName.Extract_Verification_Steps: ManagedTool(
        display_name="Extract Verification Steps",
        implementation=ExtractVerificationSteps,
        parameter_definitions={},
        is_visible=True,
        is_available=ExtractVerificationSteps.is_available(),
        error_message="ExtractVerificationSteps is not available.",
        category=Category.DataLoader,
        description="Extracts and summarizes the steps required for user account verification from the user onboarding documentation..",
    ),

    ToolName.Search_Pending_Orders: ManagedTool(
        display_name="Search Pending Orders",
        implementation=SearchPendingOrders,
        parameter_definitions={
            "status": {
                "description": "The status of the orders to search for (e.g., 'pending verification', 'completed', etc.)",
                "type": "str",
                "required": True,
            }
        },
        is_visible=True,
        is_available=SearchPendingOrders.is_available(),
        error_message="SearchPendingOrders is not available.",
        category=Category.DataLoader,
        description="Searches the order management database and returns a list of customers with orders having the specified status.",
    ),

    ToolName.Okta_Retriever: ManagedTool(
        display_name="Okta Retriever",
        implementation=OktaDocumentRetriever,
        parameter_definitions={
            "query": {
                "description": "Query for retrieval from Okta documentation.",
                "type": "str",
                "required": True,
            }
        },
        is_visible=False,
        is_available=OktaDocumentRetriever.is_available(),
        error_message="OktaDocumentRetriever is not available, please make sure to set the COHERE_API_KEY environment variable and that the FAISS docstore is connected.",
        category=Category.DataLoader,
        description="Returns documentation from the Okta product documentation website.",
    ),
    ToolName.Tavily_Internet_Search: ManagedTool(
        display_name="Web Search",
        implementation=TavilyInternetSearch,
        parameter_definitions={
            "query": {
                "description": "Query for retrieval.",
                "type": "str",
                "required": True,
            }
        },
        is_visible=True,
        is_available=TavilyInternetSearch.is_available(),
        error_message="TavilyInternetSearch not available, please make sure to set the TAVILY_API_KEY environment variable.",
        category=Category.DataLoader,
        description="Returns a list of relevant document snippets for a textual query retrieved from the internet using Tavily.",
    ),
    ToolName.Search_File: ManagedTool(
        display_name="Search File",
        implementation=SearchFileTool,
        parameter_definitions={
            "search_query": {
                "description": "Textual search query to search over the file's content for",
                "type": "str",
                "required": True,
            },
            "filenames": {
                "description": "A list of one or more uploaded filename strings to search over",
                "type": "list",
                "required": True,
            },
        },
        is_visible=True,
        is_available=SearchFileTool.is_available(),
        error_message="SearchFileTool not available.",
        category=Category.DataLoader,
        description="Performs a search over a list of one or more of the attached files for a textual search query",
    ),
    ToolName.Read_File: ManagedTool(
        display_name="Read Document",
        implementation=ReadFileTool,
        parameter_definitions={
            "filename": {
                "description": "The name of the attached file to read.",
                "type": "str",
                "required": True,
            }
        },
        is_visible=True,
        is_available=ReadFileTool.is_available(),
        error_message="ReadFileTool not available.",
        category=Category.FileLoader,
        description="Returns the textual contents of an uploaded file, broken up in text chunks.",
    ),
    ToolName.Python_Interpreter: ManagedTool(
        display_name="Python Interpreter",
        implementation=PythonInterpreter,
        parameter_definitions={
            "code": {
                "description": "Python code to execute using an interpreter",
                "type": "str",
                "required": True,
            }
        },
        is_visible=True,
        is_available=PythonInterpreter.is_available(),
        error_message="PythonInterpreterFunctionTool not available, please make sure to set the PYTHON_INTERPRETER_URL environment variable.",
        category=Category.Function,
        description="Runs python code in a sandbox.",
    ),
    ToolName.Wiki_Retriever_LangChain: ManagedTool(
        display_name="Wikipedia",
        implementation=LangChainWikiRetriever,
        parameter_definitions={
            "query": {
                "description": "Query for retrieval.",
                "type": "str",
                "required": True,
            }
        },
        kwargs={"chunk_size": 300, "chunk_overlap": 0},
        is_visible=True,
        is_available=LangChainWikiRetriever.is_available(),
        error_message="LangChainWikiRetriever not available.",
        category=Category.DataLoader,
        description="Retrieves documents from Wikipedia using LangChain.",
    ),
    ToolName.Calculator: ManagedTool(
        display_name="Calculator",
        implementation=Calculator,
        parameter_definitions={
            "code": {
                "description": "The expression for the calculator to evaluate, it should be a valid mathematical expression.",
                "type": "str",
                "required": True,
            }
        },
        is_visible=True,
        is_available=Calculator.is_available(),
        error_message="Calculator tool not available.",
        category=Category.Function,
        description="This is a powerful multi-purpose calculator which is capable of a wide array of math calculations.",
    ),
    ToolName.Google_Drive: ManagedTool(
        display_name="Google Drive",
        implementation=GoogleDrive,
        parameter_definitions={
            "query": {
                "description": "Query to search Google Drive documents with.",
                "type": "str",
                "required": True,
            }
        },
        is_visible=False,
        is_available=GoogleDrive.is_available(),
        auth_implementation=GoogleDriveAuth,
        error_message="Google Drive not available, please enable it in the GoogleDrive tool class.",
        category=Category.DataLoader,
        description="Returns a list of relevant document snippets for the user's google drive.",
    ),
    ToolName.Web_Scrape: ManagedTool(
        name=ToolName.Web_Scrape,
        display_name="Web Scrape",
        implementation=WebScrapeTool,
        parameter_definitions={
            "url": {
                "description": "The url to scrape.",
                "type": "str",
                "required": True,
            },
            "query": {
                "description": "The query to use to select the most relevant passages to return. Using an empty string will return the passages in the order they appear on the webpage",
                "type": "str",
                "required": False,
            },
        },
        is_visible=True,
        is_available=WebScrapeTool.is_available(),
        error_message="WebScrapeTool not available.",
        category=Category.DataLoader,
        description="Scrape and returns the textual contents of a webpage as a list of passages for a given url.",
    ),
}


def get_available_tools() -> dict[ToolName, dict]:
    langchain_tools = [ToolName.Python_Interpreter, ToolName.Tavily_Internet_Search]
    use_langchain_tools = bool(
        strtobool(os.getenv("USE_EXPERIMENTAL_LANGCHAIN", "False"))
    )
    use_community_tools = bool(strtobool(os.getenv("USE_COMMUNITY_FEATURES", "False")))

    if use_langchain_tools:
        return {
            key: value for key, value in ALL_TOOLS.items() if key in langchain_tools
        }

    tools = ALL_TOOLS.copy()
    if use_community_tools:
        try:
            from community.config.tools import COMMUNITY_TOOLS

            tools = ALL_TOOLS.copy()
            tools.update(COMMUNITY_TOOLS)
        except ImportError:
            logging.warning("Community tools are not available. Skipping.")

    for tool in tools.values():
        # Conditionally set error message
        tool.error_message = tool.error_message if not tool.is_available else None
        # Retrieve name
        tool.name = tool.implementation.NAME

    return tools


AVAILABLE_TOOLS = get_available_tools()
