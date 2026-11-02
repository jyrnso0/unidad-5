"""
Script Utilitario de Autodiagnostico y Verificacion Integral (verificar_laboratorio.py)
Ejecuta la suite completa de pruebas, verifica estilo con Ruff y calcula cobertura de codigo.
Compatible con consolas Windows (cp1252 / utf-8).
"""
import subprocess
import sys


def run_step(title, command):
    print("\n" + "=" * 60)
    print(f"[*] {title}")
    print(f"    Comando: {' '.join(command)}")
    print("=" * 60)
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
    return result.returncode == 0


def main():
    print("Iniciando Verificacion Integral de Unidad 5 - Calidad y Pruebas...")
    success = True

    # 1. Comprobar linter Ruff
    ruff_ok = run_step(
        "Paso 1: Verificacion de Estilo y Calidad con Ruff",
        [sys.executable, "-m", "ruff", "check", "src", "tests"]
    )
    if not ruff_ok:
        print("[!] Advertencia: Ruff detecto problemas de estilo o no esta instalado.")
        success = False

    # 2. Ejecutar Pytest con Cobertura
    cov_cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-v",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-fail-under=80"
    ]
    pytest_ok = run_step(
        "Paso 2: Ejecucion de Pruebas Automatizadas y Cobertura (>=80%)",
        cov_cmd
    )
    if not pytest_ok:
        print("[X] Error: Algunas pruebas fallaron o la cobertura no alcanzo el 80%.")
        success = False

    print("\n" + "#" * 60)
    if success:
        print("[OK] TODAS LAS VERIFICACIONES COMPLETADAS EXITOSAMENTE!")
        print("El proyecto cumple con los estandares de calidad y cobertura.")
    else:
        print("[X] SE DETECTARON OBSERVACIONES. Revisa los detalles anteriores.")
    print("#" * 60)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
