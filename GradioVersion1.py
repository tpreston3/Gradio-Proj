import gradio as gr
import re
import os
import time # For the dummy bot in case API fails
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

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
# Read the markdown content from the file
try:
    with open('gemini-models_documentation.md', 'r', encoding='utf-8') as f:
        markdown_text = f.read()
except FileNotFoundError:
    print("Error: gemini-models_documentation.md not found.")
    markdown_text = ""

def parse_markdown_to_models_data(md_text):
    """
    Parses the markdown text and extracts model information.
    Adapted for the new documentation format where models are under ### headers.
    """
    models_data = {}
    if not md_text:
        return models_data

    # Split by the model header (### Model Name). 
    # The new format uses "### " for model names.
    # We use a regex to split but keep the delimiters to know the model name.
    # However, re.split with capturing group might be complex to handle cleanly in loop.
    # Let's simple split by "### " and process.
    
    sections = re.split(r'\n### ', md_text)
    
    # The first section is intro/group headers, skip it.
    if len(sections) > 1:
        sections = sections[1:]
    else:
        # Check if the text starts with ### immediately
        if md_text.strip().startswith("### "):
             sections = [md_text.strip()[4:]] # Remove first marker
             sections.extend(re.split(r'\n### ', md_text.strip()[4:]))
             # This is getting messy, let's stick to simple split and cleaning
             pass
    
    # Better approach: Iterate and check lines
    # But splitting is easier if consistent. 
    # The file has "## Series Name" and "### Model Name".
    # Splitting by "\n### " should give us the model sections, where the first line is the name.
    
    for section in sections:
        section = section.strip()
        if not section: continue
        
        lines = section.split('\n')
        display_name = lines[0].strip()
        
        # If the split captured "Gemini 3 Pro", that's our display name.
        # But if we split by "### ", the "### " is gone.
        
        # We need to verify this is actually a model section. 
        # Look for "Internal Name" or "Description"
        if "- **Internal Name:**" not in section and "- **Description:**" not in section:
             continue

        attributes = {"Display Name": display_name}
        
        for line in lines[1:]:
            line = line.strip()
            if line.startswith("- **Internal Name:**"):
                # Map Internal Name to Model ID for compatibility
                val = line.replace("- **Internal Name:**", "").strip().replace('`', '')
                attributes["Model ID"] = f"models/{val}" if not val.startswith("models/") else val
                attributes["Internal Name"] = val
            elif line.startswith("- **Description:**"):
                attributes["Description"] = line.replace("- **Description:**", "").strip()
            # Version seems missing in new doc or implied, skipping for now
            elif line.startswith("- **Input Token Limit:**"):
                attributes["Input Token Limit"] = line.replace("- **Input Token Limit:**", "").strip()
            elif line.startswith("- **Output Token Limit:**"):
                attributes["Output Token Limit"] = line.replace("- **Output Token Limit:**", "").strip()
            elif line.startswith("- **Supported Actions:**"):
                actions_str = line.replace("- **Supported Actions:**", "").strip()
                actions = [action.replace('`', '').strip() for action in actions_str.split(',')]
                attributes["Supported Actions"] = actions

        if "Model ID" in attributes:
            models_data[display_name] = attributes
            
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
