from flask import Blueprint, render_template, request
from app.services.code import generate_code
from app.services.error import solve_error
from app.services.logic import explain_logic

code_bp = Blueprint('code', __name__)


@code_bp.route('/', methods=['GET', 'POST'])
def home():
    response = ""
    mode = "Generate"
    engine = "groq"

    if request.method == 'POST':
        user_input = request.form.get('user_input', '')
        mode = request.form.get('mode', 'Generate')
        engine = request.form.get('engine', 'groq')

        if mode == 'Generate':
            response = generate_code(user_input, engine)
        elif mode == 'Debug':
            response = solve_error(user_input, engine)
        elif mode == 'Explain':
            response = explain_logic(user_input, engine)

    return render_template('index.html', response=response, mode=mode, engine=engine)
