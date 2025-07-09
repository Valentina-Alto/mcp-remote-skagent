import os
import chainlit as cl
from dotenv import load_dotenv
from datetime import datetime

from semantic_kernel import Kernel
from semantic_kernel.functions import KernelArguments
from semantic_kernel.contents import ChatHistory
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import AzureChatPromptExecutionSettings
from semantic_kernel.connectors.mcp import MCPSsePlugin

load_dotenv(dotenv_path=r"C:\Users\vaalt\OneDrive\Desktop\Projects\github\mcp-mslearn-skagent\.env", override=True)

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Global agent
agent: ChatCompletionAgent = None
agent_thread: ChatHistoryAgentThread = None

@cl.on_chat_start
async def start_chat():
    global agent, agent_thread

    kernel = Kernel()

    service = AzureChatCompletion(
        deployment_name=AZURE_OPENAI_DEPLOYMENT,
        api_key=AZURE_OPENAI_API_KEY,
        endpoint=AZURE_OPENAI_ENDPOINT,
        service_id="chainlit-assistant"
    )
    kernel.add_service(service)

    settings = AzureChatPromptExecutionSettings()
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    history = ChatHistory()
    history.add_system_message("You are a helpful assistant.")
    agent_thread = None

    # MCP plugin
    mcp_plugin = MCPSsePlugin(
        name="CoinGecko",
        description="Access real-time crypto prices via CoinGecko MCP.",
        url="https://mcp.api.coingecko.com/sse",
        load_tools=True,
        load_prompts=True
    )
    await mcp_plugin.connect()
    kernel.add_plugin(mcp_plugin, plugin_name="CoinGecko")

    agent = ChatCompletionAgent(
        kernel=kernel,
        name="Assistant",
        instructions="You are a helpful assistant using the CoinGecko plugin when needed."
    )

    await cl.Message(content="Hi! Ask me anything about crypto or general topics.").send()


@cl.on_message
async def handle_message(message: cl.Message):
    global agent, agent_thread

    arguments = KernelArguments(now=datetime.now().strftime("%Y-%m-%d %H:%M"))

    async for response in agent.invoke(messages=message.content, thread=agent_thread, arguments=arguments):
        await cl.Message(content=str(response.content)).send()
        agent_thread = response.thread
