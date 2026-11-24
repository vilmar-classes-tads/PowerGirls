
import unittest

import app as app_module
from cadastro import CadastroService
from projeto_service import ProjetoService


def dados_usuario(cpf, email, categoria):
    return {
        "nome_completo": "Usuário de Teste",
        "cpf": cpf,
        "email": email,
        "senha": "senha123",
        "campus": "Campus Recife",
        "area_formacao": "Computação",
        "titulacao": "Mestrado",
        "categoria_servidor": categoria,
    }


class PermissoesProjetoTestCase(unittest.TestCase):

    def setUp(self):
        app_module.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret"
        )

        app_module.cadastro_service = CadastroService()
        app_module.projeto_service = ProjetoService()

        self.client = app_module.app.test_client()

        # Cria um técnico-administrativo.
        app_module.cadastro_service.cadastrar(
            dados_usuario(
                "11144477735",
                "tecnico@instituto.edu.br",
                "TECNICO_ADMINISTRATIVO"
            )
        )

        # Cria um coordenador.
        app_module.cadastro_service.cadastrar(
            dados_usuario(
                "52998224725",
                "coordenador@instituto.edu.br",
                "DOCENTE"
            )
        )

        self.email_tecnico = "tecnico@instituto.edu.br"
        self.email_coordenador = "coordenador@instituto.edu.br"

        # Cria um projeto pertencente ao coordenador.
        self.projeto_id = app_module.projeto_service.criar_projeto(
            self.email_coordenador,
            {
                "titulo": "Projeto de teste",
                "resumo": "Resumo do projeto.",
                "palavras_chave": ["tecnologia"],
                "publico_alvo": "Estudantes",
                "area_tematica": "Tecnologia",
                "campus": "Recife",
                "ods": [4, 9],
                "termo_compromisso_aceito": True
            }
        )

    def acessar_como(self, email):
        with self.client.session_transaction() as sess:
            sess["usuario_email"] = email

    def test_tecnico_nao_acessa_cadastro_projeto(self):
        self.acessar_como(self.email_tecnico)

        response = self.client.get(
            "/coordenador/projetos/novo"
        )

        self.assertEqual(response.status_code, 403)

    def test_tecnico_nao_acessa_edicao_projeto(self):
        self.acessar_como(self.email_tecnico)

        response = self.client.get(
            f"/coordenador/projetos/{self.projeto_id}/editar"
        )

        self.assertEqual(response.status_code, 403)

    def test_coordenador_acessa_cadastro_projeto(self):
        self.acessar_como(self.email_coordenador)

        response = self.client.get(
            "/coordenador/projetos/novo"
        )

        self.assertEqual(response.status_code, 200)

    def test_coordenador_acessa_edicao_projeto(self):
        self.acessar_como(self.email_coordenador)

        response = self.client.get(
            f"/coordenador/projetos/{self.projeto_id}/editar"
        )

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
