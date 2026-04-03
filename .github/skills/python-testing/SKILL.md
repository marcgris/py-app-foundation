---
name: python-testing
description: >
  Use when writing, reviewing, improving, or generating pytest test suites for
  Python and FastAPI applications. Covers unit tests, integration tests, async
  tests, fixture design, mocking strategy, parametrize patterns, and coverage gaps.
  Trigger on: "write tests", "add tests", "test this", "improve test coverage",
  "generate test suite", "what should I test", "my test is failing".
---

# Python Testing Skill

This skill produces **meaningful tests** — tests that catch real bugs, not
tests that just hit coverage numbers. Every test must assert actual behavior.

## Testing Philosophy

- **Test behavior, not implementation** — test what a function does, not how
- **Arrange–Act–Assert** — every test has exactly three phases, clearly separated
- **One concept per test** — if a test name needs "and", split it
- **Tests are documentation** — a failing test should tell you exactly what broke

## Test Layers — What Goes Where

| Layer | Location | Tools | Speed | What it tests |
|---|---|---|---|---|
| Unit | `tests/unit/` | Pure pytest | < 1ms | Pure functions, domain logic |
| Integration | `tests/integration/` | pytest + real DB (docker) | < 1s | Service + repo + DB together |
| E2E | `tests/e2e/` | httpx AsyncClient | < 5s | Full HTTP request/response cycle |

**Rule:** Mock at the repository boundary. Never mock the database — use a real
test database (via `pytest-docker`) or an in-memory repository for integration tests.

## Fixture Design Patterns

See `templates/conftest-template.py` for the canonical conftest.

### Fixture Hierarchy
```
session-scoped: database engine, docker containers
  ↓ function-scoped (default):
    db_session: transaction that rolls back after each test
      ↓ derived:
        user_repo, product_repo (receive the session)
          ↓ derived:
            client: httpx AsyncClient with overridden dependencies
```

### Fixture Rules
- Use `scope="session"` only for expensive setup (Docker containers, engine creation)
- Use function-scoped sessions that roll back — never commit in tests
- Use `pytest.fixture` factories for creating test data with sensible defaults

## Writing Unit Tests

For pure functions and domain logic:

```python
# tests/unit/test_pricing.py
import pytest
from src.core.pricing import calculate_discount


class TestCalculateDiscount:
    def test_returns_zero_for_no_items(self) -> None:
        assert calculate_discount(items=[], loyalty_years=0) == 0.0

    def test_applies_10_percent_for_loyal_customers(self) -> None:
        result = calculate_discount(items=[100.0], loyalty_years=3)
        assert result == pytest.approx(10.0)

    @pytest.mark.parametrize("years,expected", [
        (0, 0.0),
        (1, 0.05),
        (3, 0.10),
        (10, 0.15),
    ])
    def test_discount_tiers(self, years: int, expected: float) -> None:
        result = calculate_discount(items=[100.0], loyalty_years=years)
        assert result == pytest.approx(expected * 100)

    def test_raises_for_negative_price(self) -> None:
        with pytest.raises(ValueError, match="negative"):
            calculate_discount(items=[-1.0], loyalty_years=0)
```

## Writing Async Integration Tests

```python
# tests/integration/test_user_service.py
import pytest
from src.services.user_service import UserService
from src.models.user import UserCreate
from src.exceptions import UserNotFoundError
from tests.fakes import InMemoryUserRepository


@pytest.fixture
def service() -> UserService:
    return UserService(repo=InMemoryUserRepository())


async def test_create_user_returns_response_model(service: UserService) -> None:
    # Arrange
    data = UserCreate(email="alice@example.com", name="Alice")

    # Act
    result = await service.create(data)

    # Assert
    assert result.email == "alice@example.com"
    assert result.id is not None


async def test_get_nonexistent_user_raises_not_found(service: UserService) -> None:
    import uuid
    with pytest.raises(UserNotFoundError):
        await service.get_by_id(uuid.uuid4())
```

## Parametrize Patterns

Use `@pytest.mark.parametrize` for data-driven cases:

```python
@pytest.mark.parametrize("email", [
    "not-an-email",
    "@missing-local.com",
    "missing-at-sign.com",
    "",
])
async def test_rejects_invalid_emails(client: AsyncClient, email: str) -> None:
    response = await client.post("/users/", json={"email": email, "name": "Test"})
    assert response.status_code == 422
```

## Mocking — When and How

**Only mock external I/O you don't control**: email sending, payment APIs,
external HTTP calls, time. Never mock your own repositories or services.

```python
from unittest.mock import AsyncMock, patch

async def test_sends_welcome_email_on_registration(
    service: UserService,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_send = AsyncMock()
    monkeypatch.setattr("src.services.user_service.send_email", mock_send)

    await service.create(UserCreate(email="bob@example.com", name="Bob"))

    mock_send.assert_called_once()
    call_kwargs = mock_send.call_args.kwargs
    assert call_kwargs["to"] == "bob@example.com"
    assert "welcome" in call_kwargs["subject"].lower()
```

## Coverage — What to Measure

Run: `pytest --cov=src --cov-report=term-missing --cov-fail-under=80`

**Focus coverage on:**
- All service methods (happy path + not-found + validation error)
- All route handlers (2xx + 4xx + 5xx)
- All domain exception paths

**Don't chase 100%** — untestable code (main entrypoints, config loading) is
fine to exclude in `pyproject.toml`:

```toml
[tool.coverage.run]
omit = ["src/main.py", "src/config.py", "src/db/migrations/*"]
```

## Test Naming Conventions

Follow the pattern: `test_<what>_<condition>_<expected>`

```
test_create_user_with_valid_data_returns_201        ✓
test_get_user_when_not_found_returns_404            ✓
test_update_product_with_negative_price_raises      ✓
test_api()                                          ✗  — too vague
test_works()                                        ✗  — meaningless
```

## Common Anti-Patterns to Avoid

- ❌ Testing the mock itself (`assert mock.called` without asserting side effects)
- ❌ Tests that only test that no exception was raised
- ❌ `assert response.status_code == 200` with no further assertions
- ❌ Hardcoding IDs that work only in insertion order
- ❌ Tests that depend on each other's execution order
- ❌ `time.sleep()` in tests — use `freezegun` for time-dependent logic
