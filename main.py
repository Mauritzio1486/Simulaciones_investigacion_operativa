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

def simular_marcador():
    # Genera goles realistas basados en una distribución simple
    return random.randint(0, 4), random.randint(0, 4)

def ejecutar_torneo(retornar_cronica=False):
    lista_equipos = list(equipos_base.keys())
    
    if retornar_cronica:
        cronica = "<b>--- FASE DE ELIMINACIÓN DIRECTA ---</b>\n"
        
        # OCTAVOS
        octavos = random.sample(lista_equipos, 16)
        cuartos = []
        cronica += "\n<b>OCTAVOS DE FINAL:</b>\n"
        for i in range(0, 16, 2):
            g1, g2 = simular_marcador()
            # Asegurar un ganador para el relato
            if g1 == g2: g1 += 1 
            ganador = octavos[i] if g1 > g2 else octavos[i+1]
            cuartos.append(ganador)
            cronica += f"{octavos[i]} {g1} - {g2} {octavos[i+1]} | Avanza: {ganador}\n"
        
        # CUARTOS
        semis = []
        cronica += "\n<b>CUARTOS DE FINAL:</b>\n"
        for i in range(0, 8, 2):
            g1, g2 = simular_marcador()
            if g1 == g2: g1 += 1
            ganador = cuartos[i] if g1 > g2 else cuartos[i+1]
            semis.append(ganador)
            cronica += f"{cuartos[i]} {g1} - {g2} {cuartos[i+1]} | Avanza: {ganador}\n"
            
        # FINAL
        g1, g2 = simular_marcador()
        if g1 == g2: g1 += 1
        campeon = semis[0] if g1 > g2 else semis[1]
        cronica += f"\n<b>GRAN FINAL:</b>\n{semis[0]} {g1} - {g2} {semis[1]}\n"
        cronica += f"\n🏆 <b>¡CAMPEÓN: {campeon}!</b>"
        
        return campeon, cronica
    else:
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
    
    html = f"""
    <html>
    <head>
        <title>Simulacion Mundial IO2</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; margin: 40px; background-color: #f0f2f5; color: #1c1e21; }}
            .card {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 900px; margin: auto; }}
            .cronica {{ background-color: #18191a; color: #e4e6eb; padding: 20px; border-radius: 8px; white-space: pre-wrap; font-family: 'Courier New', monospace; font-size: 0.9em; border-left: 6px solid #2ecc71; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 25px; background: white; }}
            th, td {{ padding: 12px; border: 1px solid #dee2e6; text-align: left; }}
            th {{ background-color: #2c3e50; color: white; }}
            tr:nth-child(even) {{ background-color: #f8f9fa; }}
            h1, h2 {{ color: #1a73e8; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Simulación Montecarlo - Mundial</h1>
            <h2>Relato del Torneo de Muestra</h2>
            <div class="cronica">{ultima_cronica}</div>
            <h2>Ranking de Probabilidades (3000 Iteraciones)</h2>
            <table>
                <tr><th>POS</th><th>EQUIPO</th><th>TÍTULOS</th><th>PROBABILIDAD</th></tr>
    """
    for i, (eq, tits) in enumerate(resultados[:15], 1):
        prob = (tits / SIMULACIONES) * 100
        html += f"<tr><td>{i}</td><td>{eq}</td><td>{tits}</td><td>{prob:.2f}%</td></tr>"
    
    html += "</table></div></body></html>"
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)