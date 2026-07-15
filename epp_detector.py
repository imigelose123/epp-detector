#!/usr/bin/env python3
"""
EPP Detector - Detector de Equipos de Protección Personal usando LM Studio.

Analiza imágenes de personas para detectar objetos de seguridad industrial como:
- Casco de seguridad
- Gafas de protección
- Chaleco reflectante
- Guantes
- Botas de seguridad
- Arnés de seguridad
- Protección auditiva
- Respirador/máscara
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

import lmstudio as lms


# Prompt del sistema para detección de EPP
SYSTEM_PROMPT = """Eres un experto en seguridad industrial y Equipos de Protección Personal (EPP).

Tu tarea es analizar imágenes de personas en entornos de trabajo y detectar qué EPP están utilizando.

Analiza la imagen y responde en el siguiente formato JSON (solo el JSON, sin texto adicional):

{
  "analisis": "breve descripción de lo que se observa en la imagen",
  "epp_detectados": [
    {"nombre": "nombre del EPP", "estado": "presente|ausente", "observaciones": "notas adicionales"}
  ],
  "recomendaciones": ["lista de recomendaciones si faltan EPP"],
  "cumple_normativa": true/false
}

EPP a detectar:
- Casco de seguridad
- Gafas/lentes de protección
- Chaleco reflectante
- Guantes de seguridad
- Botas de seguridad
- Arnés de seguridad (para trabajos en altura)
- Protección auditiva (orejeras/tapones)
- Respirador/máscara (cuando aplique)

Sé específico y preciso en tu análisis."""


def parse_arguments() -> argparse.Namespace:
    """Parsea los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Detector de EPP usando LM Studio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python epp_detector.py -i worker.jpg
  python epp_detector.py -i worker.jpg --host 192.168.1.100 --port 8080
  python epp_detector.py -i worker.jpg --model qwen2-vl-2b-instruct
        """
    )

    parser.add_argument(
        "-i", "--image",
        type=str,
        required=True,
        help="Ruta a la imagen a analizar"
    )

    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Host donde corre LM Studio (default: localhost)"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=1234,
        help="Puerto donde corre LM Studio (default: 1234)"
    )

    parser.add_argument(
        "-m", "--model",
        type=str,
        default=None,
        help="Modelo a usar (default: el modelo cargado en LM Studio)"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Timeout en segundos para la respuesta del modelo (default: 60)"
    )

    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Mostrar solo la respuesta JSON sin formato adicional"
    )

    return parser.parse_args()


def validate_image(image_path: str) -> Path:
    """Valida que la imagen exista y sea accesible."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"La imagen no existe: {image_path}")
    if not path.is_file():
        raise ValueError(f"La ruta no es un archivo: {image_path}")
    return path


def print_banner():
    """Imprime el banner de la aplicación."""
    print("=" * 60)
    print("  EPP DETECTOR - Detector de Equipos de Proteccion Personal")
    print("=" * 60)
    print()


def print_results(analysis: str, json_only: bool = False):
    """Imprime los resultados del análisis formateados."""
    if json_only:
        print(analysis)
        return

    print("\n" + "=" * 60)
    print("  RESULTADOS DEL ANÁLISIS")
    print("=" * 60)
    print()
    print(analysis)
    print()
    print("=" * 60)


def main():
    """Función principal de la aplicación."""
    args = parse_arguments()

    try:
        # Validar imagen primero
        image_path = validate_image(args.image)

        if not args.json_only:
            print_banner()
            print(f"[+] Imagen: {args.image}")
            print(f"[+] Conectando a LM Studio en {args.host}:{args.port}")
            if args.model:
                print(f"[+] Modelo: {args.model}")
            print()

        # Configurar timeout
        lms.set_sync_api_timeout(args.timeout)

        # Preparar la imagen
        if not args.json_only:
            print("[*] Preparando imagen...")
        image_handle = lms.prepare_image(str(image_path))

        # Obtener el modelo
        if not args.json_only:
            print("[*] Cargando modelo...")
        model = lms.llm(args.model) if args.model else lms.llm()

        # Crear el chat con el mensaje del sistema
        chat = lms.Chat(SYSTEM_PROMPT)
        chat.add_user_message(
            "Analiza esta imagen y detecta los equipos de protección personal "
            "que la persona está utilizando. Responde en el formato JSON especificado.",
            images=[image_handle]
        )

        # Obtener la predicción
        if not args.json_only:
            print("[*] Analizando imagen...")
            print()
        prediction = model.respond(chat)

        # Mostrar resultados
        print_results(prediction, args.json_only)

    except FileNotFoundError as e:
        print(f"[!] Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"[!] Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error inesperado: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
