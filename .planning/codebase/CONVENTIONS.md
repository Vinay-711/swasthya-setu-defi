# Conventions Map

## Formatting & Typing
- **Type Hinting**: Extensive use of Python type hinting. 
- **Type Suppression**: Use of `# pyre-ignore[21]` inside `models/health_record.py` to suppress false positive IDE import errors.

## Data Validation
- **Pydantic Validation**: All environment variables and request/response models use Pydantic.
  - _Note_: `CORS_ORIGINS` expects a valid JSON string array representation (e.g., `'["http://localhost:3000"]'`) rather than a comma-separated list.

## Async Best Practices
- **Async DB Sessions**: The application uses `AsyncSession` from SQLAlchemy. Interactions with PostgreSQL and MongoDB are primarily asynchronous.
