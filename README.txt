ORDER PROCESSING AND QUALITY CHECKS

Python project for order validation, checkout, persistence, authorization, and
automated testing.

PROJECT STRUCTURE
 src/: Order domain, checkout service, persistence, authorization, and business rules.
 tests/: Unit, integration, service, security, and business-rule tests.
 datos/: Sample orders and business-rule test cases.
 evidencias/capturas/: Project screenshots and coverage evidence.
 .github/workflows/ci.yml: GitHub Actions continuous integration workflow.
 verificar_laboratorio.py: Lint and test coverage checks.
 INSTRUCCIONES_AGY.md: Additional execution guide.

SETUP
 python -m venv .venv
 .\.venv\Scripts\Activate.ps1
 python -m pip install -r requirements.txt

TESTS AND CHECKS
 python -m pytest -v
 python -m ruff check src tests
 python -m pytest -v --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80

The HTML coverage report is written to htmlcov/index.html.
