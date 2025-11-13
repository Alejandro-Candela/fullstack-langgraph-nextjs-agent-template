"""Script para probar los endpoints del backend."""

import requests
import json

BASE_URL = "http://localhost:8000"

print("🧪 Probando endpoints del backend...\n")

# 1. Health check
print("1. Health check:")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print()

# 2. Root endpoint
print("2. Root endpoint:")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print()

# 3. List MCP servers
print("3. List MCP servers:")
try:
    response = requests.get(f"{BASE_URL}/api/mcp-servers")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Response: {json.dumps(data, indent=2)}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print()

# 4. List MCP tools
print("4. List MCP tools:")
try:
    response = requests.get(f"{BASE_URL}/api/mcp-servers/tools")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Response: {json.dumps(data, indent=2)}")
    else:
        print(f"   Error response: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print()

# 5. API docs
print("5. API Documentation available at:")
print(f"   Swagger UI: {BASE_URL}/docs")
print(f"   ReDoc: {BASE_URL}/redoc")

