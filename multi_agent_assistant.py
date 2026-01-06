"""
Task 5-6-7 Part 3: Multi-Agent File Assistant

Create the main orchestrator agent that coordinates multiple specialized agents
to handle complex file operations. This agent uses both FileSearchTool and
FileSummarizerTool to fulfill user requests.

Complete the TODOs below to implement the multi-agent assistant.
"""

import os
from dotenv import load_dotenv
import langroid as lr
import langroid.language_models as lm
from langroid.agent.tools.orchestration import DoneTool
from file_tools import ListDirTool, ReadFileTool, WriteFileTool
from search_tool import FileSearchTool
# TODO 1: Import the tool classes from modules in this folder:
#  FileSearchTool, FileSummarizerTool,
#  ListDirTool, ReadFileTool, WriteFileTool
from summarizer_tool import FileSummarizerTool
# Load environment variables from .env file
load_dotenv()

# Get model from environment, default to Gemini if not set
CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gemini-2.5-flash")


class MultiAgentFileAssistantConfig(lr.ChatAgentConfig):
    """Configuration for the main multi-agent file assistant."""
    
    # TODO 2: Set a descriptive name for the orchestrator agent - NO SPACES!
    name: str = "orchestrator-assistant"
    
    # TODO 3: Configure the LLM
    # Hint: Use lm.OpenAIGPTConfig with chat_model=CHAT_MODEL
    # and temperature=0.1 for consistent behavior
    llm: lm.OpenAIGPTConfig = lm.OpenAIGPTConfig(chat_model=CHAT_MODEL, temperature=0.1) # Replace with proper configuration

    # TODO 4: Remind LLM about using tools
    # IMPORTANT -- this nudges the assistant to use tools when it forgets
    handle_llm_no_tool: str = f"""
    You FORGOT to use one of your TOOLs! Remember that:
    - TODO one-liners mentioning each of the 5 tools available and when to use them:
    """

    # TODO 5: Write a comprehensive system message that:
    # - Explains this is the main file assistant that helps a user with
    #   requests about files.
    # - Describe when to use each tool:
    #   * Specialized tools: FileSearchTool, FileSummarizerTool
    #   * WriteFileTool
    #   * DoneTool (IMPORTANT: mention using this when task is complete)
    # - Provides guidance on handling complex requests:
    #   * Break down complex tasks into steps
    # - IMPORTANT: Require that it must use DoneTool.name() when task is complete
    # - Note - do not change the last CRITICAL note about using one tool at a time!
    system_message: str = f"""
    You are the main file assistant that can help a user with requests about files.

    You have access to the following tools:
    `{FileSearchTool.name()}`: Use this tool to search for the file
    `{FileSummarizerTool.name()}`: Use this tool to search for the file
    `{WriteFileTool.name()}`: Use this tool to write contents to the file
    `{DoneTool.name()}`: Use this when your task is complete to return the final result.
    
    
    CRITICAL: You CANNOT use multiple tools at once! You must use ONE tool at a time,
        wait for the result, and THEN decide what to do next.

    When your task is complete, you MUST use the `{DoneTool.name()}` tool to 
    indicate completion, and use the `content` field to return any response you wish to 
    provide. It is CRITICAL to use the `content` field to return any results 
    sought by the user, since they will NOT be able to see anything outside of this tool!
    """


def run_multi_agent_assistant(prompt: str) -> str:
    """
    Create and run the multi-agent file assistant.
    
    Args:
        prompt: The user's request
        
    Returns:
        The assistant's response after coordinating with specialized agents
    """
    # TODO 6: Create the MultiAgentFileAssistantConfig
    config = MultiAgentFileAssistantConfig()  # Replace with config instance
    
    # TODO 7: Create the ChatAgent
    agent = lr.ChatAgent(config)  # Replace with agent instance
    
    # TODO 8: Enable the agent to use all required tools
    ... # your code here
    agent.enable_message(FileSummarizerTool)
    agent.enable_message(FileSearchTool)
    agent.enable_message(WriteFileTool)
    agent.enable_message(DoneTool)

    # TODO 9: Create a Task with interactive=False
    task = lr.Task(agent,interactive=False)  # Replace with task instance
    
    # TODO 10: Run the task with the prompt
    # Note: No need to specify turns when using DoneTool
    result = task.run(prompt)  # Replace with code that runs task
    
    # TODO 11: Return the result
    # Hint: result is of type ChatDocument, which has a content attribute of type str
    return result.content


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     # Test complex request that needs multiple agents
#     response = run_multi_agent_assistant(
#         "Find all files about music and give me a summary of each one"
#     )
#     print("Multi-agent response:")
#     print(response)
#     
#     # Test another complex request
#     response = run_multi_agent_assistant(
#         "Search for finance-related files and create a summary report in myfiles/finance_summary.txt"
#     )
#     print("\nFinance summary response:")
#     print(response)