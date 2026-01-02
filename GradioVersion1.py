import gradio as gr
import re
import os
import time # For the dummy bot in case API fails
import google.generativeai as genai

# --- Configuration ---
# IMPORTANT: Set your GOOGLE_API_KEY environment variable,
# or replace "YOUR_API_KEY" with your actual key.
# Example: os.environ["GOOGLE_API_KEY"] = "YOUR_ACTUAL_GOOGLE_API_KEY"
# If you directly paste your key, uncomment the line below and replace YOUR_API_KEY:
# genai.configure(api_key="YOUR_API_KEY")

# Attempt to configure from environment variable first
try:
    # Check if the API key is already configured (e.g., by a previous run or external setup)
    # The genai library might not have a direct way to check if it's configured
    # without making a call, so we rely on the os.getenv check primarily.
    api_key_to_use = os.getenv("GOOGLE_API_KEY")
    if api_key_to_use:
        genai.configure(api_key=api_key_to_use)
        print("Google GenAI SDK configured with GOOGLE_API_KEY from environment variable.")
    elif hasattr(genai, 'api_key') and genai.api_key and "YOUR_API_KEY" not in str(genai.api_key) : # Check if already set by previous configure call
        print("Google GenAI SDK seems to be already configured.")
    else:
        # Fallback or instruction if key is not found and not already configured
        print("WARNING: GOOGLE_API_KEY environment variable not found or is a placeholder.")
        print("Please set it or configure genai.configure(api_key='YOUR_API_KEY') directly in the code.")
        # To allow the app to run without a key for UI testing, we won't raise an error here.
        # The chat function will handle the missing key.
except Exception as e:
    print(f"Error during Google GenAI SDK configuration: {e}")
    print("Chat functionality with actual models may not work.")


# The markdown content provided by the user
markdown_text = """
# AI Model Information

This document lists various AI models with their details.

## Model: models/chat-bison-001
- **Display Name:** PaLM 2 Chat (Legacy)
- **Description:** A legacy text-only model optimized for chat conversations
- **Version:** 001
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 4096
- **Output Token Limit:** 1024
- **Supported Actions:** `generateMessage`, `countMessageTokens`

## Model: models/text-bison-001
- **Display Name:** PaLM 2 (Legacy)
- **Description:** A legacy model that understands text and generates text as an output
- **Version:** 001
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 8196
- **Output Token Limit:** 1024
- **Supported Actions:** `generateText`, `countTextTokens`, `createTunedTextModel`

## Model: models/embedding-gecko-001
- **Display Name:** Embedding Gecko
- **Description:** Obtain a distributed representation of a text.
- **Version:** 001
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 1024
- **Output Token Limit:** 1
- **Supported Actions:** `embedText`, `countTextTokens`

## Model: models/gemini-1.0-pro-vision-latest
- **Display Name:** Gemini 1.0 Pro Vision
- **Description:** The original Gemini 1.0 Pro Vision model version which was optimized for image understanding. Gemini 1.0 Pro Vision was deprecated on July 12, 2024. Move to a newer Gemini version.
- **Version:** 001
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 12288
- **Output Token Limit:** 4096
- **Supported Actions:** `generateContent`, `countTokens`

## Model: models/gemini-pro-vision
- **Display Name:** Gemini 1.0 Pro Vision
- **Description:** The original Gemini 1.0 Pro Vision model version which was optimized for image understanding. Gemini 1.0 Pro Vision was deprecated on July 12, 2024. Move to a newer Gemini version.
- **Version:** 001
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 12288
- **Output Token Limit:** 4096
- **Supported Actions:** `generateContent`, `countTokens`

## Model: models/gemini-1.5-pro-latest
- **Display Name:** Gemini 1.5 Pro Latest
- **Description:** Alias that points to the most recent production (non-experimental) release of Gemini 1.5 Pro, our mid-size multimodal model that supports up to 2 million tokens.
- **Version:** 001
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 2000000
- **Output Token Limit:** 8192
- **Supported Actions:** `generateContent`, `countTokens`

## Model: models/gemini-1.5-pro-001
- **Display Name:** Gemini 1.5 Pro 001
- **Description:** Stable version of Gemini 1.5 Pro, our mid-size multimodal model that supports up to 2 million tokens, released in May of 2024.
- **Version:** 001
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 2000000
- **Output Token Limit:** 8192
- **Supported Actions:** `generateContent`, `countTokens`, `createCachedContent`

## Model: models/gemini-1.5-pro-002
- **Display Name:** Gemini 1.5 Pro 002
- **Description:** Stable version of Gemini 1.5 Pro, our mid-size multimodal model that supports up to 2 million tokens, released in September of 2024.
- **Version:** 002
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 2000000
- **Output Token Limit:** 8192
- **Supported Actions:** `generateContent`, `countTokens`, `createCachedContent`

## Model: models/gemini-1.5-pro
- **Display Name:** Gemini 1.5 Pro
- **Description:** Stable version of Gemini 1.5 Pro, our mid-size multimodal model that supports up to 2 million tokens, released in May of 2024.
- **Version:** 001
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 2000000
- **Output Token Limit:** 8192
- **Supported Actions:** `generateContent`, `countTokens`

## Model: models/gemini-1.5-flash-latest
- **Display Name:** Gemini 1.5 Flash Latest
- **Description:** Alias that points to the most recent production (non-experimental) release of Gemini 1.5 Flash, our fast and versatile multimodal model for scaling across diverse tasks.
- **Version:** 001
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 1000000
- **Output Token Limit:** 8192
- **Supported Actions:** `generateContent`, `countTokens`

## Model: models/gemini-1.5-flash-001
- **Display Name:** Gemini 1.5 Flash 001
- **Description:** Stable version of Gemini 1.5 Flash, our fast and versatile multimodal model for scaling across diverse tasks, released in May of 2024.
- **Version:** 001
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 1000000
- **Output Token Limit:** 8192
- **Supported Actions:** `generateContent`, `countTokens`, `createCachedContent`

## Model: models/gemini-1.5-flash-001-tuning
- **Display Name:** Gemini 1.5 Flash 001 Tuning
- **Description:** Version of Gemini 1.5 Flash that supports tuning, our fast and versatile multimodal model for scaling across diverse tasks, released in May of 2024.
- **Version:** 001
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 16384
- **Output Token Limit:** 8192
- **Supported Actions:** `generateContent`, `countTokens`, `createTunedModel`

## Model: models/gemini-1.5-flash
- **Display Name:** Gemini 1.5 Flash
- **Description:** Alias that points to the most recent stable version of Gemini 1.5 Flash, our fast and versatile multimodal model for scaling across diverse tasks.
- **Version:** 001
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 1000000
- **Output Token Limit:** 8192
- **Supported Actions:** `generateContent`, `countTokens`

## Model: models/gemini-1.5-flash-002
- **Display Name:** Gemini 1.5 Flash 002
- **Description:** Stable version of Gemini 1.5 Flash, our fast and versatile multimodal model for scaling across diverse tasks, released in September of 2024.
- **Version:** 002
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 1000000
- **Output Token Limit:** 8192
- **Supported Actions:** `generateContent`, `countTokens`, `createCachedContent`

## Model: models/gemini-1.5-flash-8b
- **Display Name:** Gemini 1.5 Flash-8B
- **Description:** Stable version of Gemini 1.5 Flash-8B, our smallest and most cost effective Flash model, released in October of 2024.
- **Version:** 001
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 1000000
- **Output Token Limit:** 8192
- **Supported Actions:** `createCachedContent`, `generateContent`, `countTokens`

## Model: models/gemini-1.5-flash-8b-001
- **Display Name:** Gemini 1.5 Flash-8B 001
- **Description:** Stable version of Gemini 1.5 Flash-8B, our smallest and most cost effective Flash model, released in October of 2024.
- **Version:** 001
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 1000000
- **Output Token Limit:** 8192
- **Supported Actions:** `createCachedContent`, `generateContent`, `countTokens`

## Model: models/gemini-1.5-flash-8b-latest
- **Display Name:** Gemini 1.5 Flash-8B Latest
- **Description:** Alias that points to the most recent production (non-experimental) release of Gemini 1.5 Flash-8B, our smallest and most cost effective Flash model, released in October of 2024.
- **Version:** 001
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 1000000
- **Output Token Limit:** 8192
- **Supported Actions:** `createCachedContent`, `generateContent`, `countTokens`

## Model: models/gemini-1.5-flash-8b-exp-0827
- **Display Name:** Gemini 1.5 Flash 8B Experimental 0827
- **Description:** Experimental release (August 27th, 2024) of Gemini 1.5 Flash-8B, our smallest and most cost effective Flash model. Replaced by Gemini-1.5-flash-8b-001 (stable).
- **Version:** 001
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 1000000
- **Output Token Limit:** 8192
- **Supported Actions:** `generateContent`, `countTokens`

## Model: models/gemini-1.5-flash-8b-exp-0924
- **Display Name:** Gemini 1.5 Flash 8B Experimental 0924
- **Description:** Experimental release (September 24th, 2024) of Gemini 1.5 Flash-8B, our smallest and most cost effective Flash model. Replaced by Gemini-1.5-flash-8b-001 (stable).
- **Version:** 001
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 1000000
- **Output Token Limit:** 8192
- **Supported Actions:** `generateContent`, `countTokens`

## Model: models/gemini-2.5-pro-exp-03-25
- **Display Name:** Gemini 2.5 Pro Experimental 03-25
- **Description:** Experimental release (March 25th, 2025) of Gemini 2.5 Pro
- **Version:** 2.5-exp-03-25
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 1048576
- **Output Token Limit:** 65536
- **Supported Actions:** `generateContent`, `countTokens`, `createCachedContent`

## Model: models/gemini-2.5-pro-preview-03-25
- **Display Name:** Gemini 2.5 Pro Preview 03-25
- **Description:** Gemini 2.5 Pro Preview 03-25
- **Version:** 2.5-preview-03-25
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 1048576
- **Output Token Limit:** 65536
- **Supported Actions:** `generateContent`, `countTokens`, `createCachedContent`

## Model: models/gemini-2.5-flash-preview-04-17
- **Display Name:** Gemini 2.5 Flash Preview 04-17
- **Description:** Preview release (April 17th, 2025) of Gemini 2.5 Flash
- **Version:** 2.5-preview-04-17
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 1048576
- **Output Token Limit:** 65536
- **Supported Actions:** `generateContent`, `countTokens`, `createCachedContent`

## Model: models/gemini-2.5-flash-preview-04-17-thinking
- **Display Name:** Gemini 2.5 Flash Preview 04-17 for cursor testing
- **Description:** Preview release (April 17th, 2025) of Gemini 2.5 Flash
- **Version:** 2.5-preview-04-17
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 1048576
- **Output Token Limit:** 65536
- **Supported Actions:** `generateContent`, `countTokens`, `createCachedContent`

## Model: models/gemini-2.5-pro-preview-05-06
- **Display Name:** Gemini 2.5 Pro Preview 05-06
- **Description:** Preview release (May 6th, 2025) of Gemini 2.5 Pro
- **Version:** 2.5-preview-05-06
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 1048576
- **Output Token Limit:** 65536
- **Supported Actions:** `generateContent`, `countTokens`, `createCachedContent`

## Model: models/gemini-2.0-flash-exp
- **Display Name:** Gemini 2.0 Flash Experimental
- **Description:** Gemini 2.0 Flash Experimental
- **Version:** 2.0
- **Endpoints:** None
- **Labels:** None
- **Tuned Model Info:**
    - Base Model: None
    - Create Time: None
    - Update Time: None
- **Input Token Limit:** 1048576
- **Output Token Limit:** 8192
- **Supported Actions:** `generateContent`, `countTokens`, `bidiGenerateContent`
"""

def parse_markdown_to_models_data(md_text):
    """
    Parses the markdown text and extracts model information.
    Returns a dictionary where keys are model display names and values are
    dictionaries of their attributes.
    """
    models_data = {}
    # Split by the model section header.
    model_sections = re.split(r'\n## Model: ', md_text.strip())
    
    # The first element of the split might be the introductory text before any models.
    # We skip it if it doesn't look like a model section itself.
    if model_sections and not model_sections[0].strip().startswith("models/"):
        model_sections = model_sections[1:]
    elif not model_sections or (len(model_sections) == 1 and not model_sections[0].strip().startswith("models/")):
        # Handle cases where the split didn't work or only intro text was present
        if "## Model:" not in md_text :
            print("No model sections found in the markdown text.")
            return models_data
        # If ## Model: is present but was the only thing, or split failed oddly.
        # This part might need more robust error handling or logging based on md_text structure.


    for section in model_sections:
        if not section.strip(): # Skip empty sections that might result from multiple newlines
            continue
            
        lines = section.strip().split('\n')
        model_id_line = lines[0].strip() # This should be like "models/chat-bison-001"
        
        # Basic validation that this section indeed starts with a model ID path
        if not model_id_line.startswith("models/"):
            # print(f"Skipping section, expected model path, got: {model_id_line}") # For debugging
            continue

        attributes = {"Model ID": model_id_line}
        display_name_for_dict_key = None

        for line in lines[1:]:
            line = line.strip()
            if line.startswith("- **Display Name:**"):
                val = line.replace("- **Display Name:**", "").strip()
                attributes["Display Name"] = val
                display_name_for_dict_key = val # This will be the key in models_data
            elif line.startswith("- **Description:**"):
                attributes["Description"] = line.replace("- **Description:**", "").strip()
            elif line.startswith("- **Version:**"):
                attributes["Version"] = line.replace("- **Version:**", "").strip()
            elif line.startswith("- **Input Token Limit:**"):
                attributes["Input Token Limit"] = line.replace("- **Input Token Limit:**", "").strip()
            elif line.startswith("- **Output Token Limit:**"):
                attributes["Output Token Limit"] = line.replace("- **Output Token Limit:**", "").strip()
            elif line.startswith("- **Supported Actions:**"):
                actions_str = line.replace("- **Supported Actions:**", "").strip()
                # Extract actions like `action1`, `action2`
                actions = [action.replace('`', '').strip() for action in actions_str.split(',')]
                attributes["Supported Actions"] = actions
            # Other fields like Endpoints, Labels, Tuned Model Info are parsed if needed, but not used in display yet.

        # Use Display Name as the primary key for the dictionary if available
        if display_name_for_dict_key:
            models_data[display_name_for_dict_key] = attributes
        elif model_id_line: # Fallback to model_id if display name is somehow missing (should not happen with current MD)
            models_data[model_id_line] = attributes # This case is less ideal for user-facing dropdown
            
    return models_data

# Parse the model data globally on script load
models_data_global = parse_markdown_to_models_data(markdown_text)
model_display_names_list = sorted(list(models_data_global.keys()))

def display_model_attributes(selected_display_name):
    """
    Formats the attributes of the selected model for display in Markdown.
    """
    if not selected_display_name:
        return "Please select a model from the dropdown."
    model_info = models_data_global.get(selected_display_name)
    if not model_info:
        return f"Details not found for model: {selected_display_name}"

    # Format the output as Markdown
    output_md = f"## {model_info.get('Display Name', 'N/A')}\n\n"
    output_md += f"**Model ID:** `{model_info.get('Model ID', 'N/A')}`\n\n"
    output_md += f"**Description:** {model_info.get('Description', 'N/A')}\n\n"
    output_md += f"**Version:** {model_info.get('Version', 'N/A')}\n\n"
    output_md += f"**Input Token Limit:** {model_info.get('Input Token Limit', 'N/A')}\n\n"
    output_md += f"**Output Token Limit:** {model_info.get('Output Token Limit', 'N/A')}\n\n"
    
    actions = model_info.get('Supported Actions', [])
    if actions and any(actions): # Check if list is not empty and not just empty strings
        output_md += "**Supported Actions:**\n"
        for action in actions:
            if action: # Ensure action string is not empty
                output_md += f"- `{action}`\n"
    else:
        output_md += "**Supported Actions:** N/A\n"
        
    return output_md

# --- Chatbot Functions ---
def format_chat_history_for_genai(gradio_history):
    """
    Converts Gradio chat history (list of message dicts) to Google GenAI Content format.
    Each Gradio message is {"role": "user/assistant", "content": "message text"}
    Each GenAI message is {"role": "user/model", "parts": [{"text": "message text"}]}
    """
    genai_history = []
    for message_dict in gradio_history:
        # Ensure message_dict is a dictionary with 'role' and 'content'
        if isinstance(message_dict, dict) and "role" in message_dict and "content" in message_dict:
            role = "user" if message_dict["role"] == "user" else "model"
            genai_history.append({"role": role, "parts": [{"text": message_dict["content"]}]})
        # else:
            # print(f"Skipping malformed message in Gradio history: {message_dict}") # For debugging
    return genai_history

def user_chat_interaction(user_message, history: list, selected_model_display_name: str):
    """
    Handles user message input. Appends user message to history.
    The history is expected to be a list of dictionaries.
    """
    if not user_message.strip(): # Do nothing if the message is empty
        # Return current history and selected model without change if message is empty
        return "", history if history is not None else [], selected_model_display_name
    
    # Ensure history is a list, initialize if None (though Gradio usually handles this)
    current_history = history if history is not None else []
    
    # Append the new user message in the correct dictionary format
    updated_history = current_history + [{"role": "user", "content": user_message}]
    return "", updated_history, selected_model_display_name


def model_chat_response(history: list, selected_model_display_name: str):
    """
    Generates and streams the bot's response using the selected Google GenAI model.
    History is a list of message dictionaries.
    """
    current_history = history if history is not None else []

    if not selected_model_display_name:
        current_history.append({"role": "assistant", "content": "Please select a model from the dropdown first."})
        yield current_history
        return

    model_info = models_data_global.get(selected_model_display_name)
    if not model_info or "Model ID" not in model_info:
        current_history.append({"role": "assistant", "content": f"Could not find model ID for {selected_model_display_name}."})
        yield current_history
        return

    raw_model_id = model_info["Model ID"]
    genai_model_name = raw_model_id.replace("models/", "") # e.g., "gemini-1.5-pro-latest"

    # Check if API key is configured (simplified check)
    api_key_available = bool(os.getenv("GOOGLE_API_KEY"))
    # Check if genai.api_key is set and not the placeholder
    genai_api_key_is_placeholder = hasattr(genai, 'api_key') and genai.api_key and "YOUR_API_KEY" in str(genai.api_key)
    
    if not api_key_available and (not hasattr(genai, 'api_key') or genai_api_key_is_placeholder):
         current_history.append({"role": "assistant", "content": "Google API Key not configured. Please set it to use the chat."})
         yield current_history
         return

    supported_actions = model_info.get("Supported Actions", [])
    # More robust check for chat-compatible actions
    if not any(action in ["generateContent", "generateMessage", "bidiGenerateContent"] for action in supported_actions):
        current_history.append({"role": "assistant", "content": f"The selected model '{selected_model_display_name}' may not support chat generation based on its listed actions."})
        yield current_history
        return

    try:
        # The history already contains the user's latest message.
        # We need to format the entire history for the GenAI model.
        messages_for_genai = format_chat_history_for_genai(current_history)
        
        if not messages_for_genai or messages_for_genai[-1]['role'] != 'user':
            current_history.append({"role": "assistant", "content": "Error: Chat history is not in the expected format for the AI model."})
            yield current_history
            return

        model = genai.GenerativeModel(genai_model_name)
        response_stream = model.generate_content(messages_for_genai, stream=True)

        current_history.append({"role": "assistant", "content": ""}) # Add placeholder for assistant's response
        
        assistant_response_complete = False
        for chunk in response_stream:
            if hasattr(chunk, 'text') and chunk.text: # Ensure 'text' attribute exists and is not None
                current_history[-1]['content'] += chunk.text
                assistant_response_complete = True 
                time.sleep(0.02) 
                yield current_history
            
            if hasattr(chunk, 'prompt_feedback') and chunk.prompt_feedback and chunk.prompt_feedback.block_reason:
                block_reason_message = f"Content generation stopped: {chunk.prompt_feedback.block_reason}"
                if chunk.prompt_feedback.block_reason_message:
                    block_reason_message += f" - {chunk.prompt_feedback.block_reason_message}"
                
                if not current_history[-1]['content']: 
                    current_history[-1]['content'] = f"[SYSTEM: {block_reason_message}]"
                else: 
                    current_history[-1]['content'] += f"\n[SYSTEM: {block_reason_message}]"
                assistant_response_complete = True 
                yield current_history
                return 
        
        if not assistant_response_complete and not current_history[-1]['content']:
            current_history[-1]['content'] = "[SYSTEM: No text response received from the model.]"
            yield current_history

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        if current_history and current_history[-1]["role"] == "assistant" and current_history[-1]["content"] == "":
            current_history[-1]["content"] = f"[Error: {error_message}]"
        else: 
            current_history.append({"role": "assistant", "content": f"[Error: {error_message}]"})
        yield current_history

# --- Gradio Interface ---
with gr.Blocks(theme=gr.themes.Soft(primary_hue=gr.themes.colors.blue, secondary_hue=gr.themes.colors.sky)) as demo:
    gr.Markdown("# AI Model Information Viewer & Chat")
    gr.Markdown("Select a model to view its attributes and chat with it (if supported).")
    gr.Markdown("⚠️ **Ensure your `GOOGLE_API_KEY` is configured, or the chat will not use live models.**")

    with gr.Row():
        with gr.Column(scale=1): 
            gr.Markdown("### Model Selection & Attributes")
            model_dropdown = gr.Dropdown(
                choices=model_display_names_list,
                label="Select Model",
                info="Choose a model to see its details and chat with it.",
                value=model_display_names_list[0] if model_display_names_list else None 
            )
            attributes_output = gr.Markdown(label="Model Attributes")
            
        with gr.Column(scale=2): 
            gr.Markdown("### Chat with Selected Model")
            chatbot_display = gr.Chatbot(
                label="Chat Window", 
                bubble_full_width=False, 
                height=500,
                type="messages" 
            )
            with gr.Row(): # Use a row to place textbox and button side-by-side
                chat_msg_input = gr.Textbox(
                    label="Your Message", 
                    placeholder="Type your message here...",
                    show_label=False, 
                    lines=2,
                    scale=4 # Textbox takes more space
                )
                send_button = gr.Button("Send", variant="primary", scale=1) # Button takes less space
            
            clear_chat_button = gr.Button("Clear Chat", variant="stop",elem_classes="full-width-button")


    # --- Event Handling ---
    model_dropdown.change(
        fn=display_model_attributes,
        inputs=model_dropdown,
        outputs=attributes_output
    )

    # Define the common chat processing chain
    def submit_chat_message(user_message, chat_history, model_name):
        # This function will be called by both textbox submit and button click
        # It first calls user_chat_interaction
        _, updated_history, _ = user_chat_interaction(user_message, chat_history, model_name)
        # Then it yields from model_chat_response
        # Note: model_chat_response is a generator, so we need to yield from it
        # However, Gradio's .then() handles this chaining.
        # The key is that user_chat_interaction prepares the history for model_chat_response.
        return "", updated_history # Return cleared input and updated history for the first step

    # Textbox submission (Enter key)
    chat_msg_input.submit(
        fn=user_chat_interaction, # Directly call user_chat_interaction
        inputs=[chat_msg_input, chatbot_display, model_dropdown],
        outputs=[chat_msg_input, chatbot_display, model_dropdown], 
        queue=False
    ).then(
        fn=model_chat_response, # Then call model_chat_response
        inputs=[chatbot_display, model_dropdown], 
        outputs=chatbot_display
    )

    # Send button click
    send_button.click(
        fn=user_chat_interaction, # Directly call user_chat_interaction
        inputs=[chat_msg_input, chatbot_display, model_dropdown],
        outputs=[chat_msg_input, chatbot_display, model_dropdown],
        queue=False
    ).then(
        fn=model_chat_response, # Then call model_chat_response
        inputs=[chatbot_display, model_dropdown],
        outputs=chatbot_display
    )

    clear_chat_button.click(
        lambda: ([], ""), 
        None, 
        [chatbot_display, chat_msg_input], 
        queue=False 
    )
    
    # --- Initial Loading ---
    def initial_load_attributes():
        if model_display_names_list:
            return display_model_attributes(model_display_names_list[0])
        return "No models loaded. Check the Markdown source."

    demo.load(initial_load_attributes, inputs=None, outputs=attributes_output)
    
    def initial_chatbot_message():
        return [{"role": "assistant", "content": "Chatbot ready. Select a model and send a message."}]
        
    demo.load(initial_chatbot_message, None, chatbot_display)

if __name__ == "__main__":
    demo.queue().launch(debug=True)
