<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=14,20,28&height=170&section=header&text=AI%20Code%20Review%20Bot&fontSize=48&fontAlignY=35&animation=twinkling&fontColor=ffffff&desc=Automated%20PR%20Reviews%20with%20Claude%20%7C%20LLMOps%20Pipeline&descAlignY=55&descSize=18" width="100%" />

[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](.)
[![Claude API](https://img.shields.io/badge/Claude-Powered-8B5CF6?style=for-the-badge&logo=anthropic&logoColor=white)](.)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](.)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](.)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**Every Pull Request reviewed automatically. Catches bugs, security issues, and code smells before merge.**

[How It Works](#how-it-works) · [Setup](#setup-2-minutes) · [Evaluation](#evaluation-results) · [Cost Analysis](#cost-analysis)

</div>

---

## What This Is

An AI-powered code review bot that **automatically reviews every Pull Request** on GitHub using Claude (Anthropic API). It catches bugs, security issues, and code quality problems — then posts the review as a PR comment.

**This is an LLMOps project** — the value isn't just the AI review, it's the production infrastructure around it: CI/CD integration, prompt versioning, automated evaluation, cost monitoring, and containerization.

---

## How It Works

```
Developer opens Pull Request
         │
         ▼
GitHub Actions triggers automatically
         │
         ▼
Workflow extracts code diff (only code files)
         │
         ▼
Diff sent to Claude API with versioned prompt
         │
         ▼
Claude analyzes: bugs, security, performance, readability
         │
         ▼
Review posted as PR comment with structured feedback
         │
         ▼
Metrics logged: tokens, cost, latency
```

---

## LLMOps Components

| Component | Implementation | Why It Matters |
|-----------|---------------|----------------|
| **Model Serving** | Anthropic Claude API | Production LLM integration |
| **CI/CD** | GitHub Actions on every PR | Automated pipeline |
| **Prompt Management** | Versioned .txt templates (v1, v2) | Prompt engineering best practice |
| **Evaluation Pipeline** | 5 known-bug test cases | Automated quality assurance |
| **Prompt A/B Testing** | Compare v1_basic vs v2_detailed | Data-driven prompt selection |
| **Cost Monitoring** | Token counting + USD calculation per review | Budget awareness |
| **Latency Tracking** | Response time logged per review | Performance monitoring |
| **Containerization** | Dockerfile | Reproducible deployment |
| **Error Handling** | Retry logic, graceful fallbacks | Production reliability |

---

## Project Structure

```
ai-code-review-bot/
├── .github/workflows/
│   └── ai-code-review.yml          # GitHub Actions — triggers on PR
├── src/
│   ├── review.py                    # Core review engine (Claude API)
│   └── prompts/
│       ├── v1_basic.txt             # Simple review prompt
│       └── v2_detailed.txt          # Detailed 5-category review prompt
├── tests/
│   └── test_known_bugs.py           # Evaluation: SQL injection, div/0, etc.
├── Dockerfile                       # Container for reproducibility
├── requirements.txt
└── README.md
```

---

## Setup (2 Minutes)

### 1. Add your Anthropic API key to GitHub Secrets

Go to your repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret** → Name: `ANTHROPIC_API_KEY`

### 2. That's it.

The bot will automatically run on every PR. Open a PR with any code change and watch it review.

---

## Run Evaluation Locally

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"

python tests/test_known_bugs.py            # Test if bot catches known bugs
python tests/test_known_bugs.py --compare  # Compare prompt versions (A/B test)
python src/review.py my_changes.diff       # Review a specific diff file
```

### Run with Docker

```bash
docker build -t ai-code-review .
docker run -e ANTHROPIC_API_KEY="your-key" ai-code-review
```

---

## Evaluation Results

The bot is tested against 5 known buggy code patterns:

| Test Case | Category | Description |
|-----------|----------|-------------|
| SQL Injection | Security | `f"SELECT * FROM users WHERE name = '{input}'"` |
| Hardcoded API Key | Security | `API_KEY = "sk-abc123..."` |
| Division by Zero | Bug | `total / len(numbers)` without empty check |
| Missing Error Handling | Bug | `open(file)` without try/except or context manager |
| Infinite Loop Risk | Bug | `while True` without break condition |

---

## Prompt Versions

**v1_basic** — Simple one-line instruction. Fast but catches fewer issues.

**v2_detailed** — Structured 5-category review (correctness, security, performance, readability, best practices). Costs more tokens but catches more bugs.

The evaluation suite compares both to help you pick the right one for your use case — this is **prompt A/B testing** in practice.

---

## Cost Analysis

| Metric | Value |
|--------|-------|
| Cost per review | ~$0.003-0.01 |
| Reviews per $1 | ~100-300 |
| Monthly cost (10 PRs/day) | ~$1-3 |
| Equivalent senior eng time saved | ~30 min/PR |

---

## Key Learnings

| Insight | Detail |
|---------|--------|
| Prompt versioning matters | v2 catches significantly more issues than v1 |
| Automated evaluation is essential | Without test cases, you can't measure prompt improvements |
| Cost tracking from day 1 | LLM APIs get expensive fast without monitoring |
| CI/CD integration | The bot is only useful if it runs automatically |
| Structured output | Forcing categories (Bug/Security/Performance/Readability) makes reviews scannable |

---

## Tech Stack

`Python` `Anthropic Claude API` `GitHub Actions` `Docker` `CI/CD` `Prompt Engineering` `LLMOps`

---

## Related Projects

| Project | Description |
|---------|-------------|
| [Advanced Resume Analyzer (QLoRA)](https://github.com/ajay-automates/advanced-resume-analyzer-qlora) | Fine-tuned Gemma 3 4B with QLoRA |
| [AI Support Agent](https://github.com/ajay-automates/ai-support-agent) | RAG chatbot with LangSmith observability |
| [AI Image Classifier API](https://github.com/ajay-automates/ai-image-classifier-api) | Self-hosted CLIP inference |

---

<div align="center">

**Built by [Ajay Kumar Reddy Nelavetla](https://github.com/ajay-automates)** · February 2026

*Automated code review that catches real bugs — not just lint warnings.*

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=14,20,28&height=100&section=footer" width="100%" />

</div>
