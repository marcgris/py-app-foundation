---
name: security-audit
description: >
    Use when auditing, reviewing, or hardening Python code for security
    vulnerabilities. Covers OWASP Top 10, injection, secrets management,
    dependency scanning, input validation, secure defaults, and CLI threat models.
  Trigger on: "security review", "audit this code", "is this secure",
    "check for vulnerabilities", "OWASP", "pentest findings", "security hardening",
    "cli security", "command injection".
---

# Security Audit Skill

This skill performs a structured security review against the OWASP Top 10 and
Python-specific vulnerability patterns. Work through each category systematically.

## Repository Alignment

For this project, include a CLI-focused review in addition to OWASP categories:

- `src/starter/cli.py` command dispatch and error handling
- `src/starter/config.py` configuration loading and validation errors
- `src/starter/logging.py` logging output and secret-safe behavior

### CLI-Specific Security Checklist

- [ ] No shell execution paths (`shell=True`) and no command injection vectors
- [ ] No secret or token leakage in stdout/stderr output
- [ ] Deterministic error messages do not expose environment internals
- [ ] `config show` output excludes secrets by design
- [ ] Logs and command output avoid sensitive values

## Audit Checklist

Run through every category below. Flag findings with severity:
- 🔴 **CRITICAL** — exploitable, fix immediately
- 🟠 **HIGH** — significant risk, fix before next release
- 🟡 **MEDIUM** — reduce attack surface, fix in current sprint
- 🟢 **LOW** — defense-in-depth improvement

---

### A01 — Broken Access Control

Check every route:
- [ ] Is authentication enforced? (`Depends(require_auth)` on every protected route)
- [ ] Is authorization checked? (Does the user own the resource they're accessing?)
- [ ] Are admin routes protected by role check, not just auth?
- [ ] Are UUIDs used for IDs (not sequential integers that enable enumeration)?

```python
# 🔴 CRITICAL: Missing ownership check
@router.get("/invoices/{id}")
async def get_invoice(id: uuid.UUID, service = Depends(get_invoice_service)):
    return await service.get_by_id(id)  # Any authenticated user can read ANY invoice

# ✅ CORRECT: Ownership enforced
@router.get("/invoices/{id}")
async def get_invoice(
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    service = Depends(get_invoice_service),
):
    invoice = await service.get_by_id(id)
    if invoice.owner_id != current_user.id:
        raise HTTPException(status_code=403)
    return invoice
```

---

### A02 — Cryptographic Failures

- [ ] Passwords hashed with `bcrypt` or `argon2` (never MD5, SHA1, or plain SHA256)
- [ ] No secrets in source code, environment variable names, or logs
- [ ] TLS enforced in production (check Nginx/load balancer config)
- [ ] JWT tokens: `HS256` minimum; prefer `RS256` for multi-service
- [ ] Sensitive data (SSN, card numbers) encrypted at rest

```python
# ✅ CORRECT password hashing
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

---

### A03 — Injection

**SQL Injection:** Never use string formatting with SQL.

```python
# 🔴 CRITICAL: SQL Injection
query = f"SELECT * FROM users WHERE email = '{email}'"
await session.execute(text(query))

# ✅ CORRECT: Parameterized
await session.execute(select(User).where(User.email == email))
```

**Command Injection:** Avoid `subprocess` with user input. If needed:

```python
import shlex, subprocess
# 🔴 CRITICAL
subprocess.run(f"convert {filename} output.png", shell=True)

# ✅ CORRECT: Never shell=True with user data
subprocess.run(["convert", filename, "output.png"], shell=False, check=True)
```

---

### A04 — Insecure Design

- [ ] Does the API expose internal IDs, stack traces, or system paths in error responses?
- [ ] Are rate limits applied to auth endpoints? (prevent brute force)
- [ ] Is there account enumeration via different error messages for bad email vs bad password?

```python
# 🟠 HIGH: Timing attack + enumeration
if not user:
    raise HTTPException(detail="Email not found")  # reveals valid emails
if not verify_password(plain, user.password_hash):
    raise HTTPException(detail="Wrong password")

# ✅ CORRECT: Constant time, no enumeration
user = await repo.get_by_email(email)
password_valid = user is not None and verify_password(plain, user.password_hash)
if not password_valid:
    raise HTTPException(status_code=401, detail="Invalid credentials")
```

---

### A05 — Security Misconfiguration

FastAPI/Starlette defaults to check:

```python
# Check CORS is not wildcard in production
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,  # NOT ["*"] in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Disable OpenAPI docs in production
app = FastAPI(
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
)
```

---

### A06 — Vulnerable Components

Run in CI:
```bash
uv run pip-audit          # checks installed packages against CVE database
uv run safety check       # alternative scanner
```

Enable GitHub Dependabot in `.github/dependabot.yml`:
```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

---

### A07 — Authentication Failures

- [ ] JWT `exp` claim set and validated
- [ ] Refresh token rotation implemented (old token invalidated on use)
- [ ] Failed login attempts logged with IP
- [ ] Account lockout after N failures

```python
# ✅ JWT validation with expiry
from jose import JWTError, jwt
from datetime import datetime, timezone

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        if datetime.fromtimestamp(payload["exp"], tz=timezone.utc) < datetime.now(tz=timezone.utc):
            raise HTTPException(status_code=401, detail="Token expired")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

---

### A08 — Software and Data Integrity

- [ ] Dependencies pinned with hashes in `uv.lock`
- [ ] Docker images use specific SHA digests, not `latest`
- [ ] CI pipeline signatures verified (GitHub Actions `pin-actions`)

---

### A09 — Logging and Monitoring Failures

- [ ] Auth failures logged with IP, user agent, timestamp
- [ ] No PII or secrets in log output
- [ ] Structured logs with correlation IDs for request tracing
- [ ] Alerts configured for unusual failure rates

```python
import structlog
log = structlog.get_logger()

# 🔴 CRITICAL: Never log secrets or passwords
log.info("login attempt", email=email, password=password)  # NEVER

# ✅ CORRECT: Log outcomes, not secrets
log.warning("login_failed", email=email, ip=request.client.host, reason="invalid_credentials")
```

---

### A10 — Server-Side Request Forgery (SSRF)

If your app makes outbound HTTP requests based on user input:

```python
import httpx
from urllib.parse import urlparse

ALLOWED_HOSTS = {"api.trusted-partner.com", "webhooks.myservice.com"}

async def fetch_webhook(url: str) -> dict:
    parsed = urlparse(url)
    if parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError(f"Disallowed host: {parsed.hostname}")
    # Also block private IP ranges
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        return response.json()
```

---

## Secrets Scanning

Install `detect-secrets` as a pre-commit hook:

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/Yelp/detect-secrets
  rev: v1.4.0
  hooks:
    - id: detect-secrets
      args: ['--baseline', '.secrets.baseline']
```

Run baseline scan: `detect-secrets scan > .secrets.baseline`

## Audit Report Template

After completing the review, produce a report with:

```
## Security Audit Report — <Module/PR>
Date: <date>
Auditor: GitHub Copilot Security Agent

### Critical Findings (fix immediately)
- [file:line] Description of vulnerability and fix

### High Findings
- ...

### Summary
- X critical, Y high, Z medium findings
- Recommended action: <block PR / fix before release / add to backlog>
```
