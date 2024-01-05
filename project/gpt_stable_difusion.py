import requests

url = "https://stablediffusionapi.com/api/v3/dreambooth"

payload = {"key": "key",
           "model_id": 'realistic-vision-v13',
           "prompt": "Man on the moon, ultra hd selfie",
           "negative_prompt": None,
           "enhance_prompt": "no",
           "width": "512",
           "height": "512",
           "samples": "1",
           "num_inference_steps": "30",
           "guidance_scale": 7.5,
           "seed": None,
           }
headers = {}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
print (''.join(eval(response.text.replace('null', '"null"'))['output']).replace('\\', ''))