import random
import math
from itertools import combinations
from flask import Flask
import os

app = Flask(__name__)

# --- PARÁMETROS DE SIMULACIÓN ---
SIMULACIONES = 3000
FACTOR_FATIGA = 0.98 
VARIACION_RATING = 0.05 

equipos_base = {
    'México': [1.8, 1.2], 'Sudáfrica': [1.3, 1.5], 'Corea del Sur': [1.6, 1.3], 'Chequia': [1.7, 1.2],
    'Canadá': [1.6, 1.4], 'Bosnia y Herzegovina': [1.5, 1.4], 'Catar': [1.3, 1.6], 'Suiza': [1.7, 1.1],
    'Brasil': [2.6, 0.8], 'Marruecos': [1.8, 1.0], 'Haití': [1.1, 1.9], 'Escocia': [1.4, 1.3],
    'Estados Unidos': [1.9, 1.2], 'Paraguay': [1.4, 1.1], 'Australia': [1.5, 1.3], 'Turquía': [1.7, 1.3],
    'Alemania': [2.2, 1.1], 'Curazao': [1.0, 2.0], 'Costa de Marfil': [1.7, 1.4], 'Ecuador': [1.7, 1.1],
    'Países Bajos': [2.2, 1.1], 'Japón': [1.9, 1.2], 'Suecia': [1.7, 1.2], 'Túnez': [1.3, 1.4],
    'Bélgica': [2.1, 1.2], 'Egipto': [1.6, 1.3], 'Irán': [1.4, 1.3], 'Nueva Zelanda': [1.1, 1.7],
    'España': [2.3, 1.0], 'Cabo Verde': [1.2, 1.5], 'Arabia Saudita': [1.3, 1.5], 'Uruguay': [1.9, 1.0],
    'Francia': [2.5, 0.8], 'Senegal': [1.8, 1.2], 'Irak': [1.2, 1.6], 'Noruega': [1.8, 1.3],
    'Argentina': [2.6, 0.8], 'Argelia': [1.6, 1.3], 'Austria': [1.7, 1.2], 'Jordania': [1.1, 1.7],
    'Portugal': [2.3, 1.0], 'R.D. Congo': [1.3, 1.5], 'Uzbekistán': [1.2, 1.5], 'Colombia': [1.9, 1.1],
    'Inglaterra': [2.4, 0.9], 'Croacia': [1.9, 1.1], 'Ghana': [1.5, 1.4], 'Panamá': [1.3, 1.6]
}

grupos = {
    'A': ['México', 'Sudáfrica', 'Corea del Sur', 'Chequia'],
    'B': ['Canadá', 'Bosnia y Herzegovina', 'Catar', 'Suiza'],
    'C': ['Brasil', 'Marruecos', 'Haití', 'Escocia'],
    'D': ['Estados Unidos', 'Paraguay', 'Australia', 'Turquía'],
    'E': ['Alemania', 'Curazao', 'Costa de Marfil', 'Ecuador'],
    'F': ['Países Bajos', 'Japón', 'Suecia', 'Túnez'],
    'G': ['Bélgica', 'Egipto', 'Irán', 'Nueva Zelanda'],
    'H': ['España', 'Cabo Verde', 'Arabia Saudita', 'Uruguay'],
    'I': ['Francia', 'Senegal', 'Irak', 'Noruega'],
    'J': ['Argentina', 'Argelia', 'Austria', 'Jordania'],
    'K': ['Portugal', 'R.D. Congo', 'Uzbekistán', 'Colombia'],
    'L': ['Inglaterra', 'Croacia', 'Ghana', 'Panamá']
}

def generar_goles_poisson(lam):
    return sum(1 for _ in range(10) if random.random() < (lam/10)) # Poisson simplificada para Render

def simular_partido(e1, e2, ratings, fatiga):
    atk1 = ratings[e1][0] * fatiga[e1]
    def2 = ratings[e2][1]
    atk2 = ratings[e2][0] * fatiga[e2]
    def1 = ratings[e1][1]
    g1 = generar_goles_poisson(max(0.1, atk1 / def2))
    g2 = generar_goles_poisson(max(0.1, atk2 / def1))
    fatiga[e1] *= FACTOR_FATIGA
    fatiga[e2] *= FACTOR_FATIGA
    return g1, g2

def ejecutar_torneo():
    ratings_sim = {eq: [v[0] * (1 + random.uniform(-VARIACION_RATING, VARIACION_RATING)), v[1]] for eq, v in equipos_base.items()}
    fatiga = {eq: 1.0 for eq in equipos_base}
    clasificados_32 = []
    terceros = []
    for g_id, integrantes in grupos.items():
        puntos = {e: 0 for e in integrantes}; goles = {e: 0 for e in integrantes}
        for e1, e2 in combinations(integrantes, 2):
            g1, g2 = simular_partido(e1, e2, ratings_sim, fatiga)
            goles[e1] += g1; goles[e2] += g2
            if g1 > g2: puntos[e1] += 3
            elif g2 > g1: puntos[e2] += 3
            else: puntos[e1] += 1; puntos[e2] += 1
        res = sorted(integrantes, key=lambda x: (puntos[x], goles[x]), reverse=True)
        clasificados_32.extend([res[0], res[1]])
        terceros.append({'nombre': res[2], 'pts': puntos[res[2]], 'gf': goles[res[2]]})
    mejores_3ros = sorted(terceros, key=lambda x: (x['pts'], x['gf']), reverse=True)[:8]
    clasificados_32.extend([t['nombre'] for t in mejores_3ros])
    actuales = clasificados_32
    random.shuffle(actuales)
    while len(actuales) > 1:
        avanzan = []
        for i in range(0, len(actuales), 2):
            e1, e2 = actuales[i], actuales[i+1]
            g1, g2 = simular_partido(e1, e2, ratings_sim, fatiga)
            if g1 == g2: avanzan.append(random.choice([e1, e2]))
            else: avanzan.append(e1 if g1 > g2 else e2)
        actuales = avanzan
    return actuales[0]

@app.route('/')
def home():
    # Aquí llamamos a tu función que hace los cálculos
    ranking = {}
    for i in range(SIMULACIONES):
        ganador = ejecutar_torneo()
        ranking[ganador] = ranking.get(ganador, 0) + 1
    
    resultados = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    
    # Esto crea la tablita que verás en internet
    html = "<h1>Resultados de la Simulacion</h1><table border='1'>"
    for eq, tits in resultados[:10]:
        html += f"<tr><td>{eq}</td><td>{tits} titulos</td></tr>"
    html += "</table>"
    return html

if __name__ == "__main__":
    # Esto es lo que Render necesita para no dar error
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)