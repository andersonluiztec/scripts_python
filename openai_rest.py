import requests
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api_url = f"https://cs-bv-pcbv-des.openai.azure.com/openai/deployments/bv-pcbv-des/completions?api-version=2022-12-01"

json_data = {
  "model": "text-davinci-003",
  "prompt": "##### Translate this code from Visual Basic to Java\n### Visual Basic\n\nSub HelloWorld()\n MsgBox \"Hello, World!\"\nEnd Sub\" \n\n###",
  "temperature": 0,
  "max_tokens": 150,
  "top_p": 1.0,
  "frequency_penalty": 0.0,
  "presence_penalty": 0.0,
  "stop": ["###"]
}

headers =  {"api-key": "5ea3f79dfa544a26bddb70dd74277a54"}

try:
    response = requests.post(api_url, json=json_data, headers=headers, verify=False)
    completion = response.json()
    
    print(completion['choices'][0]['text'])
    
    if completion['choices'][0]['finish_reason'] == "content_filter":
        print("The generated content is filtered.")
except:
    print("An exception has occurred. \n")
    print("Error Message:", completion['error']['message'])