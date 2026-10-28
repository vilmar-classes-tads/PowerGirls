import hashlib
import hmac
import re
import secrets
from dataclasses import dataclass, field

PERFIS_PADRAO = {"ROLE_COORDENADOR", "ROLE_AVALIADOR"}

class ErroCadastro(ValueError):
    pass

def hash_senha(senha: str, salt: bytes | None = None) -> str:
    """Gera hash PBKDF2 com salt aleatório."""
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, 310_000)
    return f"pbkdf2_sha256${salt.hex()}${digest.hex()}"

def verificar_senha(senha: str, senha_hash: str) -> bool:
    try:
        algoritmo, salt_hex, digest_hex = senha_hash.split("$", 2)
        if algoritmo != "pbkdf2_sha256":
            return False
        calculado = hashlib.pbkdf2_hmac(
            "sha256", senha.encode("utf-8"), bytes.fromhex(salt_hex), 310_000
        )
        return hmac.compare_digest(calculado, bytes.fromhex(digest_hex))
    except (ValueError, TypeError):
        return False

def normalizar_cpf(cpf: str) -> str:
    return re.sub(r"\D", "", cpf or "")

def cpf_valido(cpf: str) -> bool:
    cpf = normalizar_cpf(cpf)
    return len(cpf) == 11 and cpf.isdigit()

@dataclass
class Usuario:
    nome_completo: str
    cpf: str
    email: str
    senha_hash: str
    campus: str
    area_formacao: str
    titulacao: str
    nome_social: str = ""
    sexo: str = ""
    lattes: str = ""
    telefone: str = ""
    perfis: set[str] = field(default_factory=lambda: set(PERFIS_PADRAO))

class CadastroService:
    """Serviço de cadastro com armazenamento em memória."""

    def __init__(self):
        self.usuarios_por_cpf = {}
        self.emails_cadastrados = {}

    def cadastrar(self, dados: dict) -> Usuario:
        obrigatorios = {
            "nome_completo": "Nome completo", "cpf": "CPF", "email": "E-mail institucional",
            "senha": "Senha", "campus": "Campus", "area_formacao": "Área de formação",
            "titulacao": "Titulação",
        }
        for campo, rotulo in obrigatorios.items():
            if not str(dados.get(campo, "")).strip():
                raise ErroCadastro(f"O campo {rotulo} é obrigatório.")

        cpf = normalizar_cpf(dados["cpf"])
        if not cpf_valido(cpf):
            raise ErroCadastro("Informe um CPF válido.")
        email = dados["email"].strip().lower()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            raise ErroCadastro("Informe um e-mail válido.")
        if len(dados["senha"]) < 6:
            raise ErroCadastro("A senha deve possuir pelo menos 6 caracteres.")
        if cpf in self.usuarios_por_cpf:
            raise ErroCadastro("Este CPF já está cadastrado.")
        if email in self.emails_cadastrados:
            raise ErroCadastro("Este e-mail institucional já cadastrado.")

        lattes = dados.get("lattes", "").strip()
        if lattes and not re.match(r"^https?://", lattes, re.IGNORECASE):
            raise ErroCadastro("O Link do Lattes deve começar com http:// ou https://.")
        sexo = dados.get("sexo", "").strip()
        if sexo not in {"", "Feminino", "Masculino", "Outro", "Prefiro não informar"}:
            raise ErroCadastro("Selecione uma opção válida para Sexo.")

        usuario = Usuario(
            nome_completo=dados["nome_completo"].strip(), cpf=cpf, email=email,
            senha_hash=hash_senha(dados["senha"]), campus=dados["campus"].strip(),
            area_formacao=dados["area_formacao"].strip(), titulacao=dados["titulacao"].strip(),
            nome_social=dados.get("nome_social", "").strip(), sexo=sexo, lattes=lattes,
            telefone=dados.get("telefone", "").strip(), perfis=set(PERFIS_PADRAO),
        )
        self.usuarios_por_cpf[cpf] = usuario
        self.emails_cadastrados[email] = cpf
        return usuario
