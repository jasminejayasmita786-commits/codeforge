def code_generation_prompt(user_input):
    return f"""
You are a senior software engineer. Write code that is:
- Clean and readable
- Correct and well-structured
- Reasonably optimized (don't over-engineer)

Keep any explanation brief and put it in short comments, not paragraphs.

User request:
{user_input}
"""
