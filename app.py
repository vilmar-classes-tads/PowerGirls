from datetime import date
from flask import Flask, render_template, request, redirect, url_for, session
from cadastro import (
    CadastroService, 
    ErroCadastro, 
    verificar_senha, 
    ROLE_TECNICO_ADMINISTRATIVO, 
    ROLE_COORDENADOR
)
from projeto_service import ProjetoService

app = Flask(__name__)
app.secret_key = "desenvolvimento-troque-esta-chave"
cadastro_service = CadastroService()
projeto_service = ProjetoService()

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

def usuario_coordenador_logado():
    usuario = obter_usuario_logado()

    return (
        usuario is not None
        and "ROLE_COORDENADOR" in usuario.perfis
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

def exigir_coordenador():
    bloqueio = exigir_login()

    if bloqueio:
        return bloqueio

    if not usuario_coordenador_logado():
        return "Você não tem permissão para gerenciar projetos.", 403

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


def validar_projeto(form):
    dados = {
        "titulo": form.get("titulo", "").strip(),
        "resumo": form.get("resumo", "").strip(),
        "palavras_chave": [
            palavra.strip()
            for palavra in form.get("palavras_chave", "").split(",")
            if palavra.strip()
        ],
        "publico_alvo": form.get("publico_alvo", "").strip(),
        "area_tematica": form.get("area_tematica", "").strip(),
        "campus": form.get("campus", "").strip(),
        "ods": form.getlist("ods"),
        "termo_compromisso_aceito": (
            form.get("termo_compromisso_aceito") == "on"
        )
    }

    campos = {
        "titulo": "Título",
        "resumo": "Resumo",
        "publico_alvo": "Público-alvo",
        "area_tematica": "Área temática",
        "campus": "Campus"
    }

    for campo, nome in campos.items():
        if not dados[campo]:
            return dados, f"O campo {nome} é obrigatório."

    if not dados["palavras_chave"]:
        return dados, "Informe pelo menos uma palavra-chave."

    if not dados["ods"]:
        return dados, "Selecione pelo menos um ODS."

    try:
        dados["ods"] = [int(ods) for ods in dados["ods"]]
    except ValueError:
        return dados, "Selecione ODS válidos."

    return dados, None

@app.get("/coordenador/projetos")
def meus_projetos():
    bloqueio = exigir_coordenador()
    if bloqueio:
        return bloqueio

    projetos = projeto_service.listar_projetos(
        session["usuario_email"]
    )

    return render_template(
        "projetos.html",
        projetos=sorted(projetos.items()),
        usuario_nome=session.get("usuario_nome")
    )

@app.get("/projetos")
def projetos_publicos():
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    projetos = projeto_service.listar_projetos_submetidos()

    return render_template(
        "projetos_publicos.html",
        projetos=sorted(projetos.items()),
        usuario_nome=session.get("usuario_nome")
    )

@app.route("/coordenador/projetos/novo", methods=["GET", "POST"])
def novo_projeto():
    bloqueio = exigir_coordenador()

    if bloqueio:
        return bloqueio

    if request.method == "POST":
        dados, erro = validar_projeto(request.form)

        if erro:
            return render_template(
                "projeto_form.html",
                projeto=dados,
                erro=erro,
                titulo_pagina="Novo projeto",
                url_cancelar=url_for("meus_projetos")
            ), 400

        projeto_service.criar_projeto(
            session["usuario_email"],
            dados
        )

        return redirect(url_for("meus_projetos"))

    return render_template(
        "projeto_form.html",
        projeto={},
        erro=None,
        titulo_pagina="Novo projeto",
        url_cancelar=url_for("meus_projetos")
    )


@app.route("/coordenador/projetos/<int:projeto_id>/editar", methods=["GET", "POST"])
def editar_projeto(projeto_id):
    bloqueio = exigir_coordenador()
    if bloqueio:
        return bloqueio

    projeto = projeto_service.buscar_projeto(
        projeto_id, session["usuario_email"]
    )

    if projeto is None:
        return "Projeto não encontrado.", 404

    # Projetos submetidos não podem ser editados.
    if projeto.status.value == "Submetido":
        return redirect(url_for("visualizar_projeto", projeto_id=projeto_id))

    if request.method == "POST":
        dados, erro = validar_projeto(request.form)

        if erro:
            return render_template(
                "projeto_form.html",
                projeto=dados,
                erro=erro,
                titulo_pagina="Editar projeto",
                url_cancelar=url_for(
                    "visualizar_projeto",
                    projeto_id=projeto_id
               )
            ), 400

        try:
            projeto_service.editar_projeto(
                projeto_id,
                session["usuario_email"],
                dados
            )
        except ValueError as exc:
            return render_template(
                "projeto_form.html",
                projeto=dados,
                erro=str(exc),
                titulo_pagina="Editar projeto",
                url_cancelar=url_for(
                    "visualizar_projeto",
                    projeto_id=projeto_id
                )
            ), 400

        return redirect(
            url_for("visualizar_projeto", projeto_id=projeto_id)
        )

    # Prepara os dados existentes para preencher o formulário.
    dados_projeto = {
        "titulo": projeto.titulo,
        "resumo": projeto.resumo,
        "palavras_chave": projeto.palavras_chave,
        "publico_alvo": projeto.publico_alvo,
        "area_tematica": projeto.area_tematica,
        "campus": projeto.campus,
        "ods": [str(ods) for ods in projeto.ods],
        "termo_compromisso_aceito": projeto.termo_compromisso_aceito
    }

    return render_template(
        "projeto_form.html",
        projeto=dados_projeto,
        erro=None,
        titulo_pagina="Editar projeto",
        url_cancelar=url_for(
            "visualizar_projeto",
            projeto_id=projeto_id
        )
    )


@app.get("/coordenador/projetos/<int:projeto_id>")
def visualizar_projeto(projeto_id):
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    try:
        projeto = projeto_service.visualizar_projeto(
            projeto_id,
            session["usuario_email"]
        )
    except LookupError:
        return "Projeto não encontrado.", 404

    eh_autor = (
        projeto_service.autores.get(projeto_id)
        == session["usuario_email"]
    )

    return render_template(
        "projeto_detalhes.html",
        projeto=projeto,
        projeto_id=projeto_id,
        usuario_nome=session.get("usuario_nome"),
        eh_autor=eh_autor,
        erro=None
    )


@app.post("/coordenador/projetos/<int:projeto_id>/submeter")
def submeter_projeto(projeto_id):
    bloqueio = exigir_coordenador()
    if bloqueio:
        return bloqueio

    try:
        projeto_service.submeter_projeto(
            projeto_id,
            session["usuario_email"]
        )
    except LookupError:
        return "Projeto não encontrado.", 404
    except ValueError as exc:
        projeto = projeto_service.buscar_projeto(
            projeto_id,
            session["usuario_email"]
        )

        return render_template(
            "projeto_detalhes.html",
            projeto=projeto,
            projeto_id=projeto_id,
            usuario_nome=session.get("usuario_nome"),
            eh_autor=True,
            erro=str(exc)
        ), 400

    return redirect(
        url_for("visualizar_projeto", projeto_id=projeto_id)
    )

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
            session["usuario_perfis"] = list(usuario.perfis)
            
            if ROLE_COORDENADOR in usuario.perfis:
                return redirect(url_for("meus_projetos"))
            
            elif ROLE_TECNICO_ADMINISTRATIVO in usuario.perfis: 
                return redirect(url_for("admin_editais"))
            
            return "Você não possui permissão para acessar o sistema.", 403

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
