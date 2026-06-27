# Sentinel Rules — Tasks API

Engineering conventions every PR must follow. Each rule has an id Sentinel cites in findings.

## rule: cascade-deletes
Our production database does **not** have `ON DELETE CASCADE`. When deleting a parent row,
you **must** delete its child rows explicitly first (e.g. delete a Task's `Reminder` rows
before deleting the Task). A bare parent delete will orphan child rows in prod.

## rule: thin-api
The API layer (`app/api.py`) must stay thin: input validation and calling the store/queue only.
No business logic and no slow/blocking calls (network, email) inside request handlers.

## rule: no-secrets-in-code
Never hardcode secrets, API keys, passwords, or tokens in source. Read them from environment
variables or a secret manager.

## rule: typed-functions
New public functions must have type hints on parameters and return values.

## rule: errors-not-swallowed
Do not catch an exception and silently pass. Either handle it meaningfully or let it propagate;
log it if you must continue.
