# 🔒 EPP Detector

Detector de Equipos de Protección Personal (EPP) usando [LM Studio](https://lmstudio.ai/).

Analiza imágenes de personas en entornos de trabajo para detectar objetos de seguridad industrial como:
- Casco de seguridad
- Gafas/lentes de protección
- Chaleco reflectante
- Guantes de seguridad
- Botas de seguridad
- Arnés de seguridad
- Protección auditiva
- Respirador/máscara

## Requisitos

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) (manejador de paquetes)
- [LM Studio](https://lmstudio.ai/) ejecutándose con un modelo VLM (Vision-Language Model)

## Instalación

1. **Clonar o descargar el proyecto**

2. **Instalar dependencias con uv:**
   ```bash
   cd epp-detector
   uv sync
   ```

3. **Asegurar que LM Studio esté corriendo:**
   - Abre LM Studio
   - Carga un modelo compatible con visión (VLM), como:
     - `qwen2-vl-2b-instruct`
     - `llava-v1.5-7b`
     - `fuyu-8b`
   - Asegúrate de que el servidor esté activo (por defecto en `localhost:1234`)

## Uso

### Uso básico

```bash
python epp_detector.py -i ruta/a/imagen.jpg
```

### Opciones disponibles

```
Opciones:
  -h, --help            Mostrar mensaje de ayuda y salir
  -i, --image PATH      Ruta a la imagen a analizar (requerido)
  --host HOST           Host donde corre LM Studio (default: localhost)
  --port PORT           Puerto donde corre LM Studio (default: 1234)
  -m, --model MODEL     Modelo a usar (default: el modelo cargado)
  --timeout SECONDS     Timeout en segundos (default: 60)
  --json-only           Mostrar solo la respuesta JSON sin formato
```

### Ejemplos

```bash
# Analizar imagen local
python epp_detector.py -i worker.jpg

# Conectar a LM Studio en otra máquina
python epp_detector.py -i worker.jpg --host 192.168.1.100 --port 8080

# Especificar modelo
python epp_detector.py -i worker.jpg --model qwen2-vl-2b-instruct

# Obtener solo JSON (para scripts/automatización)
python epp_detector.py -i worker.jpg --json-only
```

## Modelo de Respuesta

La aplicación devuelve un JSON con el siguiente formato:

```json
{
  "analisis": "breve descripción de lo que se observa en la imagen",
  "epp_detectados": [
    {"nombre": "nombre del EPP", "estado": "presente|ausente", "observaciones": "notas adicionales"}
  ],
  "recomendaciones": ["lista de recomendaciones si faltan EPP"],
  "cumple_normativa": true/false
}
```

## Descargar un Modelo VLM con LM Studio

Si no tienes un modelo compatible con visión, puedes descargar uno usando el CLI de LM Studio:

```bash
# Ejemplos de modelos VLM disponibles
lms get qwen2-vl-2b-instruct
lms get llava-v1.5-7b
lms get fuyu-8b
```

## Solución de Problemas

### Error: "No se pudo conectar a LM Studio"

- Verifica que LM Studio esté ejecutándose
- Verifica que el servidor esté activo en el puerto correcto (default: 1234)
- Si LM Studio está en otra máquina, verifica el firewall y la conectividad de red

### Error: "El modelo no soporta visión"

- Asegúrate de haber cargado un modelo VLM (Vision-Language Model)
- Verifica que el modelo sea compatible con análisis de imágenes

### Error: "La imagen no existe"

- Verifica que la ruta a la imagen sea correcta
- Usa rutas absolutas si hay problemas con rutas relativas

## Dependencias

- `lmstudio>=1.5.0` - SDK oficial de LM Studio para Python
- `pillow>=12.3.0` - Manejo de imágenes

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Recursos

- [LM Studio](https://lmstudio.ai/) - Sitio oficial
- [Documentación del SDK Python](https://lmstudio.ai/docs/python)
- [Documentación de entrada de imágenes](https://lmstudio.ai/docs/python/llm-prediction/image-input)

## Ejemplos

```bash
uv run epp_detector.py -i .\imagenes\sincasco1.jpg
uv run epp_detector.py -i .\imagenes\casco1.jpg
```
  