"""
Task 5-6-7 Part 2: File Summarizer Tool

Wrap the FileSummarizerAgent as a tool that can be used by other agents.
This enables delegation - other agents can ask for file summaries.

Complete the TODOs below to implement the summarizer tool.
"""

import langroid as lr
from langroid.pydantic_v1 import Field
# TODO 1: Import the file_summarizer_agent from file_summarizer_agent.py
from file_summarizer_agent import file_summarizer_agent


class FileSummarizerTool(lr.ToolMessage):
    """Tool to summarize file contents by delegating to FileSummarizerAgent."""
    
    # TODO 2: Set the request name for this tool
    # This is what other agents will use to invoke this tool
    request: str = "file-summarize"
    
    # TODO 3: Add a clear purpose description
    purpose: str = "The purpose of this tool is to summarize files"  # What does this tool do?
    
    # TODO 4: Add a file_path field with description
    file_path: str = Field(
        ...,
        description = "The file path to summarize contents from"
    )
    
    def handle(self) -> str:
        """Summarize a file by delegating to FileSummarizerAgent."""
        # TODO 5: Create a Task with the file_summarizer_agent that you imported
        # Set interactive=False
        task = lr.Task(file_summarizer_agent,interactive=False)  # Replace with lr.Task instance
        
        # TODO 6: Create a prompt for the agent
        # Hint: f"Please summarize the file: {self.file_path}"
        prompt = f"Please summarize the file: {self.file_path}"  # Replace with your prompt
        
        # TODO 7: Run the task and get the result
        # Hint: Use task.run(prompt, turns=3) to allow multiple tool uses
        result = task.run(prompt,turns=3)  # Replace with task.run(prompt, turns=3)
        
        # TODO 8: Return the content from the result
        # Hint: Result is of type ChatDocument, which has a content field of type str
        return result.content