---
name: python-refactor
description: >
  Use when refactoring, improving, or restructuring existing Python code. Covers
  Clean Architecture migration, extracting services/repositories, applying design
  patterns (Strategy, Factory, Observer, Repository), eliminating code smells,
  improving type safety, and reducing coupling. Trigger on: "refactor this",
  "this code is messy", "extract this into a service", "apply the repository pattern",
  "reduce coupling", "this function is too long", "god class", "clean this up".
---

# Python Refactor Skill

Refactoring is about **improving structure without changing behavior**. Always
have tests before refactoring. Always run tests after each step.

## The Refactoring Process

1. **Understand** — read the code fully before touching it. Ask Copilot to explain it if needed.
2. **Test** — ensure existing tests pass. If there are no tests, write characterization tests first.
3. **Identify smells** — use the catalog below
4. **Plan** — choose the smallest refactor that addresses the worst smell
5. **Execute** — one smell at a time; run tests after each change
6. **Verify** — confirm tests still pass; check types with mypy

## Code Smell Catalog & Fixes

### 🔴 God Class / God Function
**Symptom:** A class with 10+ methods doing unrelated things; a function > 50 lines.
**Fix:** Extract class or extract function.

```python
# Before: UserManager does too much
class UserManager:
    def create_user(self): ...
    def send_welcome_email(self): ...      # → EmailService
    def calculate_loyalty_discount(self): ...  # → PricingService
    def generate_report(self): ...         # → ReportService

# After: Single Responsibility
class UserService:
    def __init__(self, repo, email_svc, pricing_svc): ...
    def create_user(self, data) -> User: ...
```

### 🔴 Framework Leak into Domain
**Symptom:** FastAPI, SQLAlchemy, or HTTP concepts appear inside business logic.
**Fix:** Extract domain logic into a pure function or domain service with no imports from `fastapi` or `sqlalchemy`.

```python
# Before: FastAPI leaking into business logic
from fastapi import HTTPException
def apply_discount(user_id: int, amount: float) -> float:
    if amount < 0:
        raise HTTPException(status_code=400, detail="negative amount")

# After: Domain exception, no framework dependency
class NegativeAmountError(ValueError): ...
def apply_discount(user_id: int, amount: float) -> float:
    if amount < 0:
        raise NegativeAmountError(amount)
```

### 🔴 Direct Database Access in Service or Route
**Symptom:** `db.query(User).filter(...)` appears outside a repository class.
**Fix:** Move to repository, expose via abstract interface.

### 🟡 Long Parameter List (> 4 params)
**Symptom:** `def create_order(user_id, product_id, qty, price, discount, coupon, ...)`
**Fix:** Introduce a Pydantic parameter object.

```python
class OrderCreateParams(BaseModel):
    user_id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    price: Decimal
    discount_code: str | None = None

def create_order(params: OrderCreateParams) -> Order: ...
```

### 🟡 Primitive Obsession
**Symptom:** `user_id: int`, `email: str`, `price: float` everywhere.
**Fix:** Use typed Pydantic models or NewType.

```python
from typing import NewType
UserId = NewType("UserId", uuid.UUID)
Email = NewType("Email", str)
```

### 🟡 Duplicate Logic
**Symptom:** Same validation, transformation, or query appears in multiple places.
**Fix:** Extract to a shared function, validator, or base class.

### 🟢 Magic Numbers/Strings
**Symptom:** `if status == "active"` or `if retries > 3`
**Fix:** Use enums and named constants.

```python
from enum import StrEnum
class UserStatus(StrEnum):
    ACTIVE = "active"
    SUSPENDED = "suspended"

MAX_RETRIES: int = 3
```

## Applying Design Patterns

### Strategy Pattern — Swap algorithms at runtime
Use when you have multiple implementations of the same operation:

```python
from abc import ABC, abstractmethod

class NotificationStrategy(ABC):
    @abstractmethod
    async def send(self, message: str, recipient: str) -> None: ...

class EmailNotification(NotificationStrategy):
    async def send(self, message: str, recipient: str) -> None: ...

class SlackNotification(NotificationStrategy):
    async def send(self, message: str, recipient: str) -> None: ...

class NotificationService:
    def __init__(self, strategy: NotificationStrategy) -> None:
        self._strategy = strategy

    async def notify(self, message: str, recipient: str) -> None:
        await self._strategy.send(message, recipient)
```

### Factory Pattern — Centralize object creation
Use when construction logic is complex or varies by condition:

```python
class RepositoryFactory:
    @staticmethod
    def create_user_repo(session: AsyncSession) -> AbstractUserRepository:
        return SQLAlchemyUserRepository(session)

    @staticmethod
    def create_in_memory_user_repo() -> AbstractUserRepository:
        return InMemoryUserRepository()
```

### Observer Pattern — Decouple side effects
Use when an action triggers multiple independent reactions:

```python
from typing import Callable, Awaitable

class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable]] = {}

    def subscribe(self, event: str, handler: Callable) -> None:
        self._handlers.setdefault(event, []).append(handler)

    async def publish(self, event: str, **kwargs) -> None:
        for handler in self._handlers.get(event, []):
            await handler(**kwargs)

# Usage
bus = EventBus()
bus.subscribe("user.created", send_welcome_email)
bus.subscribe("user.created", provision_default_settings)
```

## Improving Type Safety

Run `mypy --strict src/` and fix errors in this priority order:

1. Add return type annotations to all public functions
2. Replace `Any` with concrete types or `TypeVar`
3. Add `| None` to optional parameters instead of using `Optional[X]`
4. Use `TypedDict` for dict-shaped data until you can convert to Pydantic
5. Add `# type: ignore[<code>]` only as a last resort, always with a comment

## Refactor Checklist

Before declaring a refactor done:
- [ ] `pytest` — all tests pass
- [ ] `mypy --strict src/` — no new errors introduced
- [ ] `ruff check src/` — no new lint violations
- [ ] No `Any` types added
- [ ] No framework imports in `src/core/` or `src/services/`
- [ ] Each class has a single, clear responsibility
- [ ] All new code has corresponding tests
