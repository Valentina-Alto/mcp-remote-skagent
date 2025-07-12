import asyncio
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.mcp import MCPStdioPlugin
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import KernelArguments
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import AzureChatPromptExecutionSettings
from datetime import datetime
import sys
from semantic_kernel.connectors.mcp import MCPSsePlugin, MCPStreamableHttpPlugin


# -------------------------------
# Configuration and Environment Setup
# -------------------------------
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv(dotenv_path=r"C:\Users\vaalt\OneDrive\Desktop\Projects\github\mcp-mslearn-skagent\.env", override=True)

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")
AZURE_OPENAI_PROMPT = os.getenv("AZURE_OPENAI_PROMPT")

async def main():

    print("⏳ Initializing Assistant...")

    # Initialize Semantic Kernel
    kernel = Kernel()
    service = AzureChatCompletion(
        deployment_name=AZURE_OPENAI_DEPLOYMENT,
        api_key=AZURE_OPENAI_API_KEY,
        endpoint=AZURE_OPENAI_ENDPOINT,
        service_id="my-service-id",
    )
    kernel.add_service(service)

    settings = AzureChatPromptExecutionSettings()
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    history = ChatHistory()
    thread: ChatHistoryAgentThread = None
    history.add_system_message("You are an AI assistant.")

    # Create and manually connect the MCP plugin
    print("🔌 Connecting to MCP plugin manually...")
    mcp_plugin = MCPStreamableHttpPlugin(
        name="CoinGecko",
        description="Access trusted and up-to-date information directly from Microsoft's official documentation.",
        url="https://learn.microsoft.com/api/mcp",
        load_tools=True,
        load_prompts=True
    )

    try:
        await mcp_plugin.connect()
        print("✅ MCP plugin connected.")
        kernel.add_plugin(mcp_plugin, plugin_name="MSLearn")
        print("🔧 MCP plugin registered with kernel.")
    except Exception as e:
        print(f"❌ Error: Could not register the MCP plugin: {str(e)}")
        await mcp_plugin.close()
        sys.exit(1)

    agent = ChatCompletionAgent(
        kernel=kernel,
        name="Assistant",
        instructions="You are a helpful assistant."
    )

    print("✅ Assistant is ready! Type 'exit' to stop.")

    try:
        while True:
            user_input = input("User:> ")
            if not user_input:
                continue
            if user_input.lower() == "exit":
                break

            arguments = KernelArguments(now=datetime.now().strftime("%Y-%m-%d %H:%M"))

            async for response in agent.invoke(messages=user_input, thread=thread, arguments=arguments):
                print(f"{response.content}")
                thread = response.thread
    finally:
        print("🛑 Shutting down MCP plugin...")
        await mcp_plugin.close()
        print("🔒 MCP plugin closed.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting the Assistant. Goodbye!")
    except Exception as e:
        print(f"\nError: {str(e)}")
