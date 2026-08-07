from app.models.model import load_llm
from app.prompts.logic_explain import logic_explainer_prompt


def explain_logic(user_input, engine="groq"):
    llm = load_llm(engine)
    prompt = logic_explainer_prompt(user_input)
    result = llm.invoke(prompt)
    return result.content
