"""
Task 5-6-7 Part 1: File Summarizer Agent

Create an agent that can read files and provide concise summaries.
This agent will be used by other agents to quickly understand file contents.

Complete the TODOs below to implement the file summarizer.
"""

import os
from dotenv import load_dotenv
import langroid as lr
import langroid.language_models as lm
from langroid.agent.tools.orchestration import DoneTool
from file_tools import ReadFileTool

# Load environment variables from .env file
load_dotenv()

# Get model from environment, default to Gemini if not set
CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gemini-2.5-flash")


class FileSummarizerAgentConfig(lr.ChatAgentConfig):
    """Configuration for the file summarizer specialist agent."""
    
    # TODO 1: Set a descriptive name for the agent - NO SPACES!
    name: str = "file-summarize-agent"
    
    # TODO 2: Configure the LLM
    # Hint: Use lm.OpenAIGPTConfig with chat_model=CHAT_MODEL
    # and temperature=0.3 for consistent summaries
    llm: lm.OpenAIGPTConfig = lm.OpenAIGPTConfig(chat_model=CHAT_MODEL, temperature=0.3) # Replace with proper configuration

    # IMPORTANT: This nudges the LLM to use a tool when it forgets
    handle_llm_no_tool: str = f"""
    You forgot to use one of your TOOLs!. Remember that:
    - You must use `{ReadFileTool.name()}` to read file contents;
    - You should use `{DoneTool.name()}` to return your summary;    
    """

    # TODO 3: Write a system message that:
    # - Explains the agent is a file summarization specialist
    # - Mentions it must use ReadFileTool to read file contents
    # - Instructs to analyze content for main topics and key points
    # - IMPORTANT: Must use DoneTool to return the summary
    # Regarding naming the tools, note that  the agent is unaware of the class names of
    # the tools, so you have to get the `name()` method of the tool class to
    # get the actual name, e.g. `ReadFileTool.name()`.
    system_message: str = f"""
    You are a helpful file summarization agent that can help read file contents and then analyze the contents for main topics and key points
    After analyzing contents for main topics and key points return a summary.
    
    You have access to the following tools:
    `{ReadFileTool.name()}`:  Use this to read file contents.
    `{DoneTool.name()}`: Use this when your task is complete to return the final result.

    When your task is complete, you MUST use the `{DoneTool.name()}` tool to 
    indicate completion, and use the `content` field to return any response you wish to 
    provide. It is CRITICAL to use the `content` field to return any results 
    sought by the user, since they will NOT be able to see anything outside of this tool!
    """


def run_file_summarizer(file_path: str) -> str:
    """
    Create and run a file summarizer agent on a single file.
    
    Args:
        file_path: Path to the file to summarize
        
    Returns:
        A summary of the file contents
    """
    # TODO 4: Create the FileSummarizerAgentConfig
    config = FileSummarizerAgentConfig()  # Replace with config instance
    
    # TODO 5: Create the ChatAgent
    agent = lr.ChatAgent(config)  # Replace with agent instance
    
    # TODO 6: Enable the agent to use the tools it is required to use
    ... # your code here
    agent.enable_message(ReadFileTool)
    agent.enable_message(DoneTool)

    # TODO 7: Create a Task with interactive=False
    task = lr.Task(agent,interactive=False) # Replace with task instance
    
    # TODO 8: Create a prompt asking to summarize the file
    # Unlike the system message which is generic, this prompt is specific to the file
    prompt = f"Search the file: {file_path} and summarize the content and key points"  # Replace with your prompt
    # TODO 9: Run the task and get the result
    result = task.run(prompt)
    
    # TODO 10: Return the result content
    # Hint: result is a ChatDocument, so you can access its content
    return result.content


# TODO 11: Create and export the agent for use by other modules
# This allows the summarizer tool to import and use this agent
# Hint: Create a FileSummarizerAgentConfig, then a file_summarizer_agent
file_summarizer_agent = lr.ChatAgent(FileSummarizerAgentConfig()) # Replace with configured agent instance
# now enable the necessary tools on the agent (use enable_message method on the agent)
... # replace with your one-liner
file_summarizer_agent.enable_message(ReadFileTool)
file_summarizer_agent.enable_message(DoneTool)




