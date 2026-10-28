package br.edu.ifpe.dominio;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class CadastroServiceTest {
    private CadastroService service;

    @BeforeEach
    void preparar() { service = new CadastroService(); }

    @Test
    void deveCadastrarUsuarioEAdicionarPerfisPadrao() {
        Usuario usuario = service.cadastrar("Maria Silva", "123.456.789-00", "MARIA@ifpe.edu.br", "senha123");
        assertEquals("Maria Silva", usuario.getNome());
        assertEquals("12345678900", usuario.getCpf());
        assertEquals("maria@ifpe.edu.br", usuario.getEmail());
        assertTrue(usuario.getPerfis().contains(Perfil.ROLE_COORDENADOR));
        assertTrue(usuario.getPerfis().contains(Perfil.ROLE_AVALIADOR));
        assertEquals(1, service.quantidadeUsuarios());
    }

    @Test
    void naoDevePermitirCpfDuplicadoMesmoFormatadoDiferente() {
        service.cadastrar("Maria", "12345678900", "maria@ifpe.edu.br", "senha123");
        assertThrows(IllegalArgumentException.class,
            () -> service.cadastrar("João", "123.456.789-00", "joao@ifpe.edu.br", "senha123"));
    }

    @Test
    void naoDevePermitirEmailDuplicadoIgnorandoMaiusculas() {
        service.cadastrar("Maria", "12345678900", "maria@ifpe.edu.br", "senha123");
        assertThrows(IllegalArgumentException.class,
            () -> service.cadastrar("João", "98765432100", "MARIA@ifpe.edu.br", "senha123"));
    }

    @Test
    void deveValidarCamposObrigatoriosEmailCpfESenha() {
        assertThrows(IllegalArgumentException.class, () -> service.cadastrar("", "12345678900", "a@b.com", "senha123"));
        assertThrows(IllegalArgumentException.class, () -> service.cadastrar("Maria", "123", "a@b.com", "senha123"));
        assertThrows(IllegalArgumentException.class, () -> service.cadastrar("Maria", "12345678900", "email-invalido", "senha123"));
        assertThrows(IllegalArgumentException.class, () -> service.cadastrar("Maria", "12345678900", "a@b.com", "123"));
    }

    @Test
    void devePermitirBuscarUsuarioPorCpfOuEmail() {
        Usuario criado = service.cadastrar("Maria", "12345678900", "maria@ifpe.edu.br", "senha123");
        assertSame(criado, service.buscarPorCpf("123.456.789-00"));
        assertSame(criado, service.buscarPorEmail("MARIA@ifpe.edu.br"));
    }
}
