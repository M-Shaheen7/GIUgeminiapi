# 🤖 GIU Gemini API — Build It. Ship It. Secure It.

> A hands-on project built live across 3 talks at **AWS Cloud Clubs @ German International University**.
> Three speakers. One repo. A Gemini-powered API that got built, containerized, deployed to AWS Lambda, and secured — step by step.

---

## 🗓️ The Series

| Talk | Date | Speaker | What Changed |
|------|------|---------|--------------|
| Talk 1 — Backend Dev | Thu, 12 March 2026 | Backend Engineer | Built the FastAPI + Gemini wrapper |
| Talk 2 — DevOps & Cloud | Sat, 14 March 2026 | DevOps Engineer | Dockerized + deployed to AWS Lambda |
| Talk 3 — Security | Tue, 17 March 2026 | Security Engineer | Secured secrets + configured IAM |

Each talk is tagged in the commit history: `v1.0`, `v2.0`, `v3.0`

---

## 🧠 What This Project Does

A simple REST API with one endpoint — `POST /chat` — that accepts a text prompt and returns a response from Google's Gemini AI model.

```
POST /chat
Body: { "prompt": "Explain APIs in one sentence" }
Response: { "response": "An API is a contract between two programs..." }
```

---

## 🚀 Quick Start (Local)

### 1. Clone the repo

```bash
git clone https://github.com/[YOUR_ORG]/giu-gemini-api.git
cd giu-gemini-api
```

### 2. Set up a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your real Gemini API key:

```
GEMINI_API_KEY=your_actual_key_here
```

> Get a free Gemini API key at [Google AI Studio](https://aistudio.google.com/app/apikey)

### 5. Run the API

```bash
uvicorn main:app --reload
```

The API is now running at `http://localhost:8000`

### 6. Test it

```bash
# Using curl
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is a REST API?"}'

# Or open the interactive docs
http://localhost:8000/docs
```

---

## 🐳 Running with Docker (Talk 2)

### Build the image

```bash
docker build -t giu-gemini-api .
```

### Run the container

```bash
docker run -p 8000:8000 --env-file .env giu-gemini-api
```

The API is now running inside a container at `http://localhost:8000`

---

## ☁️ Deploying to AWS Lambda (Talk 2)

> Requires: AWS account (free tier), AWS CLI configured, Docker installed

### 1. Create an ECR repository

```bash
aws ecr create-repository --repository-name giu-gemini-api --region us-east-1
```

### 2. Authenticate Docker with ECR

```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  [YOUR_ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com
```

### 3. Tag and push the image

```bash
docker tag giu-gemini-api:latest \
  [YOUR_ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/giu-gemini-api:latest

docker push \
  [YOUR_ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/giu-gemini-api:latest
```

### 4. Create the Lambda function

In the AWS Console:
1. Go to **Lambda → Create function**
2. Choose **Container image**
3. Select the image you just pushed from ECR
4. Set **Architecture** to `x86_64`
5. Under **Configuration → Environment variables**, add:
   - Key: `GEMINI_API_KEY` | Value: your actual key
6. Under **Configuration → Function URL**, enable it (Auth: NONE for public access)

Your API is now live at the Function URL shown in the console.

---

## 🔐 Security Setup (Talk 3)

### Why environment variables?

The API key should **never** appear in your source code. Here's the right setup:

**Local development** — `.env` file (never committed):
```
GEMINI_API_KEY=your_actual_key_here
```

**Production (Lambda)** — set in the AWS Lambda console under Configuration → Environment Variables. Never hardcode it in `main.py`.

**The `.gitignore` rule** — this repo has `.env` in `.gitignore`, which means Git will never commit it, even if you run `git add .`.

```
# .gitignore
.env
.venv/
__pycache__/
*.pyc
```

### IAM — least privilege

The Lambda execution role should have only the permissions it needs. For this project, the role needs:
- `logs:CreateLogGroup` — to write Lambda logs
- `logs:CreateLogStream`
- `logs:PutLogEvents`

It should **not** have admin access or access to other AWS services.

To check your Lambda's role: Console → Lambda → Configuration → Permissions → Execution role.

### What NOT to do

```python
# ❌ NEVER do this
GEMINI_API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXX"

# ✅ Always do this
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
```

---

## 📁 Project Structure

```
giu-gemini-api/
├── main.py              # FastAPI app — the /chat endpoint
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container definition (added in Talk 2)
├── .dockerignore        # Keeps the image lean
├── .env                 # Your real API key — NEVER commit this
├── .env.example         # Template — safe to commit
├── .gitignore           # Excludes .env and other sensitive files
├── README.md            # This file
└── CHANGELOG.md         # What changed in each talk
```

---

## 📦 Dependencies

```
fastapi
uvicorn[standard]
google-generativeai
python-dotenv
```

Install all: `pip install -r requirements.txt`

---

## 📝 Changelog

### v3.0 — Talk 3: Security (17 March 2026)
- Removed hardcoded API key from `main.py`
- Added `os.environ.get()` to read key from environment
- Added `.env` and `.env.example`
- Updated `.gitignore` to exclude `.env`
- Added Lambda environment variable setup instructions to README

### v2.0 — Talk 2: DevOps (14 March 2026)
- Added `Dockerfile` for containerized deployment
- Added `.dockerignore`
- Added AWS Lambda deployment instructions to README

### v1.0 — Talk 1: Backend (12 March 2026)
- Initial FastAPI app with `GET /` health check
- `POST /chat` endpoint with Gemini integration
- `requirements.txt`
- Basic README

---

## 🙏 Credits

Built live at **AWS Cloud Clubs @ German International University**
Series: **Build It. Ship It. Secure It.** — March 2026

| Role | Speaker |
|------|---------|
| Backend Engineer (Talk 1) | [SPEAKER 1 NAME] |
| DevOps Engineer (Talk 2) | [SPEAKER 2 NAME] |
| Security Engineer (Talk 3) | [SPEAKER 3 NAME] |
| Organized by | AWS Cloud Clubs @ GIU |

---

## 💡 What Next?

Now that you have a working API — here are ideas to extend it:

- Add a `POST /summarize` endpoint that summarizes a long text
- Add basic API key authentication using a header (`X-API-Key`)
- Add a rate limiter using `slowapi`
- Set up a GitHub Actions workflow that redeploys to Lambda on every push
- Add logging with AWS CloudWatch
- Try swapping Gemini for OpenAI or another model

If you build something cool on top of this — share it with the club!

---

*AWS Cloud Clubs @ German International University | 2026*
