import json

def compress_telegram_json(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    compressed_messages = []
    
    # Optional: Map users to short IDs to save more space
    user_map = {}
    user_count = 0

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

        # 3. Shorten User names (Optional but recommended)
        user_name = msg.get('from', 'Unknown')
        if user_name not in user_map:
            user_count += 1
            user_map[user_name] = f"U{user_count}"
        
        # 4. Construct minimal object
        # i: ID, u: User, t: Text, r: ReplyTo
        mini_msg = {
            "i": msg.get('id'),
            "u": user_map[user_name],
            "t": text_content.replace('\n', ' ') # Newlines into spaces to save lines
        }
        
        if 'reply_to_message_id' in msg:
            mini_msg["r"] = msg['reply_to_message_id']
            
        compressed_messages.append(mini_msg)

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        for m in compressed_messages:
            f.write(json.dumps(m, ensure_ascii=False) + '\n')
            
    print(f"Compressed and wrote {len(compressed_messages)} messages to {output_path}.")


inputFile = input("Input file name (press enter for \"input.json\"): ")
if (inputFile == ""): inputFile = "input.json";

outputFile = input("Output file name (press enter for \"output.jsonl\"): ")
if (outputFile == ""): outputFile = "output.jsonl";


compress_telegram_json(inputFile, outputFile)
