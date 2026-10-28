import unittest
from cadastro import CadastroService, ErroCadastro, verificar_senha

def dados_validos(**alteracoes):
    dados = {
        "nome_completo": "Maria da Silva", "cpf": "529.982.247-25",
        "email": "maria@instituto.edu.br", "senha": "senha123",
        "campus": "Campus Recife", "area_formacao": "Computação", "titulacao": "Mestrado",
        "nome_social": "", "sexo": "Outro", "lattes": "https://lattes.cnpq.br/exemplo",
        "telefone": "(81) 99999-0000",
    }
    dados.update(alteracoes)
    return dados

class CadastroServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = CadastroService()

    def test_cadastro_valido_e_perfis_padrao(self):
        usuario = self.service.cadastrar(dados_validos())
        self.assertEqual(usuario.nome_completo, "Maria da Silva")
        self.assertEqual(usuario.perfis, {"ROLE_COORDENADOR", "ROLE_AVALIADOR"})

    def test_campos_obrigatorios(self):
        for campo in ("nome_completo", "cpf", "email", "senha", "campus", "area_formacao", "titulacao"):
            with self.subTest(campo=campo):
                with self.assertRaises(ErroCadastro):
                    CadastroService().cadastrar(dados_validos(**{campo: ""}))

    def test_cpf_duplicado(self):
        self.service.cadastrar(dados_validos())
        with self.assertRaisesRegex(ErroCadastro, "CPF já está cadastrado"):
            self.service.cadastrar(dados_validos(email="outra@instituto.edu.br"))

    def test_email_duplicado_sem_diferenciar_maiusculas(self):
        self.service.cadastrar(dados_validos())
        with self.assertRaisesRegex(ErroCadastro, "e-mail institucional já cadastrado"):
            self.service.cadastrar(dados_validos(cpf="111.444.777-35", email="MARIA@INSTITUTO.EDU.BR"))

    def test_senha_curta(self):
        with self.assertRaisesRegex(ErroCadastro, "pelo menos 6"):
            self.service.cadastrar(dados_validos(senha="12345"))

    def test_hash_senha(self):
        usuario = self.service.cadastrar(dados_validos())
        self.assertNotEqual(usuario.senha_hash, "senha123")
        self.assertTrue(usuario.senha_hash.startswith("pbkdf2_sha256$"))
        self.assertTrue(verificar_senha("senha123", usuario.senha_hash))
        self.assertFalse(verificar_senha("errada", usuario.senha_hash))

    def test_cpf_invalido(self):
        with self.assertRaisesRegex(ErroCadastro, "CPF válido"):
            self.service.cadastrar(dados_validos(cpf="123.456"))

class RotasTests(unittest.TestCase):
    def setUp(self):
        from app import app
        app.config.update(TESTING=True, SECRET_KEY="test-secret")
        self.client = app.test_client()
        app.view_functions["cadastrar"].__globals__["cadastro_service"] = CadastroService()

    def test_sucesso_redireciona_para_login_com_mensagem(self):
        response = self.client.post("/cadastro", data=dados_validos(), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Cadastro realizado com sucesso", response.data)
        self.assertIn(b"Login", response.data)

    def test_erro_mantem_campos_e_nao_reexibe_senha(self):
        self.client.post("/cadastro", data=dados_validos())
        dados = dados_validos(cpf="529.982.247-25", nome_completo="Nome que deve permanecer")
        response = self.client.post("/cadastro", data=dados, follow_redirects=False)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Nome que deve permanecer", response.data)
        self.assertNotIn(b'value="senha123"', response.data)

if __name__ == "__main__":
    unittest.main()
