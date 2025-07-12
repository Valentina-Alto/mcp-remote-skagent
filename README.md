# MCP Microsoft Learn Semantic Kernel Agent

A conversational AI assistant built with Microsoft's Semantic Kernel that integrates with Microsoft Learn documentation through the Model Context Protocol (MCP). This application provides real-time access to Microsoft's official documentation and can answer questions about Microsoft technologies, Azure services, and development practices.

## Features

- 🤖 **Conversational AI Assistant**: Interactive chat interface powered by Azure OpenAI
- 📚 **Microsoft Learn Integration**: Direct access to Microsoft's official documentation via MCP
- 🔌 **Model Context Protocol**: Seamless integration with external data sources
- ⚡ **Real-time Responses**: Streaming responses for better user experience
- 🛡️ **Azure OpenAI**: Enterprise-grade AI with built-in safety features


## Prerequisites

- Python 3.8 or higher
- Azure OpenAI Service account and API key

## Usage

### Running the Application

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Wait for initialization**:
   The application will display initialization messages:
   ```
   ⏳ Initializing Assistant...
   🔌 Connecting to MCP plugin manually...
   ✅ MCP plugin connected.
   🔧 MCP plugin registered with kernel.
   ✅ Assistant is ready! Type 'exit' to stop.
   ```

3. **Start chatting**:
   ```
   User:> What is Azure Functions?
   ```

4. **Exit the application**:
   Type `exit` to gracefully shut down the application.

### Example Interactions

```
User:> What is Azure Functions?
[Assistant provides detailed information about Azure Functions from Microsoft Learn]

User:> How do I deploy a web app to Azure?
[Assistant provides step-by-step deployment guidance]

User:> What are the best practices for Azure security?
[Assistant shares security best practices from official documentation]
```

### Key Components

- **Semantic Kernel**: Core AI orchestration framework
- **Azure OpenAI Service**: Large language model provider
- **MCP Plugin**: Connects to Microsoft Learn documentation
- **Chat Agent**: Manages conversation flow and context


