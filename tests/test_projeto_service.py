import unittest

from projeto import StatusProjeto
from projeto_service import ProjetoService

class ProjetoServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.service = ProjetoService()

        self.dados = {
            "titulo": "Projeto de inclusão digital",
            "resumo": "Projeto voltado à inclusão digital.",
            "palavras_chave": ["inclusão", "tecnologia"],
            "publico_alvo": "Comunudade acadêmica",
            "area_tematica": "Tecnologia",
            "campus": "Recife",
            "ods": [4, 9],
            "termo_compromisso_aceito": True
        }

        self.email = "coordenador@email.com"

    def test_criar_projeto(self):
        projeto_id = self.service.criar_projeto(
            self.email, self.dados
        )

        projeto = self.service.buscar_projeto(
            projeto_id, self.email
        )

        self.assertIsNotNone(projeto)
        self.assertEqual(projeto.titulo, self.dados["titulo"])
        self.assertEqual(projeto.status, StatusProjeto.RASCUNHO)

    def test_ids_sao_incrementados(self):
        primeiro = self.service.criar_projeto(
            self.email, self.dados
        )

        segundo = self.service.criar_projeto(
            self.email, self.dados
        )

        self.assertEqual(primeiro, 1)
        self.assertEqual(segundo, 2)

    def test_listar_apenas_projetos_do_coordenador(self):
        outro_email = "outro@email.com"

        self.service.criar_projeto(self.email, self.dados)
        self.service.criar_projeto(outro_email, self.dados)

        projetos = self.service.listar_projetos(self.email)

        self.assertEqual(len(projetos), 1)

    def test_coordenador_nao_acessa_projeto_de_outro(self):
        outro_email = "outro@email.com"

        projeto_id = self.service.criar_projeto(
            outro_email, self.dados
        )

        projeto = self.service.buscar_projeto(
            projeto_id, self.email
        )

        self.assertIsNone(projeto)

    def test_editar_projeto(self):
        projeto_id = self.service.criar_projeto(
            self.email, self.dados
        )

        novos_dados = self.dados.copy()
        novos_dados["titulo"] = "Título atualizado"

        self.service.editar_projeto(
            projeto_id, self.email, novos_dados
        )

        projeto = self.service.buscar_projeto(
            projeto_id, self.email
        )

        self.assertEqual(projeto.titulo, "Título atualizado")

    def test_nao_editar_projeto_de_outro_coordenador(self):
        projeto_id = self.service.criar_projeto(
            "outro@email.com", self.dados
        )

        with self.assertRaises(LookupError):
            self.service.editar_projeto(
                projeto_id, self.email, self.dados
            )

    def test_submeter_projeto(self):
        projeto_id = self.service.criar_projeto(
            self.email, self.dados
        )

        self.service.submeter_projeto(projeto_id, self.email)

        projeto = self.service.buscar_projeto(
            projeto_id, self.email
        )

        self.assertEqual(projeto.status, StatusProjeto.SUBMETIDO)

    def test_nao_editar_projeto_submetido(self):
        projeto_id = self.service.criar_projeto(
            self.email, self.dados
        )

        self.service.submeter_projeto(projeto_id, self.email)

        novos_dados = self.dados.copy()
        novos_dados["titulo"] = "Tentativa de alteração"

        with self.assertRaises(ValueError):
            self.service.editar_projeto(
                projeto_id, self.email, novos_dados
            )

    def test_projeto_inexistente(self):
        with self.assertRaises(LookupError):
            self.service.submeter_projeto(999, self.email)

    def test_visualizar_projeto_proprio(self):
        dados = {
            "titulo": "Projeto de teste",
            "resumo": "Resumo do projeto",
            "palavras_chave": ["python", "tecnologia"],
            "publico_alvo": "Estudantes",
            "area_tematica": "Tecnologia",
            "campus": "Recife",
            "ods": [4, 9],
            "termo_compromisso_aceito": True
        }

        projeto_id = self.service.criar_projeto(
            "coordenador@email.com", dados
        )

        projeto = self.service.visualizar_projeto(
            projeto_id, "coordenador@email.com"
        )

        self.assertEqual(projeto.titulo, dados["titulo"])

    def test_visualizar_projeto_de_outro_autor(self):
        dados = {
            "titulo": "Projeto de teste",
            "resumo": "Resumo do projeto",
            "palavras_chave": ["python", "tecnologia"],
            "publico_alvo": "Estudantes",
            "area_tematica": "Tecnologia",
            "campus": "Recife",
            "ods": [4, 9],
            "termo_compromisso_aceito": True
        }

        projeto_id = self.service.criar_projeto(
            "coordenador@email.com", dados
        )

        with self.assertRaises(LookupError):
            self.service.visualizar_projeto(
                projeto_id, "outro@email.com"
            )

        
    def test_listar_projetos_submetidos(self):
        dados = {
            "titulo": "Projeto de teste",
            "resumo": "Resumo do projeto",
            "palavras_chave": ["educação", "tecnologia"],
            "publico_alvo": "Estudantes",
            "area_tematica": "Tecnologia",
            "campus": "Recife",
            "ods": [4, 9],
            "termo_compromisso_aceito": True
        }

        projeto_id = self.service.criar_projeto(
            "coordenador@email.com", dados
        )

        self.service.submeter_projeto(
            projeto_id, "coordenador@email.com"
        )

        projetos = self.service.listar_projetos_submetidos()

        self.assertIn(projeto_id, projetos)


    def test_nao_listar_rascunhos(self):
        dados = {
            "titulo": "Projeto em rascunho",
            "resumo": "Resumo do projeto",
            "palavras_chave": ["educação"],
            "publico_alvo": "Estudantes",
            "area_tematica": "Tecnologia",
            "campus": "Recife",
            "ods": [4],
            "termo_compromisso_aceito": True
        }

        projeto_id = self.service.criar_projeto(
            "coordenador@email.com", dados
        )

        projetos = self.service.listar_projetos_submetidos()

        self.assertNotIn(projeto_id, projetos)


    def test_listar_projetos_submetidos_de_diferentes_autores(self):
        dados = {
            "titulo": "Projeto de teste",
            "resumo": "Resumo do projeto",
            "palavras_chave": ["educação"],
            "publico_alvo": "Estudantes",
            "area_tematica": "Tecnologia",
            "campus": "Recife",
            "ods": [4],
            "termo_compromisso_aceito": True
        }

        primeiro_id = self.service.criar_projeto(
            "coordenador1@email.com", dados
        )

        segundo_id = self.service.criar_projeto(
            "coordenador2@email.com", dados
        )

        self.service.submeter_projeto(
            primeiro_id, "coordenador1@email.com"
        )

        self.service.submeter_projeto(
            segundo_id, "coordenador2@email.com"
        )

        projetos = self.service.listar_projetos_submetidos()

        self.assertIn(primeiro_id, projetos)
        self.assertIn(segundo_id, projetos)

    def test_visualizar_projeto_submetido_de_outro_autor(self):
        dados = {
            "titulo": "Projeto público",
            "resumo": "Resumo do projeto",
            "palavras_chave": ["educação"],
            "publico_alvo": "Estudantes",
            "area_tematica": "Tecnologia",
            "campus": "Recife",
            "ods": [4],
            "termo_compromisso_aceito": True
        }

        projeto_id = self.service.criar_projeto(
            "coordenador@email.com", dados
        )

        self.service.submeter_projeto(
            projeto_id, "coordenador@email.com"
        )

        projeto = self.service.visualizar_projeto(
            projeto_id, "outro_usuario@email.com"
        )

        self.assertEqual(projeto.titulo, "Projeto público")

if __name__ == "__main__":
    unittest.main()
    