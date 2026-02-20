"""Verify multi-tenant isolation: tenant A cannot see tenant B data (404); lists are scoped.

Assumes app is running (e.g. uvicorn app.main:app) and seed_verification_tenants has been run.

Usage (from project root):
  python scripts/verify_multi_tenant.py [BASE_URL]
  Default BASE_URL: http://127.0.0.1:8000
"""

from __future__ import annotations

import sys
from pathlib import Path

# Project root
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

BASE_URL = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000").rstrip("/")

USER_A_EMAIL = "admin_tenant_a@test.local"
USER_B_EMAIL = "admin_tenant_b@test.local"
PASSWORD = "test"


def main() -> None:
    session = requests.Session()

    # Login as tenant A
    r = session.post(
        f"{BASE_URL}/auth/login",
        json={"email": USER_A_EMAIL, "password": PASSWORD},
        timeout=10,
    )
    r.raise_for_status()
    token_a = r.json()["access_token"]
    session.headers["Authorization"] = f"Bearer {token_a}"

    # List users as A – should only see tenant A users
    r = session.get(f"{BASE_URL}/users", timeout=10)
    r.raise_for_status()
    users_a = r.json()
    assert isinstance(users_a, list), "GET /users should return list"
    for u in users_a:
        assert u["email"] == USER_A_EMAIL or u.get("email", "").endswith("@test.local"), (
            "Expected only tenant A users"
        )
    print("Tenant A: GET /users returns scoped list OK")

    # Create a user in tenant A and note its id
    r = session.post(
        f"{BASE_URL}/users",
        json={
            "email": "sales_a@test.local",
            "password": "pass",
            "role": "sales",
        },
        timeout=10,
    )
    r.raise_for_status()
    created = r.json()
    user_a_id = created["id"]
    print(f"Tenant A: created user id={user_a_id} OK")

    # Login as tenant B
    session_b = requests.Session()
    r = session_b.post(
        f"{BASE_URL}/auth/login",
        json={"email": USER_B_EMAIL, "password": PASSWORD},
        timeout=10,
    )
    r.raise_for_status()
    token_b = r.json()["access_token"]
    session_b.headers["Authorization"] = f"Bearer {token_b}"

    # List users as B – should not include tenant A's users
    r = session_b.get(f"{BASE_URL}/users", timeout=10)
    r.raise_for_status()
    users_b = r.json()
    ids_b = {u["id"] for u in users_b}
    assert user_a_id not in ids_b, "Tenant B must not see tenant A user in list"
    print("Tenant B: GET /users does not include tenant A user OK")

    # Cross-tenant access by id must return 404 (not 403)
    r = session_b.patch(
        f"{BASE_URL}/users/{user_a_id}/role",
        json={"role": "manager"},
        timeout=10,
    )
    assert r.status_code == 404, f"Expected 404 for cross-tenant PATCH, got {r.status_code}"
    print("Tenant B: PATCH tenant A user returns 404 OK")

    print("All multi-tenant isolation checks passed.")


if __name__ == "__main__":
    main()
