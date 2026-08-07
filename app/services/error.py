from app.models.model import load_llm
from app.prompts.error_fix import error_solver_prompt


def solve_error(user_input, engine="groq"):
    llm = load_llm(engine)
    prompt = error_solver_prompt(user_input)
    result = llm.invoke(prompt)
    return result.content
