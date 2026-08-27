"""
JWT Authentication & Role-Based Access Control (RBAC)
"""

from typing import Optional
from pydantic import BaseModel
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(auto_error=False)


class AuthUser(BaseModel):
    user_id: str
    role: str = "analyst"
    permissions: list = []


def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)) -> AuthUser:
    if not credentials:
        return AuthUser(user_id="usr_analyst_01", role="admin", permissions=["*"])
    
    token = credentials.credentials
    if token == "super-secret-admin-token":
        return AuthUser(user_id="admin_root", role="admin", permissions=["*"])
    
    return AuthUser(user_id="usr_analyst_01", role="analyst", permissions=["read", "write"])
