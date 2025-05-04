import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_store():
    from app.models import notes_store
    notes_store.clear()

def create_note(title="Title", content="Content", due_date=None):
    note = {"title": title, "content": content}
    if due_date:
        note["due_date"] = due_date
    return client.post("/notes/", json=note)

class TestHappyPaths:
    def test_create_and_get(self):
        r = create_note()
        assert r.status_code == 201
        data = r.json()
        assert data["id"] == 1
        assert data["title"] == "Title"
        r2 = client.get(f"/notes/{data['id']}")
        assert r2.status_code == 200

    def test_list_notes(self):
        create_note(title="A")
        create_note(title="B")
        r = client.get("/notes/")
        assert r.status_code == 200
        arr = r.json()
        assert len(arr) == 2
        titles = {n['title'] for n in arr}
        assert titles == {"A", "B"}

    def test_update_put(self):
        r = create_note()
        note_id = r.json()["id"]
        r2 = client.put(f"/notes/{note_id}", json={"title":"New","content":"NewC"})
        assert r2.status_code == 200
        updated = r2.json()
        assert updated["title"] == "New"

    def test_update_patch(self):
        r = create_note()
        note_id = r.json()["id"]
        r2 = client.patch(f"/notes/{note_id}", json={"content":"Patched"})
        assert r2.status_code == 200
        assert r2.json()["content"] == "Patched"

    def test_delete_and_head(self):
        r = create_note()
        note_id = r.json()["id"]
        r2 = client.delete(f"/notes/{note_id}")
        assert r2.status_code == 204
        r3 = client.head(f"/notes/{note_id}")
        assert r3.status_code == 404

class TestNegativePaths:
    @pytest.mark.parametrize("payload,code", [
        ({}, 422),
        ({"title": ""}, 422),
        ({"title": "A"*101}, 422),
        ({"title": "Valid", "content": "C"*1001}, 422),
        ({"title": "Valid", "due_date": "2000-01-01"}, 422),
    ])
    def test_create_validation_errors(self, payload, code):
        r = client.post("/notes/", json=payload)
        assert r.status_code == code

    def test_get_nonexistent(self):
        r = client.get("/notes/999")
        assert r.status_code == 404

    def test_put_nonexistent(self):
        r = client.put("/notes/999", json={"title":"T","content":"C"})
        assert r.status_code == 404

    def test_patch_nonexistent(self):
        r = client.patch("/notes/999", json={"content":"C"})
        assert r.status_code == 404

    def test_delete_nonexistent(self):
        r = client.delete("/notes/999")
        assert r.status_code == 404

class TestEquivalenceAndBoundaries:
    @pytest.mark.parametrize("title", ["A", "ABCD", "Z"*100])
    def test_title_valid_equivalence(self, title):
        r = create_note(title=title)
        assert r.status_code == 201

    @pytest.mark.parametrize("content", [None, "", "X"*1000])
    def test_content_valid_equivalence(self, content):
        payload = {"title": "T"}
        if content is not None:
            payload["content"] = content
        r = client.post("/notes/", json=payload)
        assert r.status_code == 201

    @pytest.mark.parametrize("due_date", [None, "2025-12-31",])
    def test_due_date_future(self, due_date):
        r = create_note(due_date=due_date)
        assert r.status_code == 201

    def test_due_date_today(self):
        from datetime import date
        today = date.today().isoformat()
        r = create_note(due_date=today)
        assert r.status_code == 201

class TestOptions:
    def test_options(self):
        r = client.options("/notes/")
        assert r.status_code == 200
        allow = r.headers.get("Allow")
        assert all(m in allow for m in ["GET","POST","PUT","PATCH","DELETE","HEAD","OPTIONS"])

    def test_options(self):
        r = client.options("/notes/")
        assert r.status_code == 200
        allow = r.headers.get("Allow")
        assert all(m in allow for m in ["GET","POST","PUT","PATCH","DELETE","HEAD","OPTIONS"])
