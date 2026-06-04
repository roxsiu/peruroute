
# PeruRoute AI

**Pipeline Generativo Multimodal para Turismo Personalizado**

> Diploma AI Engineer · Módulo: Ingeniería de Aplicaciones Generativas

---

## ¿Qué es PeruRoute AI?

PeruRoute AI es un pipeline generativo multimodal que combina dos modelos de IA fine-tuned para producir, a partir del perfil de un turista, un **itinerario personalizado** y una **imagen del destino** con identidad de marca.

```
Perfil del turista
       ↓
 LLM fine-tuned (Qwen2.5-3B + LoRA)
       ↓
 Itinerario día a día
       ↓
 Modelo de difusión (SD 1.5 + DreamBooth LoRA)
       ↓
 Imagen del destino
```

---

## Arquitectura

| Módulo | Modelo | Técnica | Dataset |
|--------|--------|---------|---------|
| Generación de texto | Qwen2.5-3B-Instruct | LoRA 16-bit (r=16) via Unsloth | 800 perfiles sintéticos (formato Alpaca) |
| Generación de imagen | Stable Diffusion 1.5 | DreamBooth LoRA (rank=16) | 12 variaciones del logo PeruRoute AI |

---

## Estructura del repositorio

```
peruroute-ai/
├── README.md
├── requirements.txt
├── peruroute.ipynb
├── dataset/
│   └── dataset_turismo_peru.csv
├── logos/
│   ├── 01_logo_fondo_oscuro.png
│   └── ... (12 variaciones)
├── src/
│   ├── generate_dataset.py
│   └── generate_logos.py

```

---

## Instalación y ejecución

### Requisitos previos

- Cuenta Kaggle con GPU T4 x2 activada
- Token HuggingFace → [Crear token](https://huggingface.co/settings/tokens)

### Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/peruroute-ai.git
```

### Paso 2 — Subir datasets a Kaggle

Crea estos datasets en Kaggle:

- `peruroute-dataset` → sube `dataset/dataset_turismo_peru.csv`
- `peruroute-logos` → sube todos los PNGs de `logos/`

### Paso 3 — Configurar token HuggingFace

En Kaggle: **Add-ons → Secrets → Agregar `HF_TOKEN`**

### Paso 4 — Ejecutar el notebook

Abre `peruroute.ipynb` en Kaggle y ejecuta las celdas secuencialmente.

### Tiempo estimado en GPU T4

| Sección | Tiempo |
|---------|--------|
| Instalación | ~10 min |
| Fine-tuning LLM | ~30 min |
| Fine-tuning imagen | ~15 min |
| Pipeline integrado | ~5 min |
| **Total** | **~60 min** |

---

## Dataset

El archivo `dataset/dataset_turismo_peru.csv` contiene **800 ejemplos sintéticos** en formato Alpaca.

| Columna | Descripción |
|---------|-------------|
| `dias_viaje` | Duración del viaje (3, 5, 7, 10, 14 días) |
| `presupuesto` | Nivel económico (bajo, medio, alto, lujo) |
| `intereses` | Tipo de experiencia (cultura, aventura, etc.) |
| `origen_turista` | País de origen |
| `destino_principal` | Destino ancla del viaje |
| `instruction` | Instrucción Alpaca (fija) |
| `input` | Perfil concatenado en texto |
| `output` | Itinerario completo generado |

---

## Logo y variaciones

El logo usa la **chacana** (cruz andina) con paleta verde andino `#2D6A4F` y dorado inca `#D4A017`.

| Archivo | Descripción |
|---------|-------------|
| `01_logo_fondo_oscuro.png` | Logo sobre fondo verde oscuro |
| `02_logo_fondo_claro.png` | Logo sobre fondo verde claro |
| `03_logo_fondo_negro.png` | Logo sobre fondo negro |
| `04_logo_fondo_dorado.png` | Logo sobre fondo dorado |
| `05_logo_fondo_azul.png` | Logo sobre fondo azul marino |
| `06_logo_fondo_rojo.png` | Logo sobre fondo rojo |
| `07_logo_invertido_horizontal.png` | Logo en espejo horizontal |
| `08_solo_icono_fondo_oscuro.png` | Solo el ícono (sin texto) |
| `09_solo_icono_fondo_claro.png` | Solo el ícono sobre fondo claro |
| `10_escala_grises.png` | Logo en escala de grises |
| `11_logo_fondo_crema.png` | Logo sobre fondo crema |
| `12_logo_fondo_verde_medio.png` | Logo sobre verde medio |

---

## Tecnologías

- [Unsloth](https://github.com/unslothai/unsloth) — Fine-tuning acelerado de LLMs
- [HuggingFace Transformers](https://huggingface.co/docs/transformers)
- [Diffusers](https://huggingface.co/docs/diffusers) — Pipeline de generación de imágenes
- [TRL](https://huggingface.co/docs/trl) — SFTTrainer
- [PEFT](https://huggingface.co/docs/peft) — Adaptadores LoRA
- Kaggle Notebooks — GPU T4 x2

---

## Nota técnica

Por limitaciones de VRAM en GPU T4 (14.6 GB) se usa **Stable Diffusion 1.5** en lugar de SDXL, y **LoRA 16-bit** en lugar de QLoRA 4-bit. Con una GPU A100 y SDXL los resultados de imagen serían significativamente mejores.

---

## Autor

Proyecto desarrollado como entrega final del **Diploma AI Engineer**
Módulo: Ingeniería de Aplicaciones Generativas
