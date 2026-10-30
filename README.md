# Cadastro de Servidores — Issue 0

Projeto de referência para cadastro de servidores, com validações, hash de senha, perfis padrão, formulário web e testes automatizados.

## Observação sobre as tecnologias
A issue pede Python, mas também exige estrutura Java/Maven, JDK 17 e `maven.yml`. Para respeitar ambos, o ZIP contém a implementação funcional em Python + Flask, testes Python, o workflow Maven solicitado e um esqueleto Maven mínimo. O workflow `python.yml` executa os testes da implementação principal.

A persistência é em memória (`dict`): os dados são perdidos ao reiniciar a aplicação. Não há banco de dados real.

## Requisitos
- Python 3.10 ou superior e pip
- Java 17 e Maven são opcionais, apenas para o esqueleto Maven

## Executar a aplicação
No terminal, dentro da pasta do projeto:
```bash
python -m venv .venv
```
Linux/macOS:
```bash
source .venv/bin/activate
```
Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```
Depois:
```bash
pip install -r requirements.txt
python app.py
```
Abra http://127.0.0.1:5000.

## Executar testes Python
```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
```
Os testes cobrem cadastro válido, campos obrigatórios, CPF/e-mail duplicados, senha curta, hash, perfis e retorno de erro.

## Testar o workflow Maven localmente (opcional)
Com Java 17 e Maven:
```bash
mvn clean test
```

## Regras implementadas
- Campos obrigatórios: nome completo, CPF, e-mail institucional, senha, campus, área de formação e titulação.
- Opcionais: nome social, sexo (inclui “Outro”), Lattes e telefone.
- CPF validado e normalizado; e-mail validado e comparado sem diferenciar maiúsculas/minúsculas.
- Senha mínima de 6 caracteres e armazenamento PBKDF2-HMAC-SHA256 com salt aleatório.
- Perfis padrão `ROLE_COORDENADOR` e `ROLE_AVALIADOR`.
- Sucesso redireciona para `/login`; erros são claros e mantêm os campos, exceto a senha.
- A tela de login é demonstrativa; autenticação completa e banco de dados não fazem parte desta versão.

## Gerenciamento de Editais — Issue 1  

### Descrição

Implementação das funcionalidades de cadastro, edição e listagem de editais, destinadas ao administrador do sistema.

A funcionalidade foi desenvolvida em Java 17, utilizando Maven e JUnit 5 para os testes automatizados.

### Funcionalidades implementadas

- Cadastro de novos editais.
- Edição de editais existentes por meio de um identificador único (ID).
- Listagem dos editais cadastrados.
- Geração automática de ID para cada edital.

### Campos do edital

- Título;
- Número;
- Ano;
- Data de início da submissão;
- Data de fim da submissão;
- Data de início da avaliação;
- Data de fim da avaliação.

### Regras de validação

- A data de início da submissão não pode ser posterior à data de fim da submissão.
- A data de início da avaliação não pode ser posterior à data de fim da avaliação.
- A edição deve localizar o edital pelo seu ID.
- Caso o edital informado não seja encontrado, uma exceção será lançada.

### Testes automatizados

Foram implementados testes utilizando JUnit 5 para verificar:

- Cadastro de editais;
- Listagem de editais;
- Edição de editais;
- Validação das datas de submissão;
- Validação das datas de avaliação;
- Tentativa de edição de edital inexistente.

### Execução dos testes

Na raiz do projeto, execute o comando:

```bash
mvn clean test
```