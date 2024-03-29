from flask import Flask, render_template, request
import plotly
import json
import plotly.graph_objects as go
from plotly.graph_objs import *
from plotly.subplots import make_subplots
import pandas as pd

app = Flask(__name__, template_folder="templates")

@app.route("/")
def homepage():
    return render_template("page.html", title="HOME PAGE")

@app.route("/<path>")
def doc(path):
    df = pd.read_csv(path + ".csv")

    fig = go.Figure(
        data=go.Bar(
            x=df['date'],
            y=df['time'],
            name="Time",
            marker=dict(color="#a7d5ed"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['score'],
            yaxis="y2",
            name="Scores",
            marker=dict(color="#e14b31"),
        )
    )

    fig.update_layout(
        title=path.capitalize(),
        legend=dict(orientation="h"),
        yaxis=dict(
            title=dict(text="time"),
            side="left",
        ),
        yaxis2=dict(
            title=dict(text="scores"),
            side="right",
            overlaying="y",
            range=[-0.5, 5.5],
        ),
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7,
                        label="7days",
                        step="day",
                        stepmode="backward"),
                    dict(count=14,
                        label="14days",
                        step="day",
                        stepmode="backward"),
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
        )
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = path
    description = """

    """
    return render_template(
        "page.html", graphJSON=graphJSON, header=header, description=description
    )

if __name__ == "__main__":
    app.run(debug=False)