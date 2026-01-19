#!/usr/bin/env python3
"""
Test script for validating local model configurations (Ollama and LMStudio).

Usage:
    python test_local_models.py --ollama              # Test Ollama
    python test_local_models.py --lmstudio            # Test LMStudio
    python test_local_models.py --all                 # Test all
    python test_local_models.py --ollama --lmstudio   # Test both
"""

import os
import json
import time
import httpx
import argparse
import asyncio
import sys
from dotenv import load_dotenv

load_dotenv()

PROXY_URL = "http://localhost:8082/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
API_KEY = "test-key"

headers = {
    "x-api-key": API_KEY,
    "anthropic-version": ANTHROPIC_VERSION,
    "content-type": "application/json",
}


def test_local_server(url, server_name):
    """Test if a local server is reachable."""
    print(f"\n{'=' * 20} Testing {server_name} at {url} {'=' * 20}")

    try:
        if server_name == "Ollama":
            response = httpx.get(f"{url}/api/tags", timeout=5, trust_env=False)
        else:
            response = httpx.get(f"{url}/v1/models", timeout=5, trust_env=False)

        if response.status_code == 200:
            models = response.json()
            print(f"✅ {server_name} is reachable!")
            if server_name == "Ollama" and "models" in models:
                model_names = [m.get("name", "unknown") for m in models["models"]]
            elif "data" in models:
                model_names = [m.get("id", "unknown") for m in models["data"]]
            else:
                model_names = []
            print(f"   Available models: {', '.join(model_names[:5])}")
            return True
        else:
            print(f"❌ {server_name} returned status {response.status_code}")
            return False
    except httpx.RequestError as e:
        print(f"❌ Cannot connect to {server_name}: {e}")
        return False


async def test_proxy_with_local_model(model_name, provider_name):
    """Test the proxy with a local model."""
    print(f"\n{'=' * 20} Testing Proxy with {provider_name} ({model_name}) {'=' * 20}")

    request_data = {
        "model": model_name,
        "max_tokens": 100,
        "messages": [
            {
                "role": "user",
                "content": "Say 'Hello from {provider_name}' in one sentence.",
            }
        ],
    }

    try:
        start_time = time.time()
        async with httpx.AsyncClient(trust_env=False) as client:
            response = await client.post(
                PROXY_URL, headers=headers, json=request_data, timeout=120
            )
        elapsed = time.time() - start_time

        if response.status_code == 200:
            result = response.json()
            print(f"✅ {provider_name} test passed! ({elapsed:.2f}s)")

            content = result.get("content", [])
            if content and isinstance(content, list):
                text_block = content[0] if isinstance(content[0], dict) else {}
                text = text_block.get("text", "")
                print(f"   Response: {text[:100]}...")
            return True
        else:
            print(f"❌ {provider_name} test failed: {response.status_code}")
            try:
                error = response.json()
                print(f"   Error: {json.dumps(error, indent=2)}")
            except:
                print(f"   Raw error: {response.text[:200]}")
            return False

    except Exception as e:
        print(f"❌ {provider_name} test error: {e}")
        return False


async def run_tests(args):
    """Run the local model tests."""
    results = {}

    ollama_url = os.environ.get("OPENAI_BASE_URL", "http://localhost:11434/v1")

    if ollama_url.endswith("/v1"):
        base_url = ollama_url[:-3]
    else:
        base_url = ollama_url

    if args.ollama or args.all:
        server_ok = test_local_server(base_url, "Ollama")
        results["ollama_server"] = server_ok

        if server_ok:
            model = os.environ.get("BIG_MODEL", "openai/qwen3-coder")
            results["ollama_proxy"] = await test_proxy_with_local_model(model, "Ollama")

    if args.lmstudio or args.all:
        lmstudio_url = "http://localhost:11435"
        server_ok = test_local_server(lmstudio_url, "LMStudio")
        results["lmstudio_server"] = server_ok

        if server_ok:
            model = os.environ.get("BIG_MODEL", "openai/qwen/qwen3-8b")
            results["lmstudio_proxy"] = await test_proxy_with_local_model(
                model, "LMStudio"
            )

    if args.ollama and args.lmstudio:
        both_ok = results.get("ollama_proxy") and results.get("lmstudio_proxy")
        results["all_tests"] = both_ok

    print("\n" + "=" * 20 + " SUMMARY " + "=" * 20)
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test}: {status}")

    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")

    return passed == total


def main():
    parser = argparse.ArgumentParser(
        description="Test local model configurations for the proxy"
    )
    parser.add_argument("--ollama", action="store_true", help="Test Ollama")
    parser.add_argument("--lmstudio", action="store_true", help="Test LMStudio")
    parser.add_argument("--all", action="store_true", help="Test all local models")

    args = parser.parse_args()

    if not any([args.ollama, args.lmstudio, args.all]):
        parser.print_help()
        print("\nExamples:")
        print("  python test_local_models.py --ollama")
        print("  python test_local_models.py --lmstudio")
        print("  python test_local_models.py --all")
        return

    success = asyncio.run(run_tests(args))
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
