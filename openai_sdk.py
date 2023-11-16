import openai

# Setting up the deployment name
deployment_name = "bv-pcbv-des"

# This is set to `azure`
openai.api_type = "azure"

# The API key for your Azure OpenAI resource.
openai.api_key = "5ea3f79dfa544a26bddb70dd74277a54"

# The base URL for your Azure OpenAI resource. e.g. "https://<your resource name>.openai.azure.com"
openai.api_base = "https://cs-bv-pcbv-des.openai.azure.com"

# Currently OPENAI API have the following versions available: 2022-12-01
openai.api_version = "2022-12-01"

# Give your prompt here
prompt = "##### Explain this code Visual Basic: \nSub HelloWorld()\n MsgBox \"Hello, World!\"\nEnd Sub\" \n\n###"
try:
    # Create a completion for the provided prompt and parameters
    # To know more about the parameters, checkout this documentation: https://learn.microsoft.com/en-us/azure/cognitive-services/openai/reference
    completion = openai.Completion.create(
                    prompt=prompt,
                    temperature=0,
                    max_tokens=150,
                    model="text-davinci-003",
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                    stop=["###"],
                    engine=deployment_name)

    # print the completion
    print(completion.choices[0].text.strip(" \n"))
    
except Exception as e:
    # Handle request timeout
    print(f"Error Message: {e}")