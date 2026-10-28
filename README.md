# Cadastro de Servidores — Issue 0

Projeto acadêmico em Java 17 e Maven, sem interface gráfica e sem banco de dados. A persistência é simulada com mapas em memória; os registros são perdidos ao encerrar o programa.

## Requisitos
- JDK 17
- Maven 3.8 ou superior

## Comandos
```bash
mvn clean compile
mvn clean test
```

## Branch da atividade
Na raiz do repositório Git da equipe:
```bash
git switch -c feature/config-ci
```
Se a branch já existir: `git switch feature/config-ci`.

## Enviar para o GitHub
```bash
git add .
git commit -m "feat: implementa cadastro e configuracao de CI"
git push -u origin feature/config-ci
```

O workflow `.github/workflows/maven.yml` executa `mvn clean test` em pushes para `main`, `develop` e `feature/**`, e em pull requests para `main` e `develop`.

## Regras implementadas
- Campos obrigatórios: nome completo, CPF, e-mail institucional, senha, campus, área de formação e titulação.
- Campos opcionais: nome social, sexo (inclui `OUTRO`), link Lattes e telefone.
- Validação dos dígitos verificadores do CPF; normalização de CPF e e-mail.
- CPF e e-mail únicos.
- Senha com no mínimo 6 caracteres, armazenada com hash BCrypt.
- Perfis padrão `ROLE_COORDENADOR` e `ROLE_AVALIADOR`.
- Testes automatizados com JUnit 5.

## Estrutura
```text
.github/workflows/maven.yml
pom.xml
src/main/java/br/edu/ifpe/dominio/{CadastroUsuarioService,Perfil,Sexo,Usuario}.java
src/test/java/br/edu/ifpe/dominio/CadastroUsuarioServiceTest.java
```

Observação: é uma implementação de domínio para a Issue 0, não uma aplicação web. O serviço pode ser integrado a uma interface/API em issues futuras.
