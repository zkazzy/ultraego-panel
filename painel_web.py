from flask import Flask, request, render_template_string
import threading, time
from threading import Event

app = Flask(__name__)
painel_ativo = Event()

HTML = """
<!DOCTYPE html>
<html>
<head><title>ULTRAEGO Painel</title></head>
<body style="font-family:sans-serif; text-align:center;">
    <h1>ULTRAEGO 7.1</h1>
    <p>Status: <b style="color:{{ cor }}">{{ status }}</b></p>
    <form method="post">
        <button name="acao" value="ativar">Ativar</button>
        <button name="acao" value="desativar">Desativar</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def controle():
    if request.method == "POST":
        acao = request.form.get("acao")
        if acao == "ativar":
            painel_ativo.set()
        else:
            painel_ativo.clear()
    status = "Ativo" if painel_ativo.is_set() else "Desativado"
    cor = "green" if painel_ativo.is_set() else "red"
    return render_template_string(HTML, status=status, cor=cor)

def loop_ultraego():
    while True:
        if painel_ativo.is_set():
            print("✅ ULTRAEGO executando...")
            # Aqui você pode chamar suas funções reais
        else:
            print("⛔ ULTRAEGO está desativado.")
        time.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=loop_ultraego, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
