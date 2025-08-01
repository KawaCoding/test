import runpod
import torch
from diffusers import StableDiffusionPipeline
import base64
from io import BytesIO

# Load the model once, outside the handler for efficiency
model_path = "/runpod-volume/models/NSFW-gen-v2"  # your local model path here

print("Loading model from:", model_path)
pipe = StableDiffusionPipeline.from_pretrained(model_path, torch_dtype=torch.float16)
pipe = pipe.to("cuda")
pipe.safety_checker = None  # Disable NSFW check if you want

def handler(event):
    print("Worker Start")
    input_data = event.get('input', {})

    prompt = input_data.get('prompt')
    seconds = input_data.get('seconds', 0)

    print(f"Received prompt: {prompt}")
    if seconds > 0:
        print(f"Sleeping for {seconds} seconds...")
        import time
        time.sleep(seconds)

    if not prompt:
        return {"error": "No prompt provided."}

    # Generate image
    image = pipe(prompt).images[0]

    # Convert image to base64 string
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    print("Image generated successfully")

    # Return the base64 image string in a dict
    return {"image_base64": img_str}

if __name__ == "__main__":
    runpod.serverless.start({'handler': handler})
