# Codebase Concerns

## Technical Debt & Issues
1. **Secrets in Environment**: Hardcoded or placeholder secrets like `SECRET_KEY` exist in the `.env` file (`replace-with-a-strong-secret`). These need rotation for production.
2. **Environment Variable Parsing Risks**: `CORS_ORIGINS` parsing is strict and fails application startup if not specifically formatted as a JSON array string.
3. **IDE Type Checker Configuration**: Persistent type checking warnings required `.pyre_configuration` and `pyrightconfig.json` adjustments with workspace root pointers and inline `# pyre-ignore[21]` suppressions.

## Fragile Areas
- **Database Connection Strings**: Managing both async Postgres and MongoDB connections simultaneously requires careful connection pooling handling under production load.
