
from flask import Flask, render_template
from monitoring import (
    get_server_details,
    get_monitoring_data
)

app = Flask(__name__)


@app.route('/')
def dashboard():

    server = get_server_details()

    metrics = get_monitoring_data()

    return render_template(
        'dashboard.html',
        server=server,
        metrics=metrics
    )


if __name__ == '__main__':

    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
