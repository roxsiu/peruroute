"""
generate_logos.py
-----------------
Genera las 12 variaciones del logo PeruRoute AI como archivos PNG.

Uso:
    pip install cairosvg Pillow
    python src/generate_logos.py

Salida:
    logos/01_logo_fondo_oscuro.png
    logos/02_logo_fondo_claro.png
    ... (12 archivos)
"""

import os
import cairosvg

OUTPUT_DIR = "logos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Paleta ────────────────────────────────────────────────────
VERDE_OSC  = "#1A3A2A"
VERDE_MED  = "#2D6A4F"
DORADO     = "#D4A017"
BLANCO     = "#FFFFFF"
GRIS_CLARO = "#F0F4F1"


def logo_svg(bg_circle, stroke_cruz, fill_escalon,
             fill_texto1, fill_texto2, fill_ai, fill_linea,
             bg_outer=None, flip=False, only_icon=False):
    """Genera el SVG del logo con los parámetros de color dados."""
    W, H   = 600, 400
    cx, cy = 190, 200
    r      = 150

    transform  = f'scale(-1,1) translate(-{W},0)' if flip else ''
    outer_bg   = f'<rect width="{W}" height="{H}" fill="{bg_outer}"/>' if bg_outer else ''

    if only_icon:
        text_part = ""
        view      = "0 0 400 400"
        W         = 400
    else:
        text_part = f"""
        <text x="365" y="175" font-family="Georgia,serif"
              font-size="58" font-weight="700" fill="{fill_texto1}"
              letter-spacing="-1">Peru</text>
        <text x="365" y="238" font-family="Georgia,serif"
              font-size="58" font-weight="700" fill="{fill_texto2}"
              letter-spacing="-1">Route</text>
        <rect x="365" y="250" width="220" height="4" rx="2" fill="{fill_linea}"/>
        <text x="365" y="290" font-family="Arial,sans-serif"
              font-size="28" fill="{fill_ai}" letter-spacing="10">AI</text>
        """
        view = f"0 0 {W} {H}"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="{view}">
    {outer_bg}
    <g transform="{transform}">
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg_circle}"/>
      <rect x="{cx-48}" y="{cy-74}" width="96"  height="148" rx="4" fill="{stroke_cruz}"/>
      <rect x="{cx-74}" y="{cy-48}" width="148" height="96"  rx="4" fill="{stroke_cruz}"/>
      <rect x="{cx-30}" y="{cy-74}" width="60" height="22" rx="2" fill="{fill_escalon}"/>
      <rect x="{cx-30}" y="{cy+52}" width="60" height="22" rx="2" fill="{fill_escalon}"/>
      <rect x="{cx-74}" y="{cy-30}" width="22" height="60" rx="2" fill="{fill_escalon}"/>
      <rect x="{cx+52}" y="{cy-30}" width="22" height="60" rx="2" fill="{fill_escalon}"/>
      <polygon points="{cx},{cy-28} {cx+26},{cy} {cx},{cy+28} {cx-26},{cy}"
               fill="{fill_escalon}"/>
      <circle cx="{cx}" cy="{cy}" r="9" fill="{BLANCO}"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none"
              stroke="{fill_escalon}" stroke-width="3"/>
      <rect x="{cx-52}" y="{cy-115}" width="8" height="8" rx="1"
            fill="{fill_escalon}" opacity="0.6"/>
      <rect x="{cx+44}" y="{cy-115}" width="8" height="8" rx="1"
            fill="{fill_escalon}" opacity="0.6"/>
      <rect x="{cx-52}" y="{cy+107}" width="8" height="8" rx="1"
            fill="{fill_escalon}" opacity="0.6"/>
      <rect x="{cx+44}" y="{cy+107}" width="8" height="8" rx="1"
            fill="{fill_escalon}" opacity="0.6"/>
    </g>
    {text_part}
    </svg>"""


VARIACIONES = [
    ("01_logo_fondo_oscuro",
     dict(bg_circle=VERDE_OSC, stroke_cruz=VERDE_MED, fill_escalon=DORADO,
          fill_texto1=VERDE_OSC, fill_texto2=VERDE_MED, fill_ai=DORADO,
          fill_linea=DORADO, bg_outer=BLANCO)),
    ("02_logo_fondo_claro",
     dict(bg_circle=GRIS_CLARO, stroke_cruz=VERDE_MED, fill_escalon=DORADO,
          fill_texto1=VERDE_OSC, fill_texto2=VERDE_MED, fill_ai=DORADO,
          fill_linea=DORADO, bg_outer=BLANCO)),
    ("03_logo_fondo_negro",
     dict(bg_circle=VERDE_OSC, stroke_cruz=VERDE_MED, fill_escalon=DORADO,
          fill_texto1=VERDE_MED, fill_texto2=DORADO, fill_ai=BLANCO,
          fill_linea=DORADO, bg_outer="#111111")),
    ("04_logo_fondo_dorado",
     dict(bg_circle=VERDE_OSC, stroke_cruz=VERDE_MED, fill_escalon=DORADO,
          fill_texto1=VERDE_OSC, fill_texto2=VERDE_MED, fill_ai=VERDE_OSC,
          fill_linea=VERDE_OSC, bg_outer=DORADO)),
    ("05_logo_fondo_azul",
     dict(bg_circle=VERDE_OSC, stroke_cruz=VERDE_MED, fill_escalon=DORADO,
          fill_texto1=BLANCO, fill_texto2=DORADO, fill_ai=BLANCO,
          fill_linea=DORADO, bg_outer="#1B3A6B")),
    ("06_logo_fondo_rojo",
     dict(bg_circle=VERDE_OSC, stroke_cruz=VERDE_MED, fill_escalon=DORADO,
          fill_texto1=BLANCO, fill_texto2=DORADO, fill_ai=BLANCO,
          fill_linea=BLANCO, bg_outer="#8B1A1A")),
    ("07_logo_invertido_horizontal",
     dict(bg_circle=VERDE_OSC, stroke_cruz=VERDE_MED, fill_escalon=DORADO,
          fill_texto1=VERDE_OSC, fill_texto2=VERDE_MED, fill_ai=DORADO,
          fill_linea=DORADO, bg_outer=BLANCO, flip=True)),
    ("08_solo_icono_fondo_oscuro",
     dict(bg_circle=VERDE_OSC, stroke_cruz=VERDE_MED, fill_escalon=DORADO,
          fill_texto1=VERDE_OSC, fill_texto2=VERDE_MED, fill_ai=DORADO,
          fill_linea=DORADO, bg_outer=BLANCO, only_icon=True)),
    ("09_solo_icono_fondo_claro",
     dict(bg_circle=GRIS_CLARO, stroke_cruz=VERDE_MED, fill_escalon=DORADO,
          fill_texto1=VERDE_OSC, fill_texto2=VERDE_MED, fill_ai=DORADO,
          fill_linea=DORADO, bg_outer="#EEEEEE", only_icon=True)),
    ("10_escala_grises",
     dict(bg_circle="#2B2B2B", stroke_cruz="#555555", fill_escalon="#AAAAAA",
          fill_texto1="#2B2B2B", fill_texto2="#555555", fill_ai="#AAAAAA",
          fill_linea="#AAAAAA", bg_outer=BLANCO)),
    ("11_logo_fondo_crema",
     dict(bg_circle=VERDE_OSC, stroke_cruz=VERDE_MED, fill_escalon=DORADO,
          fill_texto1=VERDE_OSC, fill_texto2=VERDE_MED, fill_ai=DORADO,
          fill_linea=DORADO, bg_outer="#F5F0E8")),
    ("12_logo_fondo_verde_medio",
     dict(bg_circle=VERDE_OSC, stroke_cruz=VERDE_MED, fill_escalon=DORADO,
          fill_texto1=BLANCO, fill_texto2=DORADO, fill_ai=BLANCO,
          fill_linea=DORADO, bg_outer=VERDE_MED)),
]


def main():
    for nombre, kwargs in VARIACIONES:
        svg  = logo_svg(**kwargs)
        path = f"{OUTPUT_DIR}/{nombre}.png"
        cairosvg.svg2png(bytestring=svg.encode(), write_to=path, scale=2.0)
        print(f"✅ {nombre}.png")

    print(f"\n✅ {len(VARIACIONES)} logos generados en {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
