import randomrd /s /q .git
import math
from itertools import combinations


from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Simulación terminada. Revisa los logs de Render para ver los resultados."

# ... aquí va todo tu código de simulación ...

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
# --- PARÁMETROS DE SIMULACIÓN ---
SIMULACIONES = 3000
FACTOR_FATIGA = 0.98  # Cada partido reduce el ataque un 2%
VARIACION_RATING = 0.05 # 5% de variabilidad por simulación (Sensibilidad)

# Datos de entrada (Ataque, Defensa)
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
    L = math.exp(-lam)
    k, p = 0, 1
    while p > L:
        k += 1
        p *= random.random()
    return k - 1

def simular_partido(e1, e2, ratings, fatiga, mostrar=False):
    # Aplicar fatiga al ataque
    atk1 = ratings[e1][0] * fatiga[e1]
    def2 = ratings[e2][1]
    atk2 = ratings[e2][0] * fatiga[e2]
    def1 = ratings[e1][1]

    lambda1 = max(0.1, atk1 / def2)
    lambda2 = max(0.1, atk2 / def1)
    
    g1, g2 = generar_goles_poisson(lambda1), generar_goles_poisson(lambda2)
    
    # El partido genera cansancio
    fatiga[e1] *= FACTOR_FATIGA
    fatiga[e2] *= FACTOR_FATIGA
    
    if mostrar: print(f"    {e1} {g1} - {g2} {e2}")
    return g1, g2

def ejecutar_torneo(mostrar=False):
    # 0. Preparar ratings con variabilidad (Análisis de Sensibilidad)
    ratings_simulacion = {}
    for eq, vals in equipos_base.items():
        var = 1 + random.uniform(-VARIACION_RATING, VARIACION_RATING)
        ratings_simulacion[eq] = [vals[0] * var, vals[1]]
    
    fatiga = {eq: 1.0 for eq in equipos_base}
    
    # 1. FASE DE GRUPOS
    clasificados_32 = []
    terceros = []
    
    for g_id, integrantes in grupos.items():
        puntos = {e: 0 for e in integrantes}; goles = {e: 0 for e in integrantes}
        if mostrar: print(f"\nGRUPO {g_id}:")
        for e1, e2 in combinations(integrantes, 2):
            g1, g2 = simular_partido(e1, e2, ratings_simulacion, fatiga, mostrar)
            goles[e1] += g1; goles[e2] += g2
            if g1 > g2: puntos[e1] += 3
            elif g2 > g1: puntos[e2] += 3
            else: puntos[e1] += 1; puntos[e2] += 1
        
        res = sorted(integrantes, key=lambda x: (puntos[x], goles[x]), reverse=True)
        clasificados_32.extend([res[0], res[1]])
        terceros.append({'nombre': res[2], 'pts': puntos[res[2]], 'gf': goles[res[2]]})

    mejores_3ros = sorted(terceros, key=lambda x: (x['pts'], x['gf']), reverse=True)[:8]
    clasificados_32.extend([t['nombre'] for t in mejores_3ros])

    # 2. ELIMINATORIAS
    actuales = clasificados_32
    random.shuffle(actuales)
    etapas = ["DIECISEISAVOS", "OCTAVOS", "CUARTOS", "SEMIFINAL", "FINAL"]
    
    for etapa in etapas:
        if mostrar: print(f"\n--- {etapa} ---")
        avanzan = []
        for i in range(0, len(actuales), 2):
            e1, e2 = actuales[i], actuales[i+1]
            g1, g2 = simular_partido(e1, e2, ratings_simulacion, fatiga, mostrar)
            if g1 == g2:
                ganador = random.choice([e1, e2])
                if mostrar: print(f"      (Empate {g1}-{g2} | {ganador} por penales)")
            else:
                ganador = e1 if g1 > g2 else e2
            avanzan.append(ganador)
        actuales = avanzan
        if len(actuales) == 1: break

    return actuales[0]

if __name__ == "__main__":
    ranking = {}
    print(f"--- Iniciando Simulación Robusta Montecarlo ({SIMULACIONES} iteraciones) ---")
    
    for i in range(SIMULACIONES):
        ver_detalle = (i == SIMULACIONES - 1)
        ganador = ejecutar_torneo(mostrar=ver_detalle)
        ranking[ganador] = ranking.get(ganador, 0) + 1
        if (i+1) % 1000 == 0: print(f"Hito: {i+1} mundiales simulados...")

    print("\n" + "="*60)
    print(f" PREDICCIÓN FINAL BASADA EN INVESTIGACIÓN OPERATIVA ")
    print("="*60)
    resultados = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    print(f"{'POS':<4} | {'EQUIPO':<20} | {'TÍTULOS':<10} | {'PROBABILIDAD'}")
    print("-" * 60)
    for pos, (eq, tits) in enumerate(resultados[:15], 1):
        print(f"{pos:<4} | {eq:<20} | {tits:<10} | {(tits/SIMULACIONES)*100:.2f}%")

        import os

if __name__ == '__main__':
    # Esto lee el puerto que te asigne el servidor, o usa 4000 por defecto
    port = int(os.environ.get("PORT", 4000))
    app.run(host='0.0.0.0', port=port)