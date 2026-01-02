# Gemini API Playground with Gradio

This project contains Python scripts for experimenting with Google's Gemini models using the Gradio library for web-based user interfaces. It includes a chat interface and simple streaming examples.

## Project Structure

* **`GradioVersion1.py`**: The main application. A robust Gradio interface that allows users to:
  * Select from a list of available Gemini/PaLM models.
  * View detailed attributes for each model (token limits, version, description).
  * Chat with the selected model (supports streaming responses).
  * *Note:* Model metadata is currently hardcoded as a Markdown string within this file.
* **`gemini_async.py`**: A standalone asynchronous script using the newer `google-genai` SDK to demonstrate streaming content generation from `gemini-2.5-pro`.
* **`gradiotest.py`**: A simplified or earlier version of the Gradio interface, primarily focused on parsing and displaying model attributes without the full chat integration of `GradioVersion1.py`.
* **`get_apikey.py`**: A utility script to inspect environment variables and verify that `GOOGLE_API_KEY` is set correctly.

## Available AI Models

The application supports various Gemini and PaLM models. Below is a summary of key models:

| Model | Token Limits (In/Out) | Description |
| :--- | :--- | :--- |
| **Gemini 1.5 Pro** | 2M / 8192 | Mid-size multimodal model, excellent for complex reasoning and large contexts. |
| **Gemini 1.5 Flash** | 1M / 8192 | Fast and versatile multimodal model, efficient for high-frequency tasks. |
| **Gemini 1.5 Flash-8B** | 1M / 8192 | Smallest, most cost-effective Flash model. |
| **PaLM 2 (Legacy)** | 8196 / 1024 | Legacy text-only model. |

*See `gemini-models_documentation.md` for a complete list of legacy and experimental models.*

## Setup & Requirements

### Prerequisites

* Python 3.x
* A Google Cloud API Key with access to Gemini models.

### Environment Variables

The application relies on the `GOOGLE_API_KEY` environment variable.

**Windows (PowerShell):**

```powershell
$env:GOOGLE_API_KEY="your_actual_api_key_here"
```

**Linux/macOS:**

```bash
export GOOGLE_API_KEY="your_actual_api_key_here"
```

### Installation

Install the required Python packages:

```bash
pip install gradio google-generativeai google-genai
```

## Usage

### Running the Main Chat Interface

To launch the full chat application:

```bash
python GradioVersion1.py
```

This will start a local Gradio server (usually at `http://127.0.0.1:7860`). Open this URL in your browser to interact with the models.

### Running the Async Streaming Test

To test simple async streaming in the terminal:

```bash
python gemini_async.py
```

### Verifying API Key

To check if your environment variables are readable:

```bash
python get_apikey.py
```

## Development Notes

* **Model Metadata:** The list of models and their attributes in `GradioVersion1.py` is hardcoded. If new models are released, that string needs to be manually updated.
* **SDK Usage:** The project currently mixes usage of `google.generativeai` (standard) and `google.genai` (newer). Future refactoring might aim to standardize on one SDK.
