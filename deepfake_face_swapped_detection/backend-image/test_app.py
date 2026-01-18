import requests
import numpy as np
from PIL import Image
import io
import json

# 1. Create a dummy image (random noise)
print("Generating dummy image...")
img_array = np.random.randint(0, 255, (180, 180, 3), dtype=np.uint8)
img = Image.fromarray(img_array)

# Save to bytes
img_byte_arr = io.BytesIO()
img.save(img_byte_arr, format='PNG')
img_byte_arr.seek(0) # Reset pointer to start

# 2. Define the API endpoint
url = "http://127.0.0.1:8000/explain"

# 3. Send the POST request
print(f"Sending request to {url}...")
try:
    files = {"file": ("test_image.png", img_byte_arr, "image/png")}
    response = requests.post(url, files=files)
    
    # 4. Print the result
    if response.status_code == 200:
        print("\n✅ Success! Response:")
        data = response.json()
        
        # Pretty print specific fields
        print(f"Prediction: {data['prediction']}")
        print(f"Confidence: {data['confidence_percentage']}")
        print(f"Dominant Region: {data['dominant_focus_region']}")
        print(f"\nExplanation:\n{data['explanation']}")
        
        # Don't print the huge base64 string
        print(f"\n(Heatmap image returned: {len(data['heatmap_image_base64'])} chars)")
    else:
        print(f"\n❌ Error {response.status_code}: {response.text}")

except requests.exceptions.ConnectionError:
    print("\n❌ Could not connect to the server.")
    print("Make sure you are running 'python main.py' in a separate terminal!")
