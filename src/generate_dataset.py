"""
generate_dataset.py
-------------------
Genera el dataset sintético de itinerarios turísticos para Perú
en formato Alpaca (instruction / input / output).

Uso:
    python src/generate_dataset.py

Salida:
    dataset/dataset_turismo_peru.csv  (800 filas)
"""

import csv
import random
import os

random.seed(42)

# ── Valores posibles ──────────────────────────────────────────
DIAS_OPCIONES       = [3, 5, 7, 10, 14]
PRESUPUESTO_OPC     = ["bajo", "medio", "alto", "lujo"]
INTERESES_OPC       = ["aventura", "cultura", "gastronomía", "naturaleza", "relax", "mixto"]
ORIGEN_OPC          = ["Lima", "Argentina", "Estados Unidos", "España", "Brasil",
                        "Colombia", "Francia", "Alemania", "México", "Chile"]
IDIOMA_MAP          = {
    "Lima": "español", "Argentina": "español", "Colombia": "español",
    "México": "español", "Chile": "español", "España": "español",
    "Brasil": "portugués", "Estados Unidos": "inglés",
    "Francia": "francés", "Alemania": "inglés"
}
GRUPO_OPC           = ["solo", "pareja", "familia con niños", "grupo de amigos", "adultos mayores"]
REGION_OPC          = ["costa", "sierra", "selva", "todo el país"]
DESTINOS_POR_REGION = {
    "sierra": ["Machu Picchu", "Cusco", "Valle Sagrado", "Lago Titicaca",
               "Choquequirao", "Huaraz"],
    "selva":  ["Iquitos", "Manu", "Tarapoto", "Puerto Maldonado"],
    "costa":  ["Lima", "Mancora", "Paracas", "Líneas de Nazca", "Huacachina"],
    "todo el país": [
        "Machu Picchu + Lago Titicaca",
        "Cusco + Lima + Mancora",
        "Ruta Norte: Trujillo + Chiclayo + Máncora",
        "Perú Express: Lima + Cusco + Iquitos"
    ]
}
TEMPORADA_OPC       = ["seca (mayo-octubre)", "lluvia (noviembre-abril)"]

INSTRUCCION = (
    "Genera un itinerario turístico personalizado para el Perú "
    "basado en el perfil del viajero. El itinerario debe incluir "
    "actividades por día, recomendaciones de transporte, alojamiento "
    "según presupuesto y tips culturales relevantes."
)

# ── Bloques de itinerario por destino ─────────────────────────
BLOQUES = {
    "Machu Picchu": [
        "Día 1: Llegada a Cusco. Aclimatación, mate de coca, paseo por la Plaza de Armas.",
        "Día 2: City tour Cusco: Sacsayhuamán, Qorikancha y Mercado de San Pedro.",
        "Día 3: Tren a Aguas Calientes. Tarde libre explorando el pueblo.",
        "Día 4: Amanecer en Machu Picchu. Visita guiada a la ciudadela inca.",
        "Día 5: Regreso a Cusco. Visita al Valle Sagrado: Pisac y Ollantaytambo.",
        "Día 6: Día libre en Cusco o excursión a la Montaña Arcoíris.",
        "Día 7: Vuelo de regreso desde Cusco.",
    ],
    "Lago Titicaca": [
        "Día 1: Llegada a Puno desde Cusco (tren o bus panorámico).",
        "Día 2: Tour en bote a las Islas Flotantes de los Uros.",
        "Día 3: Isla Taquile, almuerzo con vista al lago, textilería local.",
        "Día 4: Isla Amantaní, noche con familia local.",
        "Día 5: Regreso a Puno. Visita al Museo Dreyer.",
    ],
    "Iquitos": [
        "Día 1: Llegada a Iquitos. Paseo por el Malecón Tarapoto.",
        "Día 2: Reserva Nacional Pacaya-Samiria: avistamiento de fauna.",
        "Día 3: Canopy y kayak por tributarios del Amazonas.",
        "Día 4: Visita a comunidades nativas. Medicina tradicional.",
        "Día 5: Mercado de Belén. Vuelo de regreso.",
    ],
    "Mancora": [
        "Día 1: Llegada a Máncora. Check-in y playa.",
        "Día 2: Surf y kitesurf en la playa principal.",
        "Día 3: Tour en lancha: avistamiento de tortugas y delfines.",
        "Día 4: Día de relax y gastronomía costera: ceviche, tiradito.",
        "Día 5: Poza de Barro y Las Pocitas. Tarde libre.",
    ],
    "Lima": [
        "Día 1: Llegada. Barranco y Miraflores: el Parque del Amor y la Huaca Pucllana.",
        "Día 2: Centro Histórico: Plaza Mayor, Catedral y Larco Mar.",
        "Día 3: Visita al Museo Larco y tarde de ceviche en el Mercado Surquillo.",
    ],
    "Paracas": [
        "Día 1: Llegada a Paracas. Reserva Nacional: tour en lancha a Islas Ballestas.",
        "Día 2: Buggy por las dunas de Huacachina.",
        "Día 3: Sobrevuelo a las Líneas de Nazca (opcional).",
    ],
    "Cusco": [
        "Día 1: Llegada y aclimatación. Plaza de Armas y San Blas.",
        "Día 2: Sacsayhuamán y Qorikancha.",
        "Día 3: Valle Sagrado: Pisac, Ollantaytambo.",
        "Día 4: Chinchero y talleres de tejido tradicional.",
    ],
    "Huaraz": [
        "Día 1: Llegada a Huaraz. Aclimatación en la ciudad.",
        "Día 2: Laguna 69: trekking de alta montaña.",
        "Día 3: Chavín de Huántar: sitio arqueológico andino.",
        "Día 4: Laguna Churup y Callejón de Huaylas.",
    ],
}


def generar_itinerario(dias, presupuesto, intereses, grupo, destino, temporada, origen):
    alojamiento = {
        "bajo":  "hostal económico (~$20-30/noche)",
        "medio": "hotel 3 estrellas (~$60-90/noche)",
        "alto":  "hotel boutique 4 estrellas (~$120-180/noche)",
        "lujo":  "hotel de lujo 5 estrellas (~$250+/noche)"
    }[presupuesto]

    tip_temporada = (
        "Lleva ropa impermeable y evita rutas de alta montaña en días de lluvia intensa."
        if "lluvia" in temporada else
        "Es la mejor época para trekking y fotografía. Reserva con anticipación."
    )

    tip_grupo = {
        "solo":              "Únete a tours grupales para conocer otros viajeros.",
        "pareja":            "Reserva cenas románticas con vista panorámica.",
        "familia con niños": "Elige actividades de bajo impacto físico y lleva snacks.",
        "grupo de amigos":   "Los tours privados suelen salir más económicos en grupo.",
        "adultos mayores":   "Prefiere rutas con poco desnivel y toma días de aclimatación extra."
    }[grupo]

    destino_base  = destino.split("+")[0].strip()
    dias_lista    = BLOQUES.get(destino_base, BLOQUES["Cusco"])
    dias_itinerar = dias_lista[:dias]
    if len(dias_itinerar) < dias:
        for i in range(len(dias_itinerar), dias):
            dias_itinerar.append(
                f"Día {i+1}: Día libre para explorar según intereses de {intereses}."
            )

    return (
        "\n".join(dias_itinerar) + "\n\n"
        f"Alojamiento sugerido: {alojamiento}\n"
        f"Tip para {grupo}: {tip_grupo}\n"
        f"Nota de temporada: {tip_temporada}\n"
        f"Transporte recomendado: combis locales para presupuesto bajo; "
        f"taxi/remisse para comodidad."
    )


def main():
    filas = []
    id_counter = 1

    for origen in ORIGEN_OPC:
        for dias in DIAS_OPCIONES:
            for presupuesto in PRESUPUESTO_OPC:
                for intereses in random.sample(INTERESES_OPC, 2):
                    for grupo in random.sample(GRUPO_OPC, 2):
                        region   = random.choice(REGION_OPC)
                        destino  = random.choice(DESTINOS_POR_REGION[region])
                        temporada= random.choice(TEMPORADA_OPC)
                        idioma   = IDIOMA_MAP[origen]

                        input_texto = (
                            f"Turista de {origen}, viaja {grupo}, {dias} días, "
                            f"presupuesto {presupuesto}, intereses: {intereses}, "
                            f"región preferida: {region}, destino: {destino}, "
                            f"temporada: {temporada}, idioma: {idioma}."
                        )
                        output_texto = generar_itinerario(
                            dias, presupuesto, intereses, grupo,
                            destino, temporada, origen
                        )

                        filas.append({
                            "id":               id_counter,
                            "dias_viaje":       dias,
                            "presupuesto":      presupuesto,
                            "intereses":        intereses,
                            "origen_turista":   origen,
                            "idioma":           idioma,
                            "grupo":            grupo,
                            "region_preferida": region,
                            "destino_principal":destino,
                            "temporada":        temporada,
                            "instruction":      INSTRUCCION,
                            "input":            input_texto,
                            "output":           output_texto,
                        })
                        id_counter += 1

    os.makedirs("dataset", exist_ok=True)
    output_path = "dataset/dataset_turismo_peru.csv"
    campos = ["id","dias_viaje","presupuesto","intereses","origen_turista","idioma",
              "grupo","region_preferida","destino_principal","temporada",
              "instruction","input","output"]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(filas)

    print(f"✅ Dataset generado: {len(filas)} filas → {output_path}")


if __name__ == "__main__":
    main()
