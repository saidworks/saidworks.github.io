---
title: "Llama.cpp Guide: Model Management and Server Setup"
date: 2026-04-17
tags:
  - ai
  - inference
  - llm
categories:
  - AI
---

# Llama.cpp Guide: Model Management and Server Setup

This guide provides instructions for working with llama.cpp, a C++ port of Meta's LLaMA model that allows for efficient inference on various devices.

## Table of Contents
- [Pulling Models](#pulling-models)
- [Running a Model as a Server](#running-a-model-as-a-server)
- [Switching Between Models](#switching-between-models)
- [Integration with OpenWebUI](#integration-with-openwebui)

## Pulling Models

Llama.cpp works with GGML and GGUF format models. Here's how to obtain models for use with llama.cpp:

### 1. Download Pre-converted Models from Hugging Face

Many pre-converted models are available on Hugging Face:

```bash
# Using the Hugging Face CLI
huggingface-cli download TheBloke/Llama-2-7B-GGUF llama-2-7b.Q4_K_M.gguf --local-dir ./models

# Using wget or curl
wget https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q4_K_M.gguf -O ./models/llama-2-7b.Q4_K_M.gguf
```

### 2. Convert Original Meta Models

If you have access to the original Meta LLaMA models, you can convert them to GGUF format:

```bash
# Clone llama.cpp repository
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp

# Build the project
mkdir build && cd build
cmake .. && cmake --build . --config Release

# Convert the model (assuming original model is in ../models directory)
./bin/convert-llama-ggml-to-gguf /path/to/original/model ./models/converted-model.gguf
```

### 3. Choose the Right Quantization

Different quantization levels offer trade-offs between model size, memory usage, and performance:

| Quantization | Description |
|--------------|-------------|
| Q4_K_M       | Good balance of quality and size |
| Q5_K_M       | Better quality, larger size |
| Q8_0         | Higher quality, much larger size |

For example:
```bash
# Download a specific quantization level
wget https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q4_K_M.gguf -O ./models/llama-2-7b.Q4_K_M.gguf
```

## Running a Model as a Server

Llama.cpp includes a server mode that allows you to expose your model via a REST API:

### 1. Start the Server

To run a model as a server on port 11434 (which matches the Ollama default port):

```bash
# Navigate to llama.cpp directory
cd /path/to/llama.cpp

# Start the server with a specific port
./build/bin/llama-server -m ./models/llama-2-7b.Q4_K_M.gguf -p 11434
```

### 2. Server Command Parameters

Important server parameters:

| Parameter        | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-m, --model`    | Path to the model file                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `-p, --port`     | Port number (default: 8080)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `-h, --host`     | Host IP address (default: 127.0.0.1)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `-n, --parallel` | Number of parallel sequences to run                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `--ctx-size`     | Context window size                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `--threads`      | Number of threads to use during generation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `--n_gpu_layers` | Parameter in llama.cpp allows you to offload a specific number of transformer layers from the CPU to the GPU.<br/> This can significantly improve performance by leveraging the GPU's parallel processing capabilities, especially for large models.                                                                                                                                                                                                                                                                                                                                                                                 |
| `--temp`         | Temperature regulates the unpredictability of a language model's output. With higher temperature settings, <br/>outputs become more creative and less predictable as it amplifies the likelihood of less probable tokens while reducing that for more probable ones. Conversely, lower temperatures yield more conservative and predictable results.                                                                                                                                                                                                                                                                                 |
| `--top-p`        | Also known as Nucleus Sampling is a setting in language models that helps manage the randomness of their output. <br/>It works by establishing a probability threshold and then selecting tokens whose combined likelihood surpasses this limit.                                                                                                                                                                                                                                                                                                                                                                                     |
| `--top-k`        | https://cyrilzakka.github.io/llm-playbook/nested/topk.html                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `--swa-full`     | Flag is related to the Sliding Window Attention (SWA) optimization. When --swa-full is set to true, <br/>it disables the iSWA (incremental SWA) optimization, which can lead to the following effects: Increased Memory Usage: Using --swa-full=true requires more memory compared to the default setting (false). Slower Computation: The computation becomes slower because the optimization is turned off. However, this allows for certain advanced features like speculative decoding and cache reuse. Context Branching: It enables branching from older points in the context, which can be useful for specific applications. |
| `--no-mmproj`    | Flag disables the multimodal projector,<br/> likely preventing it from being used or offloaded to the GPU.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

Example with additional parameters:
```bash
./build/bin/llama-server -m ./models/llama-2-7b.Q4_K_M.gguf -p 11434 --ctx-size 4096 --threads 8
```

### 3. Testing the Server

You can test the server using curl:

```bash
curl -X POST http://localhost:11434/completion -d '{
  "prompt": "Hello, how are you?",
  "n_predict": 128
}'
```

The server supports the following endpoints:
- `/completion` - For text completion
- `/tokenize` - For tokenizing text
- `/embedding` - For generating embeddings

## Switching Between Models

You can switch between different models with llama.cpp in several ways:

### 1. Stop and Start Method

The simplest approach is to stop the current server and start a new one with a different model:

```bash
# Stop the current server (Ctrl+C in the terminal running the server)
# Then start a new server with a different model
./build/bin/llama-server -m ./models/different-model.gguf -p 11434
```

### 2. Running Multiple Servers

You can run multiple models simultaneously on different ports:

```bash
# Start the first model on port 11434
./build/bin/llama-server -m ./models/llama-2-7b.Q4_K_M.gguf -p 11434

# Start the second model on port 11435 (in a new terminal)
./build/bin/llama-server -m ./models/different-model.gguf -p 11435
```

### 3. Considerations When Switching Models

- **Memory management**: Unloading one model before loading another is important to avoid out-of-memory issues
- **Context window**: Different models may have different context window sizes
- **Performance**: Larger models require more computational resources

## Integration with OpenWebUI

OpenWebUI is a user-friendly interface that can work with llama.cpp server:

### 1. Install OpenWebUI

First, install OpenWebUI:

```bash
# Using pip
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install open-webui

# Using Docker
docker run -d \
  --name open-webui \
  -p 8080:8080 \
  -v open-webui-data:/app/backend/data \
  ghcr.io/open-webui/open-webui:latest
```

### 2. Configure OpenWebUI to Use llama.cpp Server

After installing OpenWebUI:

1. Start your llama.cpp server as described above
2. Open OpenWebUI in your browser (default: http://localhost:8080)
3. Navigate to Settings > API Connections
4. Add a new connection with the following details:
   - Name: llama.cpp
   - API Type: OpenAI Compatible
   - Base URL: http://localhost:11434/v1
   - API Key: (leave empty or use any placeholder value)
5. Save the connection and select it as your active model

### 3. Troubleshooting the Integration

- Ensure the llama.cpp server is running and accessible
- Check that the port numbers match between your server and OpenWebUI configuration
- If using Docker for OpenWebUI, ensure proper network configuration to allow it to communicate with the llama.cpp server
- For Windows users, ensure firewall settings allow the connections

### 4. Advanced Integration

For a more seamless experience, you can:

- Create a script to start both the llama.cpp server and OpenWebUI
- Configure OpenWebUI to automatically connect to the llama.cpp server on startup
- Set up reverse proxy (like Nginx) to serve both services under a single domain

## Additional Resources

- [Llama.cpp GitHub Repository](https://github.com/ggml-org/llama.cpp)
- [GGUF Model Format Documentation](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md)
- [OpenWebUI Documentation](https://github.com/open-webui/open-webui)
- [TheBloke's Quantized Models](https://huggingface.co/TheBloke)