from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def api():
    data = {'mensagem': 'Olá, mundo!'}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)