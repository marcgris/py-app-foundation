---
name: docstring-generation
description: >
  Use when writing, reviewing, or generating docstrings, module documentation,
  or API documentation for Python code. Covers Google-style docstrings, module
  headers, class documentation, exception documentation, and MkDocs integration.
  Trigger on: "write docstrings", "document this", "add docs", "generate documentation",
  "document this function", "add type docs", "missing docstrings".
---

# Docstring Generation Skill

Documentation is read far more often than it's written. Every public function,
class, and module deserves a docstring that answers: *what does it do, what does
it need, what does it return, and what can go wrong?*

## Standard: Google Style

Use Google-style docstrings consistently. They render correctly in MkDocs,
mkdocstrings, and Sphinx.

## Function/Method Docstring Template

```python
async def create_user(
    data: UserCreate,
    *,
    send_welcome_email: bool = True,
) -> UserResponse:
    """Create a new user account and optionally send a welcome email.

    Validates the input, persists the user to the database, and triggers
    the onboarding email workflow. Raises if the email is already registered.

    Args:
        data: Validated user creation payload containing email, name, and
            optional preferences. Email is normalized to lowercase before
            persistence.
        send_welcome_email: When True (default), triggers an async welcome
            email to the new user's address after successful creation.

    Returns:
        The newly created user as a response model, including the generated
        UUID and server-assigned timestamps.

    Raises:
        DuplicateEmailError: If the email address is already associated with
            an existing account.
        EmailDeliveryError: If ``send_welcome_email`` is True and the email
            service is unavailable. The user is still created successfully.

    Example:
        >>> service = UserService(repo=InMemoryUserRepository())
        >>> user = await service.create_user(
        ...     UserCreate(email="alice@example.com", name="Alice"),
        ...     send_welcome_email=False,
        ... )
        >>> print(user.email)
        alice@example.com
    """
```

## Class Docstring Template

```python
class UserService:
    """Orchestrates user lifecycle operations.

    Acts as the primary boundary between the HTTP layer and the data
    persistence layer. All business rules regarding user accounts are
    enforced here, not in routes or repositories.

    Attributes:
        MAX_LOGIN_ATTEMPTS: Class-level constant defining lockout threshold.

    Note:
        This service is stateless between requests. The repository
        dependency is injected per-request via FastAPI's ``Depends()``.

    Example:
        >>> repo = InMemoryUserRepository()
        >>> service = UserService(repo=repo, email_svc=MockEmailService())
        >>> user = await service.create_user(UserCreate(email="a@b.com", name="A"))
    """

    MAX_LOGIN_ATTEMPTS: int = 5

    def __init__(
        self,
        repo: AbstractUserRepository,
        email_svc: AbstractEmailService,
    ) -> None:
        """Initialize the service with required dependencies.

        Args:
            repo: Repository for user persistence. Can be SQLAlchemy or
                in-memory for testing.
            email_svc: Email delivery service. Injected to allow mocking
                in tests without real SMTP.
        """
        self._repo = repo
        self._email_svc = email_svc
```

## Module Docstring Template

Every `__init__.py` and every non-trivial module file should start with:

```python
"""User management domain services.

This module contains the business logic for user account operations,
including creation, authentication, profile management, and account
suspension. It is framework-agnostic — no FastAPI or SQLAlchemy imports.

Typical Usage:
    from src.services.user_service import UserService
    from src.repositories.user import InMemoryUserRepository

    service = UserService(repo=InMemoryUserRepository())
    user = await service.create_user(data)

Exported Classes:
    UserService: Primary orchestration class for user operations.

Exported Exceptions:
    DuplicateEmailError: Raised when email is already registered.
    UserNotFoundError: Raised when user ID does not exist.
"""
```

## Exception Docstring Template

```python
class DuplicateEmailError(Exception):
    """Raised when attempting to register an email that already exists.

    Args:
        email: The email address that caused the conflict.

    Attributes:
        email: The conflicting email address.

    Example:
        >>> raise DuplicateEmailError("alice@example.com")
        DuplicateEmailError: Email 'alice@example.com' is already registered.
    """

    def __init__(self, email: str) -> None:
        super().__init__(f"Email '{email}' is already registered.")
        self.email = email
```

## What to Document vs. What to Skip

**Always document:**
- All public functions and methods
- All public classes
- All raised exceptions
- Non-obvious parameters (especially boolean flags)
- Return values that aren't obvious from the type annotation

**Skip docstrings for:**
- Private methods (`_method`) where the name is self-explanatory
- Simple properties that restate the type annotation
- `__init__` if the class docstring already covers construction
- Test functions (test names serve as documentation)

**Document with inline comments (not docstrings):**
- Non-obvious algorithm steps
- Magic numbers and why they exist
- Workarounds for external library bugs

```python
# Stripe requires amounts in cents, not dollars
amount_in_cents = int(amount * 100)
```

## Generating with Copilot

Prompt patterns for Copilot to generate docstrings:

- *"Write a Google-style docstring for this function including all Args, Returns, Raises, and an Example"*
- *"Add module-level docstrings to all files in src/services/ following the pattern in src/services/user_service.py"*
- *"Review the docstrings in this file and flag any that are missing the Raises section"*

## MkDocs Integration

If using MkDocs with mkdocstrings, add to `docs/api.md`:

```markdown
# API Reference

## User Service

::: src.services.user_service.UserService
    options:
      show_source: true
      heading_level: 3
```

And in `mkdocs.yml`:

```yaml
plugins:
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: google
            show_signature_annotations: true
            separate_signature: true
```

## Docstring Quality Review Checklist

- [ ] Every public function has a docstring
- [ ] All parameters documented (especially non-obvious ones)
- [ ] Return type described when not obvious from annotation
- [ ] All raised exceptions listed in `Raises:` section
- [ ] At least one `Example:` for complex functions
- [ ] No docstrings that just restate the function name
- [ ] Module-level docstring explains the module's purpose and main exports
