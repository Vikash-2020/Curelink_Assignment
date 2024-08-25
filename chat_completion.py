from openai import AzureOpenAI
from app_secrets import azure_endpoint, azure_api_key, model, azure_api_version

client = AzureOpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_version= azure_api_version,
    api_key=azure_api_key,
    base_url=azure_endpoint
)


def get_completion(messages=None, temperature=0, max_tokens=800, top_p=1, frequency_penalty=0, presence_penalty=0, stop=None):
    # Set default values if parameters are not provided
    messages = messages or []
    
    # Make API call with provided parameters
    response = client.chat.completions.create(
        messages= messages,
        # model="DanielGPT4",
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop
    )
    return response.choices[0].message