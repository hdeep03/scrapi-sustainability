from groq import Groq
from models.result import EmissionsData
import instructor
import os
import google.generativeai as genai


key = "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"
gemini_key = "AIzaSyAjqiYeA1CXDiCc37jjA4kOnMszbqCHFLg"


genai.configure(api_key=gemini_key)
client = instructor.from_groq(Groq(api_key=key), mode=instructor.Mode.JSON)

model = genai.GenerativeModel("gemini-1.5-flash")

def get_emissions_data_groq(text: str):
    results: EmissionsData = client.chat.completions.create(
        model="llama3-groq-8b-8192-tool-use-preview",
        response_model=EmissionsData,
        messages=[
            {"role": "system", "content": "Extracting scope 1, scope 2, and scope 3 emissions from the text. UNITS ARE IN METRIC TONS OF CO2, convert if necessary."},
            {"role": "user", "content": f"Extract scope 1, scope 2, and scope 3 emissions in metric tons of CO2 from the following text if present:\n\n\n {text}"},
        ],
    )
    return results

def get_emissions_data_gemini(text: str):
    result = model.generate_content(
        f"Extract scope 1, scope 2, and scope 3 emissions in millions of metric tons of CO2 from the following text if present: \n\n\n {text}",
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=EmissionsData
        ),
    )
    return EmissionsData.model_validate_json(result.candidates[0].content.parts[0].text)



if __name__ == "__main__":
    text = """"""
    print(get_emissions_data_gemini(text))
