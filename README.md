# FitCore AI Nutrition API

API REST construida con **FastAPI** y **Gemini Vision** que analiza imágenes de comida y devuelve información nutricional detallada: calorías, macros (proteínas, carbohidratos, grasas) y desglose por ingrediente.

---

## Estructura del proyecto

```
fitcore-api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   └── meals.py       # Rutas del recurso /meals
│   │       └── router.py          # Router central de la v1
│   ├── core/
│   │   └── config.py              # Configuración con pydantic-settings
│   ├── schemas/
│   │   └── nutrition.py           # Modelos Pydantic de request/response
│   ├── services/
│   │   └── gemini_service.py      # Lógica de comunicación con Gemini
│   └── main.py                    # Factory de la aplicación FastAPI
├── docs/
│   └── db_schema.md               # Esquema de la base de datos (Mermaid + Diccionario)
├── .env.example                   # Plantilla de variables de entorno
├── .gitignore
├── requirements.txt
└── README.md
```

## Documentación del Esquema de Datos
Puedes consultar la estructura relacional detallada, los tipos de datos y los enums del proyecto en [docs/db_schema.md](docs/db_schema.md).

---

## Instalación y uso

### 1. Clonar y crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Edita .env y coloca tu GEMINI_API_KEY real
```

### 4. Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

La documentación interactiva estará disponible en `http://localhost:8000/docs`.

---

## Endpoint principal

### `POST /api/v1/meals/analyze`

Recibe una imagen y devuelve el análisis nutricional.

**Body:** `multipart/form-data`
- `file` — Imagen del platillo (JPEG, PNG, WEBP, etc.)

**Response 200:**
```json
{
  "success": true,
  "error": null,
  "food_name": "Tacos de canasta",
  "estimated_total_weight_g": 350,
  "total_calories": 620,
  "total_protein_g": 22,
  "total_carbs_g": 78,
  "total_fat_g": 24,
  "ingredients": [
    {
      "name": "Tortilla de maíz",
      "estimated_weight_g": 90,
      "calories": 210,
      "protein_g": 5,
      "carbs_g": 42,
      "fat_g": 3
    }
  ]
}
```
