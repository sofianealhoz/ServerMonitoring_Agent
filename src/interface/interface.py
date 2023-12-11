from flask import Flask, render_template
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__, template_folder = 'app/templates')

@app.route('/')
def index():
    # Création d'un graphique simple
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 11]

    plt.plot(x, y)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Sample Plot')

    # Conversion du graphique en format image pour l'afficher dans le template
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('index.html', plot_url=plot_url)

@app.route('/syststatus.html')
def syststatus():


    return render_template('syststatus.html')

@app.route('/network.html')
def network():
    return render_template('network.html')


if __name__ == '__main__':
    app.run(debug=True)
