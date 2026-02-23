# 🤖 AI Code Review Bot — LLMOps Project

**Author:** Ajay Kumar Reddy Nelavetla  
**Date:** February 2026  
**Type:** End-to-End LLMOps Pipeline

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
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

---

## Setup (2 minutes)

### 1. Add your Anthropic API key to GitHub Secrets

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `ANTHROPIC_API_KEY`
4. Value: your Anthropic API key
5. Click **Add secret**

### 2. That's it!

The bot will automatically run on every PR. Open a PR with any code change and watch it review.

---

## Run Evaluation Locally

```bash
# Install
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY="your-key-here"

# Run evaluation (tests if bot catches known bugs)
python tests/test_known_bugs.py

# Compare prompt versions (A/B test)
python tests/test_known_bugs.py --compare

# Review a specific diff file
python src/review.py my_changes.diff
```

---

## Run with Docker

```bash
docker build -t ai-code-review .
docker run -e ANTHROPIC_API_KEY="your-key" ai-code-review
```

---

## Prompt Versions

### v1_basic
Simple one-line instruction. Fast but catches fewer issues.

### v2_detailed  
Structured 5-category review (correctness, security, performance, readability, best practices). Costs more tokens but catches more bugs.

The evaluation suite compares both to help you pick the right one for your use case — this is **prompt A/B testing** in practice.

---

## Evaluation Results

The bot is tested against 5 known buggy code patterns:

| Test Case | Category | Description |
|-----------|----------|-------------|
| SQL Injection | 🔒 Security | `f"SELECT * FROM users WHERE name = '{input}'"` |
| Hardcoded API Key | 🔒 Security | `API_KEY = "sk-abc123..."` |
| Division by Zero | 🐛 Bug | `total / len(numbers)` without empty check |
| Missing Error Handling | 🐛 Bug | `open(file)` without try/except or context manager |
| Infinite Loop Risk | 🐛 Bug | `while True` without break condition |

Run `python tests/test_known_bugs.py` to see live results.

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

1. **Prompt versioning matters** — v2 catches significantly more issues than v1
2. **Automated evaluation is essential** — without test cases, you can't measure prompt improvements
3. **Cost tracking from day 1** — LLM APIs get expensive fast without monitoring
4. **CI/CD integration** — the bot is only useful if it runs automatically, not manually
5. **Structured output** — forcing the LLM to use categories (🐛🔒⚡📖) makes reviews scannable

---

## Technologies

`Python` `Anthropic Claude API` `GitHub Actions` `Docker` `CI/CD` `Prompt Engineering` `LLMOps`

---

## Related Projects

- [Advanced Resume Analyzer (QLoRA Fine-Tuning)](https://github.com/ajay-automates/advanced-resume-analyzer-qlora) — Fine-tuned Gemma 3 4B with QLoRA
- [Interview Avatar (RAG)](https://github.com/ajay-automates) — RAG-powered mock interview system

---

*Built with 🔥 in February 2026*
