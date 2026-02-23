"""
Evaluation Suite: Test the AI reviewer against known buggy code samples.
Checks if the LLM catches real bugs in code diffs.
"""

import os
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from review import review_code

# ============================================================
# KNOWN BUGGY CODE SAMPLES
# Each has a diff, the expected issue, and a check function
# ============================================================
TEST_CASES = [
    {
        "name": "SQL Injection vulnerability",
        "diff": '''
+def get_user(username):
+    query = f"SELECT * FROM users WHERE name = '{username}'"
+    cursor.execute(query)
+    return cursor.fetchone()
''',
        "must_catch": ["sql injection", "sql", "injection", "parameterized", "sanitiz"],
        "category": "security"
    },
    {
        "name": "Hardcoded API key",
        "diff": '''
+API_KEY = "sk-abc123secretkey456"
+def call_api():
+    headers = {"Authorization": f"Bearer {API_KEY}"}
+    return requests.get("https://api.example.com/data", headers=headers)
''',
        "must_catch": ["hardcoded", "secret", "key", "environment", "env"],
        "category": "security"
    },
    {
        "name": "Division by zero",
        "diff": '''
+def calculate_average(numbers):
+    total = sum(numbers)
+    return total / len(numbers)
''',
        "must_catch": ["division by zero", "empty", "zero", "len(numbers) == 0", "check"],
        "category": "bug"
    },
    {
        "name": "Missing error handling",
        "diff": '''
+def read_config(path):
+    f = open(path, 'r')
+    data = json.load(f)
+    return data
''',
        "must_catch": ["error", "exception", "try", "with", "close", "context manager"],
        "category": "bug"
    },
    {
        "name": "Infinite loop risk",
        "diff": '''
+def process_queue(queue):
+    while True:
+        item = queue.get()
+        process(item)
''',
        "must_catch": ["infinite", "break", "exit", "condition", "stop", "termination"],
        "category": "bug"
    },
]


def run_evaluation(prompt_version="v2_detailed"):
    """Run all test cases and report results."""
    print(f"{'='*60}")
    print(f"EVALUATION: Testing prompt version '{prompt_version}'")
    print(f"{'='*60}")

    results = []
    passed = 0
    total = len(TEST_CASES)

    for i, test in enumerate(TEST_CASES):
        print(f"\n--- Test {i+1}/{total}: {test['name']} ---")

        result = review_code(test["diff"], prompt_version=prompt_version)

        if "error" in result:
            print(f"  ❌ API Error: {result['error']}")
            results.append({"test": test["name"], "passed": False, "reason": "API error"})
            continue

        review_lower = result["review"].lower()
        caught = any(keyword in review_lower for keyword in test["must_catch"])

        if caught:
            passed += 1
            print(f"  ✅ CAUGHT — Bot detected the {test['category']} issue")
        else:
            print(f"  ❌ MISSED — Bot did NOT catch the {test['category']} issue")
            print(f"  Expected keywords: {test['must_catch']}")

        results.append({
            "test": test["name"],
            "category": test["category"],
            "passed": caught,
            "tokens": result["total_tokens"],
            "cost": result["cost_usd"],
            "latency_ms": result["latency_ms"],
        })

    # Summary
    accuracy = passed / total if total > 0 else 0
    total_cost = sum(r.get("cost", 0) for r in results)
    avg_latency = sum(r.get("latency_ms", 0) for r in results) / max(len(results), 1)

    print(f"\n{'='*60}")
    print(f"EVALUATION RESULTS — Prompt: {prompt_version}")
    print(f"{'='*60}")
    print(f"Passed: {passed}/{total} ({accuracy:.0%})")
    print(f"Total cost: ${total_cost:.6f}")
    print(f"Avg latency: {avg_latency:.0f}ms")

    for r in results:
        status = "✅" if r["passed"] else "❌"
        print(f"  {status} {r['test']}")

    return {"prompt_version": prompt_version, "accuracy": accuracy, "passed": passed,
            "total": total, "cost": total_cost, "avg_latency_ms": avg_latency, "details": results}


def compare_prompts():
    """A/B test: Compare v1 (basic) vs v2 (detailed) prompts."""
    print("\n" + "="*60)
    print("PROMPT A/B TEST: v1_basic vs v2_detailed")
    print("="*60)

    r1 = run_evaluation("v1_basic")
    r2 = run_evaluation("v2_detailed")

    print(f"\n{'='*60}")
    print(f"A/B TEST COMPARISON")
    print(f"{'='*60}")
    print(f"{'Metric':<20} {'v1_basic':>12} {'v2_detailed':>12}")
    print(f"{'-'*44}")
    print(f"{'Accuracy':<20} {r1['accuracy']:>11.0%} {r2['accuracy']:>11.0%}")
    print(f"{'Cost':<20} ${r1['cost']:>10.6f} ${r2['cost']:>10.6f}")
    print(f"{'Avg Latency':<20} {r1['avg_latency_ms']:>10.0f}ms {r2['avg_latency_ms']:>10.0f}ms")

    winner = "v2_detailed" if r2["accuracy"] >= r1["accuracy"] else "v1_basic"
    print(f"\nWinner: {winner}")

    return {"v1": r1, "v2": r2, "winner": winner}


if __name__ == "__main__":
    if "--compare" in sys.argv:
        compare_prompts()
    else:
        version = sys.argv[1] if len(sys.argv) > 1 else "v2_detailed"
        run_evaluation(version)
