from app.api import deps
from fastapi.testclient import TestClient


def test_directives(client: TestClient, raw_entries):
    response = client.get("/directive")

    assert response.json() == raw_entries


def test_directive(client: TestClient, raw_entries):
    for v in deps.DirectiveType:
        expected = [e for e in raw_entries if e["ty"] == v.value.capitalize()]
        response = client.get(f"/directive/{v.value}")

        assert response.json() == expected


def test_directive_id(client: TestClient, raw_entries):
    for entry in raw_entries:
        response = client.get(f"/directive/id/{entry['id']}")
        assert response.json() == entry


def test_directive_syntax(
    client: TestClient, syntax: dict[str, tuple[dict, str]]
):
    for v in syntax.values():
        response = client.post("/directive/syntax", json=v[0])
        assert response.text == v[1]
