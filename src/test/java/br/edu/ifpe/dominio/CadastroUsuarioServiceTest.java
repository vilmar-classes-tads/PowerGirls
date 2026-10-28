package br.edu.ifpe.dominio;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import static org.junit.jupiter.api.Assertions.*;

class CadastroUsuarioServiceTest {
    private CadastroUsuarioService service;
    @BeforeEach void setUp() { service = new CadastroUsuarioService(); }

    private CadastroUsuarioService.DadosCadastro dadosValidos() {
        return new CadastroUsuarioService.DadosCadastro("Maria da Silva", "529.982.247-25",
                "maria@instituicao.edu.br", "senha123", "Campus Recife", "Computação", "Mestrado",
                null, Sexo.FEMININO, null, null);
    }

    @Test void deveCadastrarComDadosValidos() {
        Usuario u = service.cadastrar(dadosValidos());
        assertEquals("Maria da Silva", u.getNomeCompleto());
        assertEquals("52998224725", u.getCpf());
        assertEquals(1, service.quantidadeUsuarios());
    }
    @Test void deveNormalizarCpfEEmail() {
        Usuario u = service.cadastrar(dadosValidos());
        assertTrue(service.buscarPorCpf("529.982.247-25").isPresent());
        assertSame(u, service.buscarPorEmail(" MARIA@INSTITUICAO.EDU.BR ").orElseThrow());
    }
    @Test void deveRecusarCpfDuplicado() {
        service.cadastrar(dadosValidos());
        var d = new CadastroUsuarioService.DadosCadastro("Outra Pessoa", "52998224725", "outra@instituicao.edu.br", "senha123", "Campus Recife", "Administração", "Especialização", null, null, null, null);
        assertThrows(IllegalArgumentException.class, () -> service.cadastrar(d));
        assertEquals(1, service.quantidadeUsuarios());
    }
    @Test void deveRecusarEmailDuplicadoIgnorandoMaiusculas() {
        service.cadastrar(dadosValidos());
        var d = new CadastroUsuarioService.DadosCadastro("Outra Pessoa", "111.444.777-35", "MARIA@INSTITUICAO.EDU.BR", "senha123", "Campus Recife", "Administração", "Especialização", null, null, null, null);
        assertThrows(IllegalArgumentException.class, () -> service.cadastrar(d));
    }
    @Test void deveRecusarCpfInvalido() {
        var d = new CadastroUsuarioService.DadosCadastro("Maria", "111.111.111-11", "maria@instituicao.edu.br", "senha123", "Campus Recife", "Computação", "Mestrado", null, null, null, null);
        assertThrows(IllegalArgumentException.class, () -> service.cadastrar(d));
    }
    @Test void deveRecusarSenhaCurta() {
        var d = new CadastroUsuarioService.DadosCadastro("Maria", "529.982.247-25", "maria@instituicao.edu.br", "12345", "Campus Recife", "Computação", "Mestrado", null, null, null, null);
        assertThrows(IllegalArgumentException.class, () -> service.cadastrar(d));
    }
    @Test void deveRecusarCampoObrigatorioVazio() {
        var d = new CadastroUsuarioService.DadosCadastro(" ", "529.982.247-25", "maria@instituicao.edu.br", "senha123", "Campus Recife", "Computação", "Mestrado", null, null, null, null);
        assertThrows(IllegalArgumentException.class, () -> service.cadastrar(d));
    }
    @Test void deveGuardarSenhaComHashBcrypt() {
        Usuario u = service.cadastrar(dadosValidos());
        assertNotEquals("senha123", u.getSenhaHash());
        assertTrue(new BCryptPasswordEncoder().matches("senha123", u.getSenhaHash()));
    }
    @Test void deveAtribuirPerfisPadrao() {
        Usuario u = service.cadastrar(dadosValidos());
        assertTrue(u.getPerfis().contains(new Perfil("ROLE_COORDENADOR")));
        assertTrue(u.getPerfis().contains(new Perfil("ROLE_AVALIADOR")));
        assertEquals(2, u.getPerfis().size());
    }
    @Test void deveAceitarSexoOutroECamposOpcionais() {
        var d = new CadastroUsuarioService.DadosCadastro("João da Silva", "529.982.247-25", "joao@instituicao.edu.br", "senha123", "Campus Recife", "Computação", "Doutorado", "Jo", Sexo.OUTRO, "https://lattes.cnpq.br/exemplo", "(81) 99999-0000");
        Usuario u = service.cadastrar(d);
        assertEquals(Sexo.OUTRO, u.getSexo()); assertEquals("Jo", u.getNomeSocial());
        assertEquals("https://lattes.cnpq.br/exemplo", u.getLinkLattes()); assertEquals("(81) 99999-0000", u.getTelefone());
    }
}
