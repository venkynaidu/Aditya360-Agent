# Aditya360 Agent — Student Login + Agentic AI

## Setup
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` as `.env`, then add your Gemini API key.

```env
GEMINI_API_KEY=YOUR_KEY
GEMINI_MODEL=gemini-3.8-flash
```

Run:
```powershell
streamlit run app.py
```

## Student access
The front page provides:
- Student registration
- Student ID login
- Department/year profile
- Passwords stored as PBKDF2 hashes with unique salts
- SQLite student database
- Logged-in Aditya360 chat

For an institutional deployment, connect registration to the university's authoritative student database/SSO rather than allowing unrestricted self-registration.

## UI
The supplied Aditya360 PNG logo is displayed on a white rounded card. The interface uses a dark green/teal gradient, feature cards, industry AI/data quote and Venkys AI attribution.

## Production next steps
Add verified university RAG documents, institutional SSO, role-based access, admin approval, password reset, rate limiting, audit logging, HTTPS, database backups and privacy controls.


## Header UI revision

The Aditya360 logo is now rendered in a compact top-left white card with:
- rounded corners,
- subtle green border/glow,
- responsive desktop/mobile sizing,
- reduced hero whitespace,
- high contrast for the navy and green logo artwork.

The logo is embedded as base64 at runtime so the white rounded card reliably contains it in Streamlit.
