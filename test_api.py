import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv

# Ensure we load .env with test API key
load_dotenv()

import server as server_mod

client = TestClient(server_mod.app)

API_KEY = os.getenv("API_KEY", "change-me")

def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert "status" in r.json()

def test_add_and_list_entries():
    # create entry with API key
    headers = {"x-api-key": API_KEY}
    r = client.post("/api/meet/entries", json={"name": "Test Runner", "lane": 1, "heat": 1}, headers=headers)
    assert r.status_code == 201
    entry = r.json()
    assert "id" in entry
    # list entries
    r2 = client.get("/api/meet/entries")
    assert r2.status_code == 200
    entries = r2.json()
    assert any(e["id"] == entry["id"] for e in entries)

def test_record_event_and_results():
    headers = {"x-api-key": API_KEY}
    # add entry
    r = client.post("/api/meet/entries", json={"name": "Runner 2", "lane": 2, "heat": 1}, headers=headers)
    entry = r.json()
    # record finish
    r2 = client.post("/api/meet/event", json={"entry_id": entry["id"], "type": "finish"}, headers=headers)
    assert r2.status_code == 201
    # results
    r3 = client.get("/api/meet/results")
    assert r3.status_code == 200
    results = r3.json()
    # results may contain our entry
    assert isinstance(results, list)
