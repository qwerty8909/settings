import requests

url = "https://stablediffusionapi.com/api/v3/text2img"

payload = {"key": "4lTHuAaagxTcTbWcMg9gdl4yFus4RvoShLSvFkl9Qr7yjLrAzFI2nZViYQ0E",
           "prompt": "ultra realistic close up portrait ((beautiful pale cyberpunk female with heavy black "
                     "eyeliner)), blue eyes, shaved side haircut, hyper detail, cinematic lighting, magic neon, "
                     "dark red city, Canon EOS R3, nikon, f/1.4, ISO 200, 1/160s, 8K, RAW, unedited, symmetrical "
                     "balance, in-frame, 8K",
           "negative_prompt": "((out of frame)), ((extra fingers)), mutated hands, ((poorly drawn hands)), ((poorly "
                              "drawn face)), (((mutation))), (((deformed))), (((tiling))), ((naked)), ((tile)), "
                              "((fleshpile)), ((ugly)), (((abstract))), blurry, ((bad anatomy)), ((bad proportions)), "
                              "((extra limbs)), cloned face, (((skinny))), glitchy, ((extra breasts)), "
                              "((double torso)), ((extra arms)), ((extra hands)), ((mangled fingers)), "
                              "((missing breasts)), (missing lips), ((ugly face)), ((fat)), ((extra legs)), anime",
           "width": "512",
           "height": "512",
           "samples": "1",
           "num_inference_steps": "20",
           "safety_checker": "no",
           "enhance_prompt": "yes",
           "seed": None,
           "guidance_scale": 7.5,
           "webhook": None,
           "track_id": None}
headers = {}

response = requests.request("POST", url, headers=headers, data=payload)

print (''.join(eval(response.text.replace('null', '"null"'))['output']).replace('\\', ''))