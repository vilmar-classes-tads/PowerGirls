import unittest

from projeto import Projeto, StatusProjeto

class ProjetoTest(unittest.TestCase):

    def criar_projeto(self, termo_aceito=True):
        return Projeto(
            titulo="Projeto de inclusão digital",
            resumo="Projeto voltado à inclusão digital.",
            palavras_chave=["inclusão", "tecnologia"],
            publico_alvo="Comunidade acadêmica",
            area_tematica="Tecnologia",
            campus="Recife",
            ods=[4, 9],
            termo_compromisso_aceito=termo_aceito
        )

    def test_projeto_inicia_com_status_rascunho(self):
        projeto = self.criar_projeto()

        self.assertEqual(projeto.status, StatusProjeto.RASCUNHO)

    def test_editar_projeto_em_rascunho(self):
        projeto = self.criar_projeto()

        projeto.editar_projeto(
            "Novo título",
            "Novo resumo",
            ["educação"],
            "Estudantes",
            "Educação",
            "Recife",
            [4],
            True
        )

        self.assertEqual(projeto.titulo, "Novo título")

    def test_submeter_projeto(self):
        projeto = self.criar_projeto()

        projeto.submeter()

        self.assertEqual(projeto.status, StatusProjeto.SUBMETIDO)

    def test_nao_submeter_sem_aceitar_termo(self):
        projeto = self.criar_projeto(termo_aceito=False)

        with self.assertRaises(ValueError):
            projeto.submeter()

    def test_nao_editar_projeto_submetido(self):
        projeto = self.criar_projeto()
        projeto.submeter()

        with self.assertRaises(ValueError):
            projeto.editar_projeto(
                "Outro título",
                "Outro resumo",
                ["teste"],
                "Estudantes",
                "Educação",
                "Recife",
                [4],
                True
            )

    def test_editar_projeto_em_correcao(self):
        projeto = self.criar_projeto()
        projeto.submeter()
        projeto.enviar_para_correcao()

        projeto.editar_projeto(
            "Título corrigido",
            "Resumo corrigido",
            ["correção"],
            "Estudantes",
            "Educação",
            "Recife",
            [4],
            True
        )

        self.assertEqual(projeto.titulo, "Título corrigido")
        self.assertEqual(projeto.status, StatusProjeto.EM_CORRECAO)

    def test_nao_enviar_rascunho_para_correcao(self):
        projeto = self.criar_projeto()

        with self.assertRaises(ValueError):
            projeto.enviar_para_correcao()


if __name__ == "__main__":
    unittest.main()
