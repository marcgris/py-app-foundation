---
name: pydantic-models
description: >
  Use when designing, reviewing, or improving Pydantic v2 data models for
  FastAPI applications. Covers model hierarchy, field validation, custom
  validators, serialization, settings management, and model composition patterns.
  Trigger on: "create a model", "add validation", "Pydantic schema", "request body",
  "response model", "settings class", "validate this field", "model for".
---

# Pydantic Models Skill

Pydantic v2 is the type system and validation layer for the entire application.
Use it everywhere: API contracts, domain entities, configuration, and events.

## Model Hierarchy Pattern

Every resource has a family of models with a clear purpose:

```
<Resource>Base          ← shared validated fields
├── <Resource>Create    ← input for POST (no id/timestamps)
├── <Resource>Update    ← input for PATCH (all fields Optional)
├── <Resource>InDB      ← internal representation (includes hashed_password etc.)
└── <Resource>Response  ← output to clients (excludes sensitive fields)
```

## Canonical Model Structure

```python
from __future__ import annotations
import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
    computed_field,
)


class ProductBase(BaseModel):
    """Shared, validated fields for the Product resource."""
    name: str = Field(..., min_length=1, max_length=255, description="Product display name")
    price: Decimal = Field(..., gt=0, decimal_places=2, description="Price in USD")
    sku: str = Field(..., pattern=r"^[A-Z]{3}-\d{6}$", description="SKU in format ABC-123456")
    tags: list[str] = Field(default_factory=list, max_length=10)


class ProductCreate(ProductBase):
    """Input for POST /products. Validated on arrival."""
    category_id: uuid.UUID


class ProductUpdate(BaseModel):
    """Input for PATCH /products/{id}. All fields optional."""
    name: str | None = Field(None, min_length=1, max_length=255)
    price: Decimal | None = Field(None, gt=0, decimal_places=2)
    sku: str | None = Field(None, pattern=r"^[A-Z]{3}-\d{6}$")
    tags: list[str] | None = None


class ProductResponse(ProductBase):
    """Output model — safe to return to any client."""
    model_config = ConfigDict(from_attributes=True)  # enables .model_validate(orm_obj)

    id: uuid.UUID
    category_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ProductInDB(ProductResponse):
    """Internal model with fields not exposed to clients."""
    internal_cost: Decimal | None = None
    supplier_id: uuid.UUID | None = None
```

## Field Validators

```python
from pydantic import field_validator

class UserCreate(BaseModel):
    email: str
    password: str
    username: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain an uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain a digit")
        return v

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        import re
        if not re.match(r"^[a-zA-Z0-9_-]{3,30}$", v):
            raise ValueError("Username must be 3–30 alphanumeric characters, hyphens, or underscores")
        return v
```

## Model Validators (cross-field validation)

```python
from pydantic import model_validator

class DateRangeFilter(BaseModel):
    start_date: datetime
    end_date: datetime

    @model_validator(mode="after")
    def validate_date_range(self) -> DateRangeFilter:
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        if (self.end_date - self.start_date).days > 365:
            raise ValueError("Date range cannot exceed 365 days")
        return self
```

## Computed Fields

```python
from pydantic import computed_field

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    subtotal: Decimal
    tax_rate: Decimal
    discount: Decimal = Decimal("0")

    @computed_field  # included in serialization automatically
    @property
    def total(self) -> Decimal:
        return (self.subtotal * (1 + self.tax_rate)) - self.discount

    @computed_field
    @property
    def display_total(self) -> str:
        return f"${self.total:.2f}"
```

## Settings Management with pydantic-settings

```python
# src/config.py
from functools import lru_cache
from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "My App"
    debug: bool = False
    allowed_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    # Database
    database_url: PostgresDsn
    db_pool_size: int = Field(default=10, ge=1, le=50)

    # Auth
    secret_key: str = Field(..., min_length=32)
    access_token_expire_minutes: int = Field(default=30, ge=1)

    # External APIs
    sendgrid_api_key: str | None = None

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        if v == "change-me" or v == "secret":
            raise ValueError("Use a real secret key in production")
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

## Nested Models & Relationships

```python
class AddressModel(BaseModel):
    street: str
    city: str
    country: str = Field(..., min_length=2, max_length=2)  # ISO code
    postal_code: str

class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    billing_address: AddressModel
    shipping_addresses: list[AddressModel] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
```

## Serialization Control

```python
from pydantic import Field

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    hashed_password: str = Field(exclude=True)   # never serialized
    created_at: datetime = Field(serialization_alias="createdAt")  # camelCase output

# Serialize to dict
user.model_dump()
user.model_dump(mode="json")           # JSON-safe types (UUIDs as strings)
user.model_dump(exclude_unset=True)    # only fields explicitly set (great for PATCH)
user.model_dump(exclude_none=True)     # exclude None values
user.model_dump(by_alias=True)         # use serialization_alias names
```

## Pagination Models

```python
from typing import Generic, TypeVar
T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    skip: int
    limit: int

    @computed_field
    @property
    def has_more(self) -> bool:
        return self.skip + self.limit < self.total

# Usage in route
@router.get("/users/", response_model=PaginatedResponse[UserResponse])
```

## Common Mistakes to Avoid

- ❌ Using `Optional[X]` instead of `X | None` (use the modern syntax)
- ❌ Not setting `model_config = ConfigDict(from_attributes=True)` on response models
- ❌ Mutating models after creation (use `model_copy(update={...})` instead)
- ❌ Using `dict()` instead of `model_dump()` (deprecated in v2)
- ❌ Missing `@classmethod` on `@field_validator` methods
- ❌ Using `default=[]` instead of `default_factory=list` (shared mutable default)
