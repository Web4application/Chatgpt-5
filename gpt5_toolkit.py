import os
import sys
import re
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
IMAGE_EXTS = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff"]

def detect_role(text):
    text_lower = text.lower()
    if text_lower.startswith("system:"):
        return "system"
    elif text_lower.startswith("assistant:"):
        return "assistant"
    return "user"

def classify_arg(arg):
    if os.path.exists(arg):
        return "local_file"
    elif re.match(r'^https?://', arg):
        if any(arg.lower().endswith(ext) for ext in IMAGE_EXTS):
            return "image_url"
        else:
            return "remote_file"
    else:
        return "text"

def prepare_input(arg):
    arg_type = classify_arg(arg)
    role = "user"

    if arg_type == "text":
        role = detect_role(arg)
        return {"role": role, "content":[{"type":"input_text", "text":arg}]}
    elif arg_type == "image_url":
        return {"role": role, "content":[{"type":"input_image", "image_url":arg}]}
    elif arg_type == "local_file":
        f = client.files.create(file=open(arg, "rb"), purpose="user_data")
        return {"role": role, "content":[{"type":"input_file", "file_id":f.id}]}
    elif arg_type == "remote_file":
        return {"role": role, "content":[{"type":"input_file", "file_url":arg}]}

def run_shorthand(args_list, tools=None, stream=False):
    conversation = [prepare_input(arg) for arg in args_list]

    response = client.responses.create(
        model="gpt-5",
        input=conversation,
        tools=tools,
        stream=stream
    )

    if stream:
        for event in response:
            print(event, end="", flush=True)
        print()
    else:
        print(response.output_text)

def interactive_chat(tools=None, stream=False):
    print("GPT-5 Interactive Terminal Chat")
    print("Type 'exit' to quit.\n")

    conversation = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            break

        input_item = prepare_input(user_input)
        conversation.append(input_item)

        response = client.responses.create(
            model="gpt-5",
            input=conversation,
            tools=tools,
            stream=stream
        )

        if stream:
            print("GPT-5: ", end="", flush=True)
            for event in response:
                print(event, end="", flush=True)
            print()
        else:
            print("GPT-5:", response.output_text)

        conversation.append({"role": "assistant", "content":[{"type":"output_text", "text":response.output_text}]})

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="GPT-5 Super CLI + Interactive Chat")
    parser.add_argument("inputs", nargs="*", help="Text, local files, image URLs, or file URLs")
    parser.add_argument("--stream", "-s", action="store_true", help="Enable streaming output")
    parser.add_argument("--tools", "-T", type=str, help="Optional JSON string defining tools/functions")
    args = parser.parse_args()

    tools = json.loads(args.tools) if args.tools else None

    if args.inputs:
        run_shorthand(args.inputs, tools=tools, stream=args.stream)
    else:
        interactive_chat(tools=tools, stream=args.stream)
