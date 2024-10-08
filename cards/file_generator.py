import os
import random

import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# Cargar respuestas desde el archivo Excel
file_path = "content/QA.xlsx"
df = pd.read_excel(file_path)

# Obtener la columna de respuestas
respuestas = df["Respuesta"].tolist()

# Respuestas especiales (solo una por matriz)
respuestas_especiales = ["Astro.png", "Einstein.png", "Datafam.png"]

# Remover las respuestas especiales de la lista general
respuestas_generales = [r for r in respuestas if r not in respuestas_especiales]


# Función para verificar si una matriz es válida
def es_valida(matriz, filas_usadas, columnas_usadas, diagonales_usadas):
    filas = [frozenset(fila) for fila in matriz]
    columnas = [frozenset(columna) for columna in zip(*matriz)]
    diagonal1 = frozenset([matriz[i][i] for i in range(3)])
    diagonal2 = frozenset([matriz[i][2 - i] for i in range(3)])

    for fila in filas:
        if fila in filas_usadas:
            return False
    for columna in columnas:
        if columna in columnas_usadas:
            return False
    if diagonal1 in diagonales_usadas or diagonal2 in diagonales_usadas:
        return False

    return True


# Generar matrices 3x3 distintas
def generar_matrices(respuestas_generales, respuestas_especiales, cantidad_matrices):
    filas_usadas = set()
    columnas_usadas = set()
    diagonales_usadas = set()
    matrices = []

    while len(matrices) < cantidad_matrices:
        respuestas_seleccionadas = random.sample(respuestas_generales, 8)
        respuesta_especial = random.choice(respuestas_especiales)
        respuestas_seleccionadas.insert(random.randint(0, 8), respuesta_especial)
        matriz = [respuestas_seleccionadas[i : i + 3] for i in range(0, 9, 3)]

        if es_valida(matriz, filas_usadas, columnas_usadas, diagonales_usadas):
            for fila in matriz:
                filas_usadas.add(frozenset(fila))
            for columna in zip(*matriz):
                columnas_usadas.add(frozenset(columna))
            diagonales_usadas.add(frozenset([matriz[i][i] for i in range(3)]))
            diagonales_usadas.add(frozenset([matriz[i][2 - i] for i in range(3)]))
            matrices.append(matriz)

    return matrices


# Definir la cantidad de matrices que deseas generar
cantidad_matrices = 50
matrices_bingo = generar_matrices(respuestas_generales, respuestas_especiales, cantidad_matrices)


# Función para rellenar una plantilla de bingo
def rellenar_plantilla(matriz, plantilla, output_path, index):
    img = Image.open(plantilla)
    draw = ImageDraw.Draw(img)

    # Cargar la fuente personalizada
    try:
        font_path = "content/YourFont.ttf"  # Cambia "YourFont.ttf" a la fuente que prefieras
        font = ImageFont.truetype(font_path, 50)  # Ajusta el tamaño de la fuente aquí (más grande)
    except OSError:
        font = ImageFont.load_default()

    # Color azul oscuro
    color_azul_oscuro = (0, 0, 139)

    # Nuevas coordenadas para los centros de las posiciones de las respuestas en la plantilla
    posiciones = [
        [(327.5, 190), (865, 190), (1157.5, 190)],  # Fila 1
        [(327.5, 420), (600, 420), (865, 420)],  # Fila 2
        [(600, 635), (865, 635), (1157.5, 635)],  # Fila 3
    ]

    # Dibujar las respuestas en las posiciones correspondientes
    for i in range(3):
        for j in range(3):
            x, y = posiciones[i][j]
            text = matriz[i][j]
            # Usar textbbox para calcular el tamaño del texto y alinearlo al centro
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            draw.text((x - text_width / 2, y - text_height / 2), text, font=font, fill=color_azul_oscuro)

    # Guardar la imagen
    img.save(os.path.join(output_path, f"bingo_card_{index}.png"))


# Crear el directorio de salida si no existe
output_dir = "results/"
os.makedirs(output_dir, exist_ok=True)

# Ruta de la plantilla
plantilla = "content/plantilla_bingo.png"

# Rellenar y guardar las tarjetas de bingo
for idx, matriz in enumerate(matrices_bingo, 1):
    rellenar_plantilla(matriz, plantilla, output_dir, idx)

print(f"{cantidad_matrices} tarjetas de bingo generadas y guardadas en {output_dir}")
