# codeforge

**A calm, no-clutter AI coding assistant — generate, debug, or explain code through a single focused interface.**

[![Status](https://img.shields.io/badge/status-active-brightgreen)](#)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](#)
![License](https://img.shields.io/badge/License-MIT-lightgrey)(#)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](#)
[![Flask](https://img.shields.io/badge/flask-3.x-black)](#)

<img width="2400" height="600" alt="image" src="https://github.com/user-attachments/assets/b65a5aa4-4cc9-4428-aa09-fa6b1ae2b503" />




---

## Table of Contents

- [Overview](#overview)
- [Motivation](#motivation)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Workflow](#workflow)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Screenshots](#screenshots)
- [Internal Endpoints](#internal-endpoints)
- [Performance](#performance)
- [Security](#security)
- [Advantages](#advantages)
- [Limitations](#limitations)
- [Real-World Applications](#real-world-applications)
- [Future Roadmap](#future-roadmap)
- [Challenges Faced](#challenges-faced)
- [Lessons Learned](#lessons-learned)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)
- [Acknowledgements](#acknowledgements)

---

## Overview

**codeforge** is a lightweight Flask web application that puts a large language model to work in three focused modes: writing new code from a description, diagnosing an error and proposing a fix, or explaining existing code in plain language.

It exists to remove the friction between "I have a coding problem" and "I have a clear answer" — one text box, one button, no navigation, no clutter. The interface is deliberately minimal: a single page, large legible type, and a small number of visible choices at any time.

**Who it's for:** students and developers who want a fast, distraction-free way to generate, debug, or understand code without switching between multiple tools or tabs.

**Key objectives:**
- Keep the interface simple enough to use without a learning curve
- Support more than one LLM provider so the user isn't locked to a single vendor
- Keep response formatting short and structured, especially for debugging output

---

## Motivation

Most AI coding assistants are bundled into larger IDEs or chat products with more surface area than a specific task needs. codeforge was built as a standalone, single-purpose tool: pick a mode, describe the problem, get an answer — nothing else competing for attention on the page.

It also serves as a practical exercise in structuring a small Flask application properly: separating routes, services, prompt templates, and model providers into distinct layers rather than one large file.

---

## Features

| Category | Feature | Description |
|---|---|---|
| Core functionality | Generate mode | Produces clean, working code from a plain-language description |
| Core functionality | Debug mode | Diagnoses an error and returns a short cause/fix/corrected-code response |
| Core functionality | Explain mode | Breaks existing code into a short, numbered, plain-language explanation |
| Technical capability | Multi-engine support | Switch between **Groq** and **Meta's Llama API** per request |
| User experience | Single-page interface | One form, one output panel, no navigation required |
| User experience | Immediate feedback | Button state changes to "Working…" on submit so the click is never ambiguous |
| User experience | Copy-to-clipboard | One click to copy the model's output |
| Accessibility | Legible typography | Built with Atkinson Hyperlegible, a typeface designed for reading clarity |
| Accessibility | Reduced motion respected | No ambient animation; `prefers-reduced-motion` is honored |
| Security | Environment-based secrets | API keys are read from `.env`, which is git-ignored by default |
| Scalability | Provider abstraction | Adding a new LLM provider requires one change in `model.py`, not a rewrite |
| Deployment readiness | Config via environment | No hardcoded credentials or endpoints in source |

---

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Web framework | Flask |
| Templating | Jinja2 |
| LLM orchestration | LangChain (`langchain-groq`, `langchain-openai`) |
| LLM providers | Groq (`openai/gpt-oss-120b`), Meta Llama API (OpenAI-compatible endpoint) |
| Frontend | HTML5, CSS3, vanilla JavaScript |
| Fonts | Atkinson Hyperlegible, JetBrains Mono |
| Config management | python-dotenv |
| Version control | Git / GitHub |
| Database | None — the app is stateless by design |
| Testing | Not yet implemented — see [Testing](#testing) |
| Deployment | Not yet configured — see [Deployment](#deployment) |

---

## Architecture

codeforge follows a simple layered structure: routes handle HTTP, services contain business logic, prompts hold provider-agnostic prompt templates, and a single model loader abstracts away which LLM provider actually answers the request.

```
                     ┌────────────────────┐
                     │      Browser        │
                     │  (index.html form)   │
                     └─────────┬────────────┘
                               │ POST /
                               ▼
                     ┌────────────────────┐
                     │   Flask Blueprint    │
                     │   (code_routes.py)    │
                     └─────────┬────────────┘
                               │ mode + engine + input
                               ▼
              ┌────────────────────────────────┐
              │           Services              │
              │  code.py / error.py / logic.py   │
              └───────┬─────────────────┬────────┘
                       │                 │
                       ▼                 ▼
             ┌──────────────┐   ┌──────────────────┐
             │   Prompts     │   │   Model Loader     │
             │ (templates)   │   │   (model.py)        │
             └──────────────┘   └─────────┬──────────┘
                                           │
                          ┌────────────────┴───────────────┐
                          ▼                                 ▼
                  ┌───────────────┐               ┌────────────────────┐
                  │  Groq API      │               │  Meta Llama API      │
                  │ (ChatGroq)     │               │ (OpenAI-compatible)   │
                  └───────────────┘               └────────────────────┘
```

---

## Workflow

1. User selects a **mode** (Generate, Debug, Explain) and an **engine** (Groq, Meta Llama).
2. User submits a description, error message, or code snippet.
3. Flask's `code_routes.py` reads the form data and calls the matching service.
4. The service loads the selected LLM via `model.py` and formats the request using the matching prompt template.
5. The model's response is returned and rendered directly back into the page — no client-side API calls, no exposed keys.

---

## Folder Structure

```
codeforge/
├── run.py                     # Application entry point
├── requirements.txt           # Python dependencies
├── .env.example                # Template for required environment variables
├── .gitignore                  # Excludes .env, venv/, __pycache__
└── app/
    ├── __init__.py              # Flask app factory
    ├── routes/
    │   └── code_routes.py        # Single blueprint handling GET/POST /
    ├── services/
    │   ├── code.py                # Generate-mode business logic
    │   ├── error.py               # Debug-mode business logic
    │   └── logic.py               # Explain-mode business logic
    ├── models/
    │   └── model.py                # Loads Groq or Meta Llama based on selection
    ├── prompts/
    │   ├── code_create.py          # Generate-mode prompt template
    │   ├── error_fix.py            # Debug-mode prompt template
    │   └── logic_explain.py        # Explain-mode prompt template
    ├── templates/
    │   └── index.html               # Single-page UI (Jinja2)
    └── static/
        └── css/
            └── style.css             # Styling
```

---

## Installation

**Prerequisites:** Python 3.10 or later, Git, a Groq API key, and (optionally) a Meta Llama API key.

```bash
# 1. Clone the repository
git clone https://github.com/jasminejayasmita786-commits/codeforge.git
cd codeforge

# 2. Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# then open .env and add your real API keys

# 5. Run the app
python run.py
```

The app runs at `http://127.0.0.1:5000` by default.

---

## Usage

1. Open the app in a browser.
2. Choose a mode:
   - **Generate** — describe what you want built
   - **Debug** — paste the failing code and the error message
   - **Explain** — paste code you want broken down step by step
3. Choose an engine — **Groq** or **Meta Llama**.
4. Type your input and press **Run** (or `Ctrl`/`⌘` + `Enter`).
5. Copy the output with the **Copy** button in the output panel.

---

## Configuration

Environment variables are read from `.env` (never committed — see `.gitignore`):

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Yes, for Groq engine | API key from [console.groq.com](https://console.groq.com) |
| `LLAMA_API_KEY` | Yes, for Meta Llama engine | API key from [llama.developer.meta.com](https://llama.developer.meta.com) |
| `LLAMA_MODEL` | No | Defaults to `Llama-4-Maverick-17B-128E-Instruct-FP8`; override to use a different Llama model |

---

## Screenshots



[![HOME](<img width="1897" height="996" alt="image" src="https://github.com/user-attachments/assets/ae525a01-1787-4d27-b276-665fb0d7e866" />

)]

[![OUTPUT-GENERATION](<img width="1881" height="931" alt="image" src="https://github.com/user-attachments/assets/07d41ae2-6df3-4d3e-87ea-298f21f25ffa" />

)]

[![O/P-DEBUG](<img width="1873" height="923" alt="image" src="https://github.com/user-attachments/assets/291e35b7-5063-42da-963a-66e318f55acb" />

)]

[![EXPLAIN CODE](<img width="1872" height="887" alt="image" src="https://github.com/user-attachments/assets/2bdfe9c0-24a1-4513-8fcc-c88cd72e8740" />

)]



---

## Internal Endpoints

codeforge does not expose a public JSON API — it's a server-rendered form, not a client-consumed API. For reference, the one internal route is:

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Renders the form with an empty output panel |
| `POST` | `/` | Accepts `mode`, `engine`, and `user_input`; renders the page with the model's response |

---

## Performance

- Each request is a single, synchronous call to the selected LLM provider — response time is dictated by that provider's latency, typically a few seconds.
- No caching layer exists yet; identical prompts are re-sent to the model each time.
- The app itself is stateless and holds no data between requests, so it imposes negligible overhead of its own.

---

## Security

- API keys live only in `.env`, which is excluded from version control via `.gitignore`.
- There is currently no user authentication — anyone with access to a running instance can use it and consume API credits. This is acceptable for local/personal use; **add authentication before deploying publicly.**
- User input is passed directly into prompt templates. This is a single-user local tool, not a hardened public-facing service — treat accordingly if exposing it beyond localhost.

---

## Advantages

- Minimal, focused interface with no unnecessary navigation or clutter
- Clean separation of routes, services, prompts, and model logic
- Provider-agnostic design — switching or adding LLM providers doesn't touch route or service code
- No database or external infrastructure required to run

---

## Limitations

- No conversation history or saved past results
- No automated tests yet
- No authentication or rate limiting
- Single synchronous request at a time — no streaming responses
- Local-first; no deployment configuration included yet

---

## Real-World Applications

- Personal coding assistant for students learning to debug and read code
- Quick-reference tool during coursework or side projects
- A base template for anyone building a small, focused LLM-powered internal tool

---

## Future Roadmap

- [ ] Add automated test suite
- [ ] Add conversation/output history
- [ ] Add streaming responses instead of full-page reload
- [ ] Add basic authentication for shared/public deployments
- [ ] Add Docker support
- [ ] Add CI/CD pipeline
- [ ] Deploy a public demo instance
- [ ] Add additional LLM providers
- [ ] Mobile-specific UI polish

---

## Challenges Faced

- Aligning form field names between the template and the Flask route required care, since a single mismatch silently breaks submission.
- Adding a second LLM provider without duplicating service logic meant centralizing provider selection into one `model.py` loader rather than branching in every service file.

---

## Lessons Learned

- Keeping routes, services, prompts, and model-loading in separate modules makes it straightforward to add a new mode or provider without touching unrelated code.
- A simple, consistent response format (short, structured output) matters as much as the underlying model for a good user experience in a debugging tool.

---

## Testing

No automated tests currently exist.

**Planned approach:**
- Unit tests for each service (`code.py`, `error.py`, `logic.py`) using mocked LLM responses
- Route-level tests using Flask's test client
- Test runner: `pytest` (to be added to `requirements.txt`)

---

## Deployment

Not yet configured. Suggested paths once ready:
- **Render / Railway / Fly.io** — simple Flask deployment with environment variable support
- **Docker** — containerize with a `Dockerfile` once added (see roadmap)

Regardless of platform, `GROQ_API_KEY` and `LLAMA_API_KEY` must be set as environment variables on the host — never committed to the repository.

---

## Contributing

1. Fork the repository and create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes, keeping the existing routes/services/prompts/models separation
3. Commit with a clear message: `git commit -m "Add: short description"`
4. Push and open a pull request describing the change and why it's needed
5. For bugs, open an issue with steps to reproduce and expected vs. actual behavior

---

## License

Add your preferred license (e.g., MIT) as a `LICENSE` file in the repository root and update the badge above.

---

## Author

**Jasmine Jayasmita (Jasss)**
- GitHub: [@jasminejayasmita786-commits](https://github.com/jasminejayasmita786-commits)
- LinkedIn: [jasminejayasmitasoa](https://www.linkedin.com/in/jasminejayasmitasoa/)
- Email: [MAIL it out !](jasminejayasmita786@gmail.com)

---

## Acknowledgements

- [Groq](https://groq.com) for fast LLM inference
- [Meta Llama API](https://llama.developer.meta.com) for OpenAI-compatible open-model access
- [LangChain](https://www.langchain.com) for provider orchestration
- [Atkinson Hyperlegible](https://brailleinstitute.org/freefont) for the interface typeface
