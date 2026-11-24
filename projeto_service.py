from projeto import Projeto


class ProjetoService:
    """Serviço de gerenciamento de projetos com armazenamento em memória."""

    def __init__(self):
        self.projetos = {}
        self.autores = {}
        self.proximo_id = 1

    def criar_projeto(self, email_autor, dados):
        projeto = Projeto(
            titulo=dados["titulo"],
            resumo=dados["resumo"],
            palavras_chave=dados["palavras_chave"],
            publico_alvo=dados["publico_alvo"],
            area_tematica=dados["area_tematica"],
            campus=dados["campus"],
            ods=dados["ods"],
            termo_compromisso_aceito=dados["termo_compromisso_aceito"]
        )

        projeto_id = self.proximo_id

        self.projetos[projeto_id] = projeto
        self.autores[projeto_id] = email_autor

        self.proximo_id += 1

        return projeto_id

    def listar_projetos(self, email_autor):
        return {
            projeto_id: projeto
            for projeto_id, projeto in self.projetos.items()
            if self.autores[projeto_id] == email_autor
        }

    def listar_projetos_submetidos(self):
        return {
            projeto_id: projeto
            for projeto_id, projeto in self.projetos.items()
            if projeto.status.value == "Submetido"
        }

    def buscar_projeto(self, projeto_id, email_autor):
        if self.autores.get(projeto_id) != email_autor:
            return None

        return self.projetos.get(projeto_id)

    def visualizar_projeto(self, projeto_id, email_usuario):
        projeto = self.projetos.get(projeto_id)

        if projeto is None:
            raise LookupError("Projeto não encontrado.")

        eh_autor = self.autores.get(projeto_id) == email_usuario
        esta_submetido = projeto.status.value == "Submetido"

        if not eh_autor and not esta_submetido:
            raise LookupError("Projeto não encontrado.")

        return projeto

    def editar_projeto(self, projeto_id, email_autor, dados):
        projeto = self.buscar_projeto(projeto_id, email_autor)

        if projeto is None:
            raise LookupError("Projeto não encontrado.")

        projeto.editar_projeto(
            titulo=dados["titulo"],
            resumo=dados["resumo"],
            palavras_chave=dados["palavras_chave"],
            publico_alvo=dados["publico_alvo"],
            area_tematica=dados["area_tematica"],
            campus=dados["campus"],
            ods=dados["ods"],
            termo_compromisso_aceito=dados["termo_compromisso_aceito"]
        )

    def submeter_projeto(self, projeto_id, email_autor):
        projeto = self.buscar_projeto(projeto_id, email_autor)

        if projeto is None:
            raise LookupError("Projeto não encontrado.")

        projeto.submeter()
