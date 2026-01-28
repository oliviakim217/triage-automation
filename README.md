# Jira Story Creator

Simple app to create Jira stories.


## Configuration

### Generate password hash

```bash
python -c "import bcrypt; print(bcrypt.hashpw(b'your-password', bcrypt.gensalt()).decode())"
```

### Generate session secret

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```


## Run locally

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows
# source .venv/bin/activate    # macOS/Linux
pip install -r requirements.txt
python server3.py
```

Open http://localhost:8000

