"""
AI Code Review Bot — Core Review Engine
Uses Claude (Anthropic API) to review code diffs from Pull Requests.
Supports versioned prompts, cost tracking, and structured output.
"""

import os
import sys
import json
import time
import anthropic
from datetime import datetime, timezone


# ============================================================
# CONFIGURATION
# ============================================================
MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 2048
MAX_DIFF_LENGTH = 8000  # Truncate very large diffs

# Cost per token (Claude Sonnet pricing as of 2025)
INPUT_COST_PER_1K = 0.003
OUTPUT_COST_PER_1K = 0.015


# ============================================================
# PROMPT LOADING (Versioned Prompts)
# ============================================================
def load_prompt(version="v2_detailed"):
    """Load a versioned prompt template from the prompts directory."""
    prompt_dir = os.path.join(os.path.dirname(__file__), "prompts")
    prompt_file = os.path.join(prompt_dir, f"{version}.txt")

    if not os.path.exists(prompt_file):
        print(f"Warning: Prompt {prompt_file} not found, using default")
        return get_default_prompt()

    with open(prompt_file, "r") as f:
        return f.read()


def get_default_prompt():
    return """You are a senior software engineer performing a code review.
Analyze the following code diff and provide actionable feedback.
Focus on: bugs, security issues, performance, readability, and best practices.
Be concise and specific. Reference line numbers when possible."""


# ============================================================
# CODE REVIEW FUNCTION
# ============================================================
def review_code(diff: str, prompt_version: str = "v2_detailed") -> dict:
    """
    Send a code diff to Claude for review.

    Args:
        diff: The git diff string
        prompt_version: Which prompt template to use

    Returns:
        dict with: review, tokens, cost, latency, model, prompt_version
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {"error": "ANTHROPIC_API_KEY not set", "review": "⚠️ API key missing. Cannot perform review."}

    # Truncate very large diffs
    if len(diff) > MAX_DIFF_LENGTH:
        diff = diff[:MAX_DIFF_LENGTH] + "\n\n... [DIFF TRUNCATED — too large for single review] ..."

    # Load versioned prompt
    system_prompt = load_prompt(prompt_version)

    user_message = f"""Please review the following code changes from a Pull Request:

```diff
{diff}
```

Provide your review in this format:

## 🤖 AI Code Review

### Summary
(1-2 sentence overview of the changes)

### Issues Found
(List any bugs, security issues, or problems. Use ⚠️ for warnings, 🐛 for bugs, 🔒 for security)

### Suggestions
(Improvements for readability, performance, or best practices)

### Overall Assessment
(One of: ✅ Looks Good | ⚠️ Minor Issues | 🔴 Needs Changes)
"""

    # Call Claude API
    client = anthropic.Anthropic(api_key=api_key)

    start_time = time.time()

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
    except anthropic.APIError as e:
        return {
            "error": str(e),
            "review": f"⚠️ AI review failed: {str(e)}",
            "latency_ms": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "cost_usd": 0,
        }

    latency_ms = (time.time() - start_time) * 1000

    # Extract response
    review_text = response.content[0].text
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens

    # Calculate cost
    cost = (input_tokens / 1000 * INPUT_COST_PER_1K) + (output_tokens / 1000 * OUTPUT_COST_PER_1K)

    result = {
        "review": review_text,
        "model": MODEL,
        "prompt_version": prompt_version,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "cost_usd": round(cost, 6),
        "latency_ms": round(latency_ms, 1),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "diff_length": len(diff),
    }

    return result


# ============================================================
# MONITORING: Log metrics to file
# ============================================================
def log_metrics(result: dict, log_file: str = "review_metrics.jsonl"):
    """Append review metrics to a JSONL log file for monitoring."""
    metrics = {k: v for k, v in result.items() if k != "review"}
    with open(log_file, "a") as f:
        f.write(json.dumps(metrics) + "\n")


# ============================================================
# CLI ENTRY POINT
# ============================================================
if __name__ == "__main__":
    # Read diff from stdin or file
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            diff = f.read()
    else:
        diff = sys.stdin.read()

    if not diff.strip():
        print("No diff provided. Usage: python review.py <diff_file>")
        sys.exit(1)

    print("🤖 Running AI code review...")
    result = review_code(diff)

    if "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)

    print(result["review"])
    print(f"\n--- Metrics ---")
    print(f"Model: {result['model']}")
    print(f"Tokens: {result['total_tokens']} (in: {result['input_tokens']}, out: {result['output_tokens']})")
    print(f"Cost: ${result['cost_usd']:.6f}")
    print(f"Latency: {result['latency_ms']:.0f}ms")

    log_metrics(result)
