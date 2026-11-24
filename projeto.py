from enum import Enum


class StatusProjeto(Enum):
    RASCUNHO = "Rascunho"
    SUBMETIDO = "Submetido"
    EM_CORRECAO = "Em Correção"


class Projeto:

    def __init__(
        self,
        titulo,
        resumo,
        palavras_chave,
        publico_alvo,
        area_tematica,
        campus,
        ods,
        termo_compromisso_aceito
    ):
        self.status = StatusProjeto.RASCUNHO

        self.editar_projeto(
            titulo,
            resumo,
            palavras_chave,
            publico_alvo,
            area_tematica,
            campus,
            ods,
            termo_compromisso_aceito
        )

    def editar_projeto(
        self,
        titulo,
        resumo,
        palavras_chave,
        publico_alvo,
        area_tematica,
        campus,
        ods,
        termo_compromisso_aceito
    ):
        if self.status not in (
            StatusProjeto.RASCUNHO,
            StatusProjeto.EM_CORRECAO
        ):
            raise ValueError(
                "Não é permitido editar um projeto submetido."
            )

        campos = {
            "Título": titulo,
            "Resumo": resumo,
            "Público-alvo": publico_alvo,
            "Área temática": area_tematica,
            "Campus": campus
        }

        for nome, valor in campos.items():
            if not isinstance(valor, str) or not valor.strip():
                raise ValueError(f"{nome} é obrigatório.")

        if palavras_chave is None:
            raise ValueError("Palavras-chave não podem ser nulas.")

        if ods is None:
            raise ValueError("ODS não podem ser nulos.")

        self.titulo = titulo.strip()
        self.resumo = resumo.strip()
        self.palavras_chave = list(palavras_chave)
        self.publico_alvo = publico_alvo.strip()
        self.area_tematica = area_tematica.strip()
        self.campus = campus.strip()
        self.ods = list(ods)
        if not isinstance(termo_compromisso_aceito, bool):
            raise ValueError("O aceite do Termo de Compromisso deve ser informado.")
        self.termo_compromisso_aceito = termo_compromisso_aceito
    
    def submeter(self):
        if self.status not in (
            StatusProjeto.RASCUNHO,
            StatusProjeto.EM_CORRECAO
        ):
            raise ValueError(
                "Somente projetos em rascunho ou correção podem ser submetidos."
            )

        if not self.termo_compromisso_aceito:
            raise ValueError(
                "É necessário aceitar o Termo de Compromisso."
            )

        self.status = StatusProjeto.SUBMETIDO

    def enviar_para_correcao(self):
        if self.status != StatusProjeto.SUBMETIDO:
            raise ValueError(
                "Somente projetos submetidos podem entrar em correção."
            )

        self.status = StatusProjeto.EM_CORRECAO
