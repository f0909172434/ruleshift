from fastapi.testclient import TestClient

from ruleshift.api import app

client = TestClient(app)


def test_workbench_full_stream_and_replay():
    r = client.post("/api/world", json={"seed": 17, "schedule": "recurring"})
    assert r.status_code == 200
    sid = r.json()["session_id"]
    assert r.json()["mode"] == "researcher_not_agent_input"
    assert client.post(f"/api/world/{sid}/next").status_code == 409
    for i in range(8):
        done = client.post(f"/api/world/{sid}/reference")
        assert done.json()["score"]["success"]
        assert done.json()["execution_kind"] == "privileged_reference_not_llm"
        if i < 7:
            assert client.post(f"/api/world/{sid}/next").status_code == 200
    assert client.post(f"/api/world/{sid}/next").status_code == 409
    assert client.get(f"/api/world/{sid}/replay").json()["verified"]


def test_schema_and_unknown_sessions():
    assert client.post("/api/world", json={"schedule": "anything"}).status_code == 422
    assert client.get("/api/world/unknown").status_code == 404
    assert client.get("/api/not-a-route").status_code == 404
    assert client.post("/api/world", json={"seed": -1}).status_code == 422
