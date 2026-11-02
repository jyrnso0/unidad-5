# Order Processing and Quality Checks

Python project for order validation, checkout, persistence, authorization, and
automated testing.

## Project structure

- `src/domain.py`: order validation, discounts, and state transitions.
- `src/application.py`: checkout service and payment gateway coordination.
- `src/repository.py`: SQLAlchemy order persistence.
- `src/security.py`: order cancellation authorization rules.
- `src/pia_domain.py`: inventory, quantity, and volume-discount rules.
- `tests/`: unit, integration, service, security, and business-rule tests.
- `datos/`: sample orders and business-rule test cases.
- `evidencias/capturas/`: project screenshots and coverage evidence.
- `.github/workflows/ci.yml`: GitHub Actions continuous integration workflow.
- `verificar_laboratorio.py`: runs lint and test coverage checks.
- `INSTRUCCIONES_AGY.md`: additional execution guide.

## Setup

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run tests and checks

```powershell
python -m pytest -v
python -m ruff check src tests
python -m pytest -v --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80
```

The HTML coverage report is written to `htmlcov/index.html`.
