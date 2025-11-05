import os
from dotenv import load_dotenv
from google import genai
import json
import re
load_dotenv()

class GeminiClient:
    '''
    THIS IS A SIMPLE WRAPPER AROUND THE GOOGLE GEMINI API USING THE OFFICIAL GOOGLE GENAI LIBRARY.
    ARGS:
        api_key: YOUR GOOGLE GEMINI API KEY OR SERVICE ACCOUNT CREDENTIAL STRING.
    METHODS:
        generate_text(prompt, model): GENERATES TEXT BASED ON THE PROMPT USING THE SPECIFIED MODEL.
    '''
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = genai.Client(api_key=self.api_key)

    def generate_text(self, prompt, model="gemini-2.5-flash")-> str:
        response = self.client.models.generate_content(
            model=model,
            contents=prompt
        )
        return response.text

class StructuralClient:
    '''
    This is the class for structural and logical reasoning tasks.
    It first breaks down the problem into smaller sections and give each section to Gemini for processing in PARALLEL.
    Finally, it combines the results from each section to produce a final answers.
    '''
    def __init__(self, gemini_client: GeminiClient):
        self.llm_structural  = gemini_client

    def generate_structural_response(self, prompt: str):
        structure_prompt_template = f"""
You are a planning module for a parallel large language model system.

The system divides complex questions into smaller reasoning sections.
Each section is processed by a separate worker LLM in parallel.

Your task:
1. Read the user's question: "{prompt}"
2. Determine how many logical sections are required to answer it clearly and completely.
3. For each section, write:
   - A clear section title
   - A short instruction for that section
4. Decide the minimum number of worker nodes required (equal to the number of sections).
5. Ensure that sections are **non-overlapping**, **logically ordered**, and **cover all key aspects**.

Return your answer in **strict JSON** with this exact format:
{{
  "num_workers": <number_of_sections>,
  "sections": [
    {{
      "title": "Section 1 Title",
      "instruction": "Describe what this section should include."
    }},
    {{
      "title": "Section 2 Title",
      "instruction": "..."
    }}
  ]
}}
""" 
        response = self.llm_structural.generate_text(prompt=structure_prompt_template)
        return response
        
def structural_responsetojson(response: str):
    match =  re.search(r"```json\s*(\{.*?\})\s*```", response, re.DOTALL)
    if match:
        response = match.group(1)
    else:
        response = response.strip()
    try:
        response_json = json.loads(response)
        return response_json
    except json.JSONDecodeError:
        print("Error: Response is not valid JSON.")
        return None



def main():

    llm1 = StructuralClient(GeminiClient(api_key=os.getenv("GEMINI_API_KEY")))
    
    response = llm1.generate_structural_response(prompt="explain quantum computing in simple terms")
    response = structural_responsetojson(response)
    print(response)    

    pass
if __name__ == "__main__":
    main()