import json

def compress_telegram_json(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    compressed_messages = []

    for msg in data.get('messages', []):
        # 1. Only process actual messages with text
        if msg.get('type') != 'message':
            continue
            
        # 2. Flatten the text field
        text_content = msg.get('text', "")
        if isinstance(text_content, list):
            text_content = "".join([
                item['text'] if isinstance(item, dict) else item 
                for item in text_content
            ])
            
        if not text_content.strip():
            continue # Skip messages that are just stickers/files with no text
            
        compressed_messages.append(text_content)

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        for m in compressed_messages:
            f.write(m + '\n')
            
    print(f"Compressed and wrote {len(compressed_messages)} messages.")


inputFile = input("Input file name (press enter for \"input.json\"): ")
if (inputFile == ""): inputFile = "input.json";

outputFile = input("Output file name (press enter for \"output.jsonl\"): ")
if (outputFile == ""): outputFile = "output.jsonl";


compress_telegram_json(inputFile, outputFile)
