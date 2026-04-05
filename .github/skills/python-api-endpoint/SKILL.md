---
name: python-api-endpoint
description: >
  Use when creating, extending, or restructuring FastAPI endpoints. Covers the
  full vertical slice: Pydantic request/response models, route handler, service
  method, repository method, dependency wiring, and pytest integration test stub.
  Trigger on: "add endpoint", "new route", "create API for", "add a GET/POST/PUT/DELETE",
  "build a resource", "add CRUD for".
---

# Python API Endpoint Skill

This skill implements a **complete vertical slice** for a new FastAPI endpoint,
following Clean Architecture principles. Every layer is created together so
nothing is left unwired.

## Architecture Rules (enforce these always)

1. **Routes are thin** — route handlers do nothing except call a service and return a response model
2. **Services own business logic** — orchestrate repositories, apply rules, raise domain exceptions
3. **Repositories abstract data** — only place SQLAlchemy/async DB calls live
4. **Models are the contract** — all input/output passes through Pydantic models
5. **Dependencies are injected** — never instantiate services or repos inside handlers

## Step-by-Step Execution

### Step 1 — Define the Pydantic Models (`src/models/<resource>.py`)

See `templates/all-templates.md` (models section) for the canonical pattern.
Templates are intentionally consolidated in this single file; there are no
separate `templates/models-template.py` or sibling files.

- Create a `<Resource>Base` with shared fields
- Create a `<Resource>Create` (input, no `id`)
- Create a `<Resource>Update` (all fields optional, for PATCH)
- Create a `<Resource>Response` (output, includes `id`, timestamps)
- Use `model_config = ConfigDict(from_attributes=True)` on response models

### Step 2 — Define the Repository Interface (`src/repositories/<resource>.py`)

See `templates/all-templates.md` (repository section) for the canonical pattern.

- Define an `Abstract<Resource>Repository(ABC)` with typed method signatures
- Implement `SQLAlchemy<Resource>Repository` that inherits the abstract class
- Methods: `get_by_id`, `get_all`, `create`, `update`, `delete`
- All methods are `async`; use `AsyncSession`

### Step 3 — Implement the Service (`src/services/<resource>_service.py`)

See `templates/all-templates.md` (service section) for the canonical pattern.

- Constructor receives the abstract repository (not the concrete one)
- Raise `<Resource>NotFoundError` (a domain exception) when entity is missing
- Never return SQLAlchemy models directly — convert to response models

### Step 4 — Create the Router (`src/api/routes/<resource>.py`)

See `templates/all-templates.md` (router section) for the canonical pattern.

- Use `APIRouter(prefix="/<resources>", tags=["<Resources>"])`
- Each route returns the correct Pydantic response model
- Use `Depends()` for service injection
- Set appropriate HTTP status codes (201 for create, 204 for delete)

### Step 5 — Register the Router (`src/api/main.py` or `src/main.py`)

```python
from src.api.routes.users import router as users_router
app.include_router(users_router)
```

### Step 6 — Write the Integration Test (`tests/integration/test_<resource>_routes.py`)

See `templates/all-templates.md` (test section) for the canonical pattern.

- Use `httpx.AsyncClient` with `ASGITransport`
- Override the repository dependency with an in-memory implementation
- Test: create, read one, read all, update, delete, and not-found cases

## File Checklist

Before finishing, confirm these files exist and are wired:

- [ ] `src/models/<resource>.py` — Pydantic models
- [ ] `src/repositories/<resource>.py` — abstract + SQLAlchemy implementation
- [ ] `src/services/<resource>_service.py` — business logic
- [ ] `src/api/routes/<resource>.py` — FastAPI router
- [ ] `src/api/main.py` — router registered
- [ ] `tests/integration/test_<resource>_routes.py` — integration tests
- [ ] `src/exceptions.py` — domain exception added

## Domain Exceptions Pattern

Always add a typed exception to `src/exceptions.py`:

```python
class UserNotFoundError(Exception):
    def __init__(self, user_id: uuid.UUID) -> None:
        super().__init__(f"User {user_id} not found")
        self.user_id = user_id
```

Register the exception handler in `main.py`:

```python
@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})
```
