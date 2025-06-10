from flask import Flask, render_template
import pandas as pd
import json

app = Flask(__name__)

@app.route('/')
def dashboard():
    df = pd.read_csv("fcc_dias_anticipacion_con_predicciones.csv")

    promedio_anticipacion = round(df['dias_anticipacion'].mean(), 2)
    precision_alertas = round((df['alertas_correctas'] / df['alertas_predictivas']).mean(), 2)
    falsos_negativos = int(df['falsos_negativos'].sum())
    impacto_usd = int(df['impacto_estimado_usd'].sum())

    anticipacion_por_mes = df.groupby('mes').agg({
        'dias_anticipacion': 'mean',
        'dias_anticipacion_predicho': 'mean'
    }).reset_index()

    barras = df.groupby(['tipo_sistema', 'severidad_alerta'])['dias_anticipacion'].mean().unstack(fill_value=0)

    correlacion = df[['dias_anticipacion', 'alertas_correctas', 'impacto_estimado_usd']].corr().round(2).values.tolist()
    etiquetas = ['dias_anticipacion', 'alertas_correctas', 'impacto_estimado_usd']

    data = {
        "meses": anticipacion_por_mes['mes'].tolist(),
        "dias_anticipacion": anticipacion_por_mes['dias_anticipacion'].round(2).tolist(),
        "dias_anticipacion_predicho": anticipacion_por_mes['dias_anticipacion_predicho'].round(2).tolist(),
        "sistemas": list(barras.index),
        "severidades": list(barras.columns),
        "barras": barras.round(2).to_dict(orient='list'),
        "kpis": {
            "promedio_anticipacion": promedio_anticipacion,
            "precision_alertas": precision_alertas,
            "falsos_negativos": falsos_negativos,
            "impacto_usd": impacto_usd
        },
        "correlacion": correlacion,
        "etiquetas_correlacion": etiquetas
    }

    return render_template("index.html", data=json.dumps(data))

if __name__ == '__main__':
    app.run(debug=True)
