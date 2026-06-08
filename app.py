from pathlib import Path
from ollama import Client

def main():
    # 1. Initialize the official client targeted at your remote server
    client = Client(host="http://10.22.39.192:11434")
    
    # 2. Local path to the image on your computer
    local_image_path = "chart.png" 
    
    try:
        # Crucial Fix: Read the file as raw bytes locally on your computer
        image_bytes = Path(local_image_path).read_bytes()
        
        print(f"📡 Serializing bytes and transmitting to remote Qwen2.5-VL at 10.22.39.192...")
        
        # 3. Pass the raw bytes instead of the file path string
        response = client.chat(
            model="qwen2.5vl:latest",
            messages=[
                {
                    "role": "user",
                    "content": "Analyze this visual asset. Break down all explicit metrics and headings.",
                    # Sending the byte stream directly allows remote processing
                    "images": [image_bytes] 
                }
            ],
            options={
                "temperature": 0.0
            }
        )
        
        # 4. Print clean text result
        print("\n📝 Qwen2.5-VL Analysis:\n")
        print(response.message.content)
        
    except FileNotFoundError:
        print(f"\n❌ Error: Could not find '{local_image_path}' on your local computer. Please place an image in this directory.")
    except Exception as e:
        print(f"\n❌ Remote pipeline failed: {e}")

if __name__ == "__main__":
    main()