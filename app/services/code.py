from app.models.model import load_llm
from app.prompts.code_create import code_generation_prompt


def generate_code(user_input, engine="groq"):
    llm = load_llm(engine)
    prompt = code_generation_prompt(user_input)
    result = llm.invoke(prompt)
    return result.content
