from flask import Flask, render_template, request, redirect, url_for, session
from cadastro import CadastroService, ErroCadastro

app = Flask(__name__)
app.secret_key = "desenvolvimento-troque-esta-chave"
cadastro_service = CadastroService()

@app.get("/")
def index():
    return render_template("cadastro.html", dados={}, erro=None)

@app.post("/cadastro")
def cadastrar():
    chaves = ["nome_completo", "cpf", "email", "senha", "campus",
              "area_formacao", "titulacao", "nome_social", "sexo", "lattes", "telefone"]
    dados = {k: request.form.get(k, "").strip() for k in chaves}
    try:
        cadastro_service.cadastrar(dados)
    except ErroCadastro as exc:
        dados["senha"] = ""
        return render_template("cadastro.html", dados=dados, erro=str(exc)), 400
    session["mensagem_sucesso"] = "Cadastro realizado com sucesso. Faça login para continuar."
    return redirect(url_for("login"))

@app.get("/login")
def login():
    return render_template("login.html", mensagem=session.pop("mensagem_sucesso", None))

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)
