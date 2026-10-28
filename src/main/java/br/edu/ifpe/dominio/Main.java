
package br.edu.ifpe.dominio;

public class Main {
    public static void main(String[] args) {
        CadastroUsuarioService service = new CadastroUsuarioService();

        var dados = new CadastroUsuarioService.DadosCadastro(
                "Maria da Silva",
                "529.982.247-25",
                "maria@instituicao.edu.br",
                "senha123",
                "Campus Recife",
                "Computação",
                "Mestrado",
                "Maria",
                Sexo.FEMININO,
                "https://lattes.cnpq.br/exemplo",
                "(81) 99999-0000"
        );

        try {
            Usuario usuario = service.cadastrar(dados);

            System.out.println("Cadastro realizado com sucesso!");
            System.out.println("Nome: " + usuario.getNomeCompleto());
            System.out.println("CPF: " + usuario.getCpf());
            System.out.println("E-mail: " + usuario.getEmailInstitucional());
            System.out.println("Campus: " + usuario.getCampus());
            System.out.println("Perfis: " + usuario.getPerfis());
            System.out.println("Senha armazenada em hash? "
                    + !usuario.getSenhaHash().equals("senha123"));
            System.out.println("Total de usuários: " + service.quantidadeUsuarios());

        } catch (IllegalArgumentException e) {
            System.out.println("Erro no cadastro: " + e.getMessage());
        }
    }
}
