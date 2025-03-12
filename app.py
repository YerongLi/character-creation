# import deepsparse
import gradio as gr
import os
import json
from typing import Tuple, List
from transformers import pipeline
# deepsparse.cpu.print_hardware_capability()
MODEL_ID = os.getenv('MODELS') + "/Llama-3.2-1B-Instruct"
with open('characters.json', 'r') as file:
    characters = json.load(file)
character = characters[0]

filled_system_prompt = f"""
You are now simulating the character {character['name']}. Here are the details of your persona:
- {character['personas'][0]}
- {character['personas'][1]}
- {character['personas'][2]}

Respond to the user's messages as if you are {character['name']}, keeping in mind your persona traits.
"""
# Extract the first character's data
character = characters[0]

# Create the system prompt


# DESCRIPTION = f"""
# # 

# Model ID: {MODEL_ID[len("hf:"):]}

# Character {character}
# """
# DESCRIPTION = f"""
# # Model ID: {MODEL_ID[len("hf:"):]}  # Strips the "hf:" prefix

# Character:
# - Name: {character['name']}
#   {chr(10).join([f"- {persona}" for persona in character['personas']])}
# """

MAX_MAX_NEW_TOKENS = 80
DEFAULT_MAX_NEW_TOKENS = 80

# Setup the engine
pipe = pipeline( task="text-generation", model=MODEL_ID, max_new_tokens=MAX_MAX_NEW_TOKENS, num_return_sequences=1
               )


def clear_and_save_textbox(message: str) -> Tuple[str, str]:
    return "", message


def display_input(
    message: str, history: List[Tuple[str, str]]
) -> List[Tuple[str, str]]:
    history.append((message, ""))
    return history


def delete_prev_fn(history: List[Tuple[str, str]]) -> Tuple[List[Tuple[str, str]], str]:
    try:
        message, _ = history.pop()
    except IndexError:
        message = ""
    return history, message or ""

theme = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="green",
)
def get_description(index):
    character = characters[index]
    description = f"""Character Name: {character['name']}\n
{chr(10).join(f"- {persona}" for persona in character['personas'])}
    """
    return description

def build_system_prompt(index):
    character = characters[index]
    global filled_system_prompt
    system_prompt = f"""
    You are now simulating the character {character['name']}. Here are the details of your persona:
    - {character['personas'][0]}
    - {character['personas'][1]}
    - {character['personas'][2]}
    
    Respond to the user's messages as if you are {character['name']}, keeping in mind your persona traits.
    """
    filled_system_prompt = system_prompt
    return system_prompt

with gr.Blocks(theme=theme) as demo:
    scene_input = gr.Textbox(
        label="Scene",
        placeholder="A 51-year-old man was shot in the chest by his 52-year-old roommate, Michael Lawrence Finnegan, during a dispute in Lucerne on Friday evening. The incident occurred around 8 p.m. at a residence on 15th Avenue, where Finnegan allegedly shot the victim with a .22-caliber pistol. The victim was hospitalized and is expected to survive. Finnegan claimed the victim had been hostile for several days, threatening to evict him and repeatedly entering his room. Feeling threatened, Finnegan said he shot his roommate in self-defense. He was arrested on suspicion of assault with a firearm.",
        # placeholder="Describe the scene or context for the conversation...",
        lines=2,
    )
    character_name_dropdown = gr.Dropdown(
        choices=[char["name"] for char in characters],
        label="Select a Character",
    )
    description_output = gr.Markdown(value="Select a character to see their description.")
    system_prompt_output = gr.State(value="")
    # Update description and system prompt based on dropdown selection
    def update_outputs(name):
        index = [char["name"] for char in characters].index(name)
        return get_description(index), build_system_prompt(index)
    # print(system_prompt_output)
    # print(system_prompt_output)
    def reset_and_update_outputs(name):
        description, prompt = update_outputs(name)
        return description, prompt, [], ""  # Clear chatbot and saved_input
    # character_name_dropdown.change(
    #     fn=reset_and_update_outputs,
    #     inputs=[character_name_dropdown],
    #     outputs=[description_output, system_prompt_output],
    # )

    # Update and clear outputs when dropdown changes

    with gr.Group():
        chatbot = gr.Chatbot(label="Chatbot")
        with gr.Row():
            textbox = gr.Textbox(
                container=False,
                show_label=False,
                placeholder="Type a message...",
                scale=10,
            )
            submit_button = gr.Button("Submit", variant="primary", scale=1, min_width=0)

    with gr.Row():
        retry_button = gr.Button("🔄  Retry", variant="secondary")
        undo_button = gr.Button("↩️ Undo", variant="secondary")
        clear_button = gr.Button("🗑️  Clear", variant="secondary")

    saved_input = gr.State()
    character_name_dropdown.change(
        fn=reset_and_update_outputs,  # Reset the description, prompt, chatbot, and saved_input
        inputs=[character_name_dropdown],
        outputs=[description_output, system_prompt_output, chatbot, saved_input],
    )
    gr.Examples(
        examples=[
            "What is your name?",
            "What do you do for a living?",
            "How old are you?",
            "What has just happened?",
            "Who is Elon Musk?",
        ],
        inputs=[textbox],
    )

    max_new_tokens = gr.Slider(
        label="Max new tokens",
        value=DEFAULT_MAX_NEW_TOKENS,
        minimum=0,
        maximum=MAX_MAX_NEW_TOKENS,
        step=1,
        interactive=True,
        info="The maximum numbers of new tokens",
    )
    temperature = gr.Slider(
        label="Temperature",
        value=0.9,
        minimum=0.05,
        maximum=1.0,
        step=0.05,
        interactive=True,
        info="Higher values produce more diverse outputs",
    )
    top_p = gr.Slider(
        label="Top-p (nucleus) sampling",
        value=0.40,
        minimum=0.0,
        maximum=1,
        step=0.05,
        interactive=True,
        info="Higher values sample more low-probability tokens",
    )
    top_k = gr.Slider(
        label="Top-k sampling",
        value=20,
        minimum=1,
        maximum=100,
        step=1,
        interactive=True,
        info="Sample from the top_k most likely tokens",
    )
    reptition_penalty = gr.Slider(
        label="Repetition penalty",
        value=1.2,
        minimum=1.0,
        maximum=2.0,
        step=0.05,
        interactive=True,
        info="Penalize repeated tokens",
    )

    # Generation inference
    def generate(
        message,
        history,
        max_new_tokens: int,
        temperature: float,
        top_p: float,
        top_k: int,
        reptition_penalty: float,
    ):
        generation_config = {
            "max_new_tokens": max_new_tokens,
            "do_sample": True,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "reptition_penalty": reptition_penalty,
        }
        # system_prompt = f"""
        # You are now simulating the character {character['name']}. Here are the details of your persona:
        # - {character['personas'][0]}
        # - {character['personas'][1]}
        # - {character['personas'][2]}
        
        # Respond to the user's messages as if you are {character['name']}, keeping in mind your persona traits.
        # """
        conversation = []
        print(system_prompt_output)
        conversation.append({"role": "system", "content": filled_system_prompt})
        conversation.append({"role": "user", "content": message})
        
        formatted_conversation = pipe.tokenizer.apply_chat_template(
            conversation, tokenize=False, add_generation_prompt=True
        )

        # Generate text using the pipeline 
        inference = pipe(text_inputs=formatted_conversation,
                         max_new_tokens=max_new_tokens,
                         temperature=temperature,
                         top_p=top_p,
                         top_k=top_k,
                         repetition_penalty=reptition_penalty,
                         num_return_sequences=1)
        for token in inference:
            generated_text = token['generated_text'].replace(formatted_conversation, "").strip() 
            history[-1][1] += generated_text
            yield history

        # print(pipe.timer_manager)

    # Hooking up all the buttons
    textbox.submit(
        fn=clear_and_save_textbox,
        inputs=textbox,
        outputs=[textbox, saved_input],
        api_name=False,
        queue=False,
    ).then(
        fn=display_input,
        inputs=[saved_input, chatbot],
        outputs=chatbot,
        api_name=False,
        queue=False,
    ).success(
        generate,
        inputs=[
            saved_input,
            chatbot,
            max_new_tokens,
            temperature,
            top_p,
            top_k,
            reptition_penalty,
        ],
        outputs=[chatbot],
        api_name=False,
    )

    submit_button.click(
        fn=clear_and_save_textbox,
        inputs=textbox,
        outputs=[textbox, saved_input],
        api_name=False,
        queue=False,
    ).then(
        fn=display_input,
        inputs=[saved_input, chatbot],
        outputs=chatbot,
        api_name=False,
        queue=False,
    ).success(
        generate,
        inputs=[
            saved_input,
            chatbot,
            max_new_tokens,
            temperature,
            top_p,
            top_k,
            reptition_penalty,
        ],
        outputs=[chatbot],
        api_name=False,
    )

    retry_button.click(
        fn=delete_prev_fn,
        inputs=chatbot,
        outputs=[chatbot, saved_input],
        api_name=False,
        queue=False,
    ).then(
        fn=display_input,
        inputs=[saved_input, chatbot],
        outputs=chatbot,
        api_name=False,
        queue=False,
    ).then(
        generate,
        inputs=[
            saved_input,
            chatbot,
            max_new_tokens,
            temperature,
            top_p,
            top_k,
            reptition_penalty,
        ],
        outputs=[chatbot],
        api_name=False,
    )

    undo_button.click(
        fn=delete_prev_fn,
        inputs=chatbot,
        outputs=[chatbot, saved_input],
        api_name=False,
        queue=False,
    ).then(
        fn=lambda x: x,
        inputs=[saved_input],
        outputs=textbox,
        api_name=False,
        queue=False,
    )

    clear_button.click(
        fn=lambda: ([], ""),
        outputs=[chatbot, saved_input],
        queue=False,
        api_name=False,
    )

demo.queue().launch(share=True)
