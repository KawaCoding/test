import runpod
import time
import os
from datetime import datetime

def print_volume_structure(start_path="/runpod-volume"):
    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, "").count(os.sep)
        indent = " " * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = " " * 4 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")

# Call it before loading the model
print("📁 Dumping volume structure:")
print_volume_structure()

def handler(event):
    print("Worker Start")
    input = event['input']

    prompt = input.get('prompt')  
    seconds = input.get('seconds', 0)  

    print(f"Received prompt: {prompt}")
    print(f"Sleeping for {seconds} seconds...")

    # Create a timestamped test folder in the mounted volume
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_folder = f"/runpod-volume/test_folder_{timestamp}"
    try:
        os.makedirs(test_folder, exist_ok=True)
        print(f"✅ Created test folder: {test_folder}")
    except Exception as e:
        print(f"❌ Failed to create test folder: {e}")

    time.sleep(seconds)

    return {
        "status": "done",
        "prompt": prompt,
        "test_folder": test_folder
    }

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
