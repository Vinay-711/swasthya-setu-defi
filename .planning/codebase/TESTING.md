# Testing Map

## Framework
- **Pytest**: The primary test runner for the backend (`pytest backend/tests/ -v`).

## Test Structure
- **Fixtures**: Located in `backend/tests/conftest.py`. Provides async event loops, test database sessions, and mocked dependencies.
- **Coverage**: The test suite covers AI models (`test_ai_models.py`), endpoints, and mock services.

## Current State
- **Execution**: Tests run successfully via `source .venv/bin/activate && pytest backend/tests/ -v`.
- **Status**: 100% pass rate currently (8/8 tests passed).
