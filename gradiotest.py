import gradio as gr
import re

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
    # Split by the model section header. The first part is the general intro.
    # Using a regex that accounts for potential variations in newlines before "## Model:"
    model_sections = re.split(r'\n## Model: ', md_text.strip())
    
    if not model_sections or len(model_sections) <= 1:
        # Handle case where the split might not work as expected or no models found
        # For instance, if the first "## Model:" is at the very beginning
        if md_text.strip().startswith("## Model:"):
             model_sections = [md_text.strip().split("## Model: ", 1)[1]]
        elif "## Model:" not in md_text:
             print("No model sections found.")
             return models_data # No models to parse
        # If only the header is present, skip it.
        # The logic below assumes model_sections[0] is header if it doesn't start with a model path.
        # However, re.split will put the text *before* the first delimiter in model_sections[0].
        # So, if the text starts with "# AI Model Information", model_sections[0] will be that.
        # We need to ensure we skip the initial overall header.
        if not model_sections[0].startswith("models/"): # A heuristic check
            model_sections = model_sections[1:]


    for section in model_sections:
        if not section.strip(): # Skip empty sections
            continue
            
        lines = section.strip().split('\n')
        model_id_line = lines[0].strip()
        
        # Ensure the first line is indeed a model path, otherwise skip this section
        if not model_id_line.startswith("models/"):
            # This might be part of the header or a malformed section
            # print(f"Skipping section, expected model path, got: {model_id_line}")
            continue

        attributes = {"Model ID": model_id_line}
        display_name_for_dict_key = None

        for line in lines[1:]:
            line = line.strip()
            if line.startswith("- **Display Name:**"):
                val = line.replace("- **Display Name:**", "").strip()
                attributes["Display Name"] = val
                display_name_for_dict_key = val
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
            # Other fields like Endpoints, Labels, Tuned Model Info are ignored for now.

        # Use Display Name as the primary key for the dictionary if available
        if display_name_for_dict_key:
            models_data[display_name_for_dict_key] = attributes
        elif model_id_line: # Fallback to model_id if display name is somehow missing
            models_data[model_id_line] = attributes
            
    return models_data

# Parse the model data
models_data_global = parse_markdown_to_models_data(markdown_text)

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

# Get the list of model display names for the dropdown
model_display_names_list = sorted(list(models_data_global.keys()))

# Create the Gradio interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# AI Model Information Viewer")
    gr.Markdown("Select a model from the dropdown to view its attributes.")
    
    with gr.Row():
        model_dropdown = gr.Dropdown(
            choices=model_display_names_list,
            label="Select Model",
            info="Choose a model to see its details"
        )
    
    with gr.Row():
        attributes_output = gr.Markdown(label="Model Attributes")

    model_dropdown.change(
        fn=display_model_attributes,
        inputs=model_dropdown,
        outputs=attributes_output
    )
    
    # Set a default view for when the app loads
    if model_display_names_list:
        demo.load(lambda: display_model_attributes(model_display_names_list[0]), inputs=None, outputs=attributes_output)
    else:
        demo.load(lambda: "No models loaded. Check the Markdown source.", inputs=None, outputs=attributes_output)


if __name__ == "__main__":
    # Launch the Gradio app
    demo.launch()
