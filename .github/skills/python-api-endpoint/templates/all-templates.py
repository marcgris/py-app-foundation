# ============================================================
# templates/models-template.py
# Replace <Resource> with your entity name (e.g., User, Product)
# ============================================================
from __future__ import annotations
import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class <Resource>Base(BaseModel):
    """Shared fields for <Resource> models."""
    name: str = Field(..., min_length=1, max_length=255)
    # Add shared fields here


class <Resource>Create(<Resource>Base):
    """Input model for creating a <Resource>."""
    pass  # Add create-only fields here


class <Resource>Update(BaseModel):
    """Input model for partially updating a <Resource>. All fields optional."""
    name: str | None = Field(None, min_length=1, max_length=255)
    # Mirror <Resource>Base fields but all Optional


class <Resource>Response(<Resource>Base):
    """Output model returned to clients."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# ============================================================
# templates/repository-template.py
# ============================================================
from __future__ import annotations
import uuid
from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import <Resource>ORM
from src.models.<resource> import <Resource>Create, <Resource>Update


class Abstract<Resource>Repository(ABC):
    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> <Resource>ORM | None: ...

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[<Resource>ORM]: ...

    @abstractmethod
    async def create(self, data: <Resource>Create) -> <Resource>ORM: ...

    @abstractmethod
    async def update(self, id: uuid.UUID, data: <Resource>Update) -> <Resource>ORM | None: ...

    @abstractmethod
    async def delete(self, id: uuid.UUID) -> bool: ...


class SQLAlchemy<Resource>Repository(Abstract<Resource>Repository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, id: uuid.UUID) -> <Resource>ORM | None:
        return await self._session.get(<Resource>ORM, id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[<Resource>ORM]:
        result = await self._session.execute(
            select(<Resource>ORM).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def create(self, data: <Resource>Create) -> <Resource>ORM:
        obj = <Resource>ORM(**data.model_dump())
        self._session.add(obj)
        await self._session.commit()
        await self._session.refresh(obj)
        return obj

    async def update(self, id: uuid.UUID, data: <Resource>Update) -> <Resource>ORM | None:
        obj = await self.get_by_id(id)
        if obj is None:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        await self._session.commit()
        await self._session.refresh(obj)
        return obj

    async def delete(self, id: uuid.UUID) -> bool:
        obj = await self.get_by_id(id)
        if obj is None:
            return False
        await self._session.delete(obj)
        await self._session.commit()
        return True


# ============================================================
# templates/service-template.py
# ============================================================
from __future__ import annotations
import uuid
from src.repositories.<resource> import Abstract<Resource>Repository
from src.models.<resource> import <Resource>Create, <Resource>Response, <Resource>Update
from src.exceptions import <Resource>NotFoundError


class <Resource>Service:
    def __init__(self, repo: Abstract<Resource>Repository) -> None:
        self._repo = repo

    async def get_by_id(self, id: uuid.UUID) -> <Resource>Response:
        obj = await self._repo.get_by_id(id)
        if obj is None:
            raise <Resource>NotFoundError(id)
        return <Resource>Response.model_validate(obj)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[<Resource>Response]:
        objs = await self._repo.get_all(skip=skip, limit=limit)
        return [<Resource>Response.model_validate(o) for o in objs]

    async def create(self, data: <Resource>Create) -> <Resource>Response:
        obj = await self._repo.create(data)
        return <Resource>Response.model_validate(obj)

    async def update(self, id: uuid.UUID, data: <Resource>Update) -> <Resource>Response:
        obj = await self._repo.update(id, data)
        if obj is None:
            raise <Resource>NotFoundError(id)
        return <Resource>Response.model_validate(obj)

    async def delete(self, id: uuid.UUID) -> None:
        deleted = await self._repo.delete(id)
        if not deleted:
            raise <Resource>NotFoundError(id)


# ============================================================
# templates/router-template.py
# ============================================================
from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends, status
from src.services.<resource>_service import <Resource>Service
from src.models.<resource> import <Resource>Create, <Resource>Response, <Resource>Update
from src.dependencies import get_<resource>_service

router = APIRouter(prefix="/<resources>", tags=["<Resources>"])


@router.get("/", response_model=list[<Resource>Response])
async def list_<resources>(
    skip: int = 0,
    limit: int = 100,
    service: <Resource>Service = Depends(get_<resource>_service),
) -> list[<Resource>Response]:
    return await service.get_all(skip=skip, limit=limit)


@router.get("/{id}", response_model=<Resource>Response)
async def get_<resource>(
    id: uuid.UUID,
    service: <Resource>Service = Depends(get_<resource>_service),
) -> <Resource>Response:
    return await service.get_by_id(id)


@router.post("/", response_model=<Resource>Response, status_code=status.HTTP_201_CREATED)
async def create_<resource>(
    data: <Resource>Create,
    service: <Resource>Service = Depends(get_<resource>_service),
) -> <Resource>Response:
    return await service.create(data)


@router.patch("/{id}", response_model=<Resource>Response)
async def update_<resource>(
    id: uuid.UUID,
    data: <Resource>Update,
    service: <Resource>Service = Depends(get_<resource>_service),
) -> <Resource>Response:
    return await service.update(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_<resource>(
    id: uuid.UUID,
    service: <Resource>Service = Depends(get_<resource>_service),
) -> None:
    await service.delete(id)


# ============================================================
# templates/test-template.py
# ============================================================
from __future__ import annotations
import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.repositories.<resource> import Abstract<Resource>Repository
from src.models.<resource> import <Resource>Create, <Resource>Update
from src.dependencies import get_<resource>_service
from src.services.<resource>_service import <Resource>Service


class InMemory<Resource>Repository(Abstract<Resource>Repository):
    """In-memory implementation for tests — no DB required."""

    def __init__(self) -> None:
        self._store: dict[uuid.UUID, dict] = {}

    async def get_by_id(self, id: uuid.UUID):
        return self._store.get(id)

    async def get_all(self, skip: int = 0, limit: int = 100):
        return list(self._store.values())[skip : skip + limit]

    async def create(self, data: <Resource>Create):
        obj = {"id": uuid.uuid4(), **data.model_dump()}
        self._store[obj["id"]] = obj
        return obj

    async def update(self, id: uuid.UUID, data: <Resource>Update):
        if id not in self._store:
            return None
        self._store[id].update(data.model_dump(exclude_unset=True))
        return self._store[id]

    async def delete(self, id: uuid.UUID) -> bool:
        return self._store.pop(id, None) is not None


@pytest.fixture
def repo() -> InMemory<Resource>Repository:
    return InMemory<Resource>Repository()


@pytest.fixture
async def client(repo: InMemory<Resource>Repository) -> AsyncClient:
    def override():
        return <Resource>Service(repo)

    app.dependency_overrides[get_<resource>_service] = override
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
    app.dependency_overrides.clear()


async def test_create_<resource>(client: AsyncClient) -> None:
    response = await client.post("/<resources>/", json={"name": "Test"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test"
    assert "id" in data


async def test_get_<resource>(client: AsyncClient) -> None:
    created = (await client.post("/<resources>/", json={"name": "Test"})).json()
    response = await client.get(f"/<resources>/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


async def test_get_<resource>_not_found(client: AsyncClient) -> None:
    response = await client.get(f"/<resources>/{uuid.uuid4()}")
    assert response.status_code == 404


async def test_update_<resource>(client: AsyncClient) -> None:
    created = (await client.post("/<resources>/", json={"name": "Old"})).json()
    response = await client.patch(f"/<resources>/{created['id']}", json={"name": "New"})
    assert response.status_code == 200
    assert response.json()["name"] == "New"


async def test_delete_<resource>(client: AsyncClient) -> None:
    created = (await client.post("/<resources>/", json={"name": "Test"})).json()
    response = await client.delete(f"/<resources>/{created['id']}")
    assert response.status_code == 204
    get_response = await client.get(f"/<resources>/{created['id']}")
    assert get_response.status_code == 404
