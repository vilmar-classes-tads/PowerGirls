from datetime import date
from flask import Flask, render_template, request, redirect, url_for, session
from cadastro import CadastroService, ErroCadastro, verificar_senha, ROLE_TECNICO_ADMINISTRATIVO

app = Flask(__name__)
app.secret_key = "desenvolvimento-troque-esta-chave"
cadastro_service = CadastroService()

# Armazenamento em memória dos editais para a versão web.
editais = {}
proximo_edital_id = 1


def obter_usuario_logado():
    email = session.get("usuario_email")

    if not email:
        return None

    cpf = cadastro_service.emails_cadastrados.get(email)

    if not cpf:
        return None

    return cadastro_service.usuarios_por_cpf.get(cpf)


def usuario_admin_logado():
    usuario = obter_usuario_logado()

    return (
        usuario is not None
        and "ROLE_TECNICO_ADMINISTRATIVO" in usuario.perfis
    )


def exigir_login():
    if obter_usuario_logado() is None:
        return redirect(url_for("login"))

    return None


def exigir_admin():
    bloqueio = exigir_login()

    if bloqueio:
        return bloqueio

    if not usuario_admin_logado():
        return "Você não tem permissão para gerenciar editais.", 403

    return None

def validar_edital(form):
    dados = {
        "titulo": form.get("titulo", "").strip(),
        "numero": form.get("numero", "").strip(),
        "ano": form.get("ano", "").strip(),
        "inicio_submissao": form.get("inicio_submissao", "").strip(),
        "fim_submissao": form.get("fim_submissao", "").strip(),
        "inicio_avaliacao": form.get("inicio_avaliacao", "").strip(),
        "fim_avaliacao": form.get("fim_avaliacao", "").strip(),
    }

    if not dados["titulo"]:
        return dados, "O título é obrigatório."

    try:
        dados["numero"] = int(dados["numero"])
        if dados["numero"] <= 0:
            raise ValueError
    except ValueError:
        return dados, "O número do edital deve ser um número inteiro positivo."

    try:
        dados["ano"] = int(dados["ano"])
        if dados["ano"] < 1900:
            raise ValueError
    except ValueError:
        return dados, "O ano deve ser válido."

    campos_data = [
        "inicio_submissao", "fim_submissao",
        "inicio_avaliacao", "fim_avaliacao"
    ]
    try:
        for campo in campos_data:
            dados[campo] = date.fromisoformat(dados[campo])
    except ValueError:
        return dados, "Informe todas as datas corretamente."

    if dados["inicio_submissao"] > dados["fim_submissao"]:
        return dados, "O início da submissão não pode ser posterior ao fim."

    if dados["inicio_avaliacao"] > dados["fim_avaliacao"]:
        return dados, "O início da avaliação não pode ser posterior ao fim."

    return dados, None


@app.get("/")
def index():
    return render_template("cadastro.html", dados={}, erro=None)


@app.post("/cadastro")
def cadastrar():
    chaves = ["nome_completo", "cpf", "email", "senha", "campus", "categoria_servidor",
              "area_formacao", "titulacao", "nome_social", "sexo", "lattes", "telefone"]
    dados = {k: request.form.get(k, "").strip() for k in chaves}
    try:
        cadastro_service.cadastrar(dados)
        print("USUÁRIOS CADASTRADOS:", cadastro_service.usuarios_por_cpf)
    except ErroCadastro as exc:
        dados["senha"] = ""
        return render_template("cadastro.html", dados=dados, erro=str(exc)), 400
    session["mensagem_sucesso"] = "Cadastro realizado com sucesso. Faça login para continuar."
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    mensagem = session.pop("mensagem_sucesso", None)

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        cpf = cadastro_service.emails_cadastrados.get(email)
        usuario = cadastro_service.usuarios_por_cpf.get(cpf) if cpf else None

        if usuario is None or not verificar_senha(senha, usuario.senha_hash):
            erro = "E-mail ou senha inválidos."
        else:
            session["usuario_email"] = usuario.email
            session["usuario_nome"] = usuario.nome_completo
            return redirect(url_for("admin_editais"))

    return render_template("login.html", mensagem=mensagem, erro=erro)


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.get("/admin/editais")
def admin_editais():
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio
    return render_template(
    "edital.html",
    editais=sorted(editais.values(), key=lambda e: e["id"]),
    usuario_nome=session.get("usuario_nome"),
    pode_editar=usuario_admin_logado()
)


@app.route("/admin/editais/novo", methods=["GET", "POST"])
def novo_edital():
    bloqueio = exigir_admin()
    if bloqueio:
        return bloqueio

    if request.method == "POST":
        global proximo_edital_id
        dados, erro = validar_edital(request.form)
        if erro:
            return render_template("edital_form.html", edital=dados, erro=erro, titulo_pagina="Novo edital"), 400

        dados["id"] = proximo_edital_id
        editais[proximo_edital_id] = dados
        proximo_edital_id += 1
        return redirect(url_for("admin_editais"))

    return render_template("edital_form.html", edital={}, erro=None, titulo_pagina="Novo edital")


@app.route("/admin/editais/<int:edital_id>/editar", methods=["GET", "POST"])
def editar_edital(edital_id):
    bloqueio = exigir_admin()
    if bloqueio:
        return bloqueio

    edital = editais.get(edital_id)
    if edital is None:
        return "Edital não encontrado.", 404

    if request.method == "POST":
        dados, erro = validar_edital(request.form)
        dados["id"] = edital_id
        if erro:
            return render_template("edital_form.html", edital=dados, erro=erro, titulo_pagina="Editar edital"), 400
        editais[edital_id] = dados
        return redirect(url_for("admin_editais"))

    return render_template("edital_form.html", edital=edital, erro=None, titulo_pagina="Editar edital")


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)
