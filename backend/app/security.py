from fastapi import Header, HTTPException

ROLES = {"admin": 3, "manager": 2, "analyst": 1, "viewer": 0}


def require_role(required: str, role: str | None) -> None:
    if role is None or ROLES.get(role.lower(), -1) < ROLES[required]:
        raise HTTPException(status_code=403, detail=f"Requires {required} role")


def get_role(x_business_role: str | None = Header(default="viewer")) -> str:
    return x_business_role.lower()
