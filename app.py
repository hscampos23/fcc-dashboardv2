from flask import Flask, render_template, jsonify
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from flask import send_file

app = Flask(__name__)

@app.route("/")
def index():
    df = pd.read_csv("fcc_sensing_simulado-tercer intento con predicciones.csv")

    # Convertir columna 'pronosticado' a booleano seguro
    df['pronosticado'] = df['pronosticado'].astype(str).str.lower() == 'true'

    # Crear columnas separadas para datos reales y pronosticados
    df['reales'] = df.apply(lambda row: row['dias_anticipacion'] if not row['pronosticado'] else None, axis=1)
    df['pronosticados'] = df.apply(lambda row: row['dias_anticipacion'] if row['pronosticado'] else None, axis=1)

    # Línea de tiempo de días de anticipación
    trace_reales = go.Scatter(x=df['mes'], y=df['reales'], mode='lines+markers', name='Datos reales', line=dict(color='blue'))
    trace_pronostico = go.Scatter(x=df['mes'], y=df['pronosticados'], mode='lines+markers', name='Datos pronosticados', line=dict(color='orange', dash='dot'))
    layout_linea = go.Layout(title='Evolución del promedio de días de anticipación', xaxis=dict(title='Mes'), yaxis=dict(title='Días de anticipación'))
    fig_linea = go.Figure(data=[trace_reales, trace_pronostico], layout=layout_linea)
    linea_html = pio.to_html(fig_linea, full_html=False)

    return f"""
    <html>
        <head><title>Dashboard FCC</title></head>
        <body>
            <h1 style='text-align:center;'>¿Estamos anticipando efectivamente los riesgos en sistemas TI?</h1>
            <div>{linea_html}</div>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
