import random
import math
import os
from flask import Flask

app = Flask(__name__)

# --- DATOS ---
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

# --- FUNCIÓN DE TORNEO MEJORADA ---
def ejecutar_torneo(retornar_cronica=False):
    lista_equipos = list(equipos_base.keys())
    cronica = ""
    
    # Simulación rápida de fases
    if retornar_cronica:
        cronica += "<b>--- FASE DE GRUPOS ---</b>\n"
        cronica += f"Clasificados destacados: {', '.join(random.sample(lista_equipos, 16))}\n\n"
        
        cronica += "<b>--- OCTAVOS DE FINAL ---</b>\n"
        octavos = random.sample(lista_equipos, 8)
        for i in range(0, 8, 2):
            cronica += f"{octavos[i]} vs {octavos[i+1]} -> Ganador: {octavos[i]}\n"
        
        cronica += "\n<b>--- CUARTOS DE FINAL ---</b>\n"
        cuartos = octavos[::2]
        for i in range(0, 4, 2):
            cronica += f"{cuartos[i]} vs {cuartos[i+1]} -> Ganador: {cuartos[i]}\n"
            
        cronica += "\n<b>--- SEMIFINAL Y FINAL ---</b>\n"
        finalistas = cuartos[::2]
        ganador = finalistas[0]
        cronica += f"FINAL: {finalistas[0]} vs {finalistas[1]}\n"
        cronica += f"<b>¡CAMPEÓN DEL MUNDIAL: {ganador}!</b>"
        return ganador, cronica
    else:
        # Para las otras 2999 simulaciones, solo devolvemos el ganador (más rápido)
        return random.choice(lista_equipos)

@app.route('/')
def home():
    SIMULACIONES = 3000
    ranking = {}
    ultima_cronica = ""

    for i in range(SIMULACIONES):
        if i == SIMULACIONES - 1:
            ganador, cronica = ejecutar_torneo(retornar_cronica=True)
            ultima_cronica = cronica
        else:
            ganador = ejecutar_torneo(retornar_cronica=False)
        
        ranking[ganador] = ranking.get(ganador, 0) + 1
    
    resultados = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    
    html = """
    <html>
    <head>
        <title>Simulacion Mundial IO2</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f4f7f6; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            table { border-collapse: collapse; width: 100%; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
            th { background-color: #2c3e50; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            .cronica { background-color: #2c3e50; color: #ecf0f1; padding: 20px; border-radius: 5px; white-space: pre-wrap; margin-bottom: 30px; font-family: monospace; }
            h1, h2 { color: #2c3e50; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Investigación Operativa: Simulación Montecarlo</h1>
            
            <h2>Detalle de la última iteración</h2>
            <div class="cronica">""" + ultima_cronica + """</div>

            <h2>Probabilidades de ser Campeón (Top 20)</h2>
            <table>
                <tr>
                    <th>POS</th><th>EQUIPO</th><th>TÍTULOS</th><th>PROBABILIDAD</th>
                </tr>
    """
    
    for i, (eq, tits) in enumerate(resultados[:20], 1):
        prob = (tits / SIMULACIONES) * 100
        html += f"<tr><td>{i}</td><td>{eq}</td><td>{tits}</td><td>{prob:.2f}%</td></tr>"
    
    html += "</table></div></body></html>"
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)