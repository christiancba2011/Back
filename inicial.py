from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def principal():
    return "hola culiau 😂😂"
 
if __name__ == '__main__': 
    app.run(debug=True)
    
    