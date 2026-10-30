
package br.edu.ifpe.dominio;

import static org.junit.jupiter.api.Assertions.*;

import java.time.LocalDate;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

//Testa as funcionalidades e regras de negócio dos editais.
class EditalServiceTest {

    private EditalService service;

    @BeforeEach

    // Cria uma nova instância do serviço antes de cada teste.
    void configurar() {
        service = new EditalService();
    }

    private Edital criarEdital() {
        return new Edital(
                "Edital de Extensão",
                1,
                2026,
                LocalDate.of(2026, 3, 1),
                LocalDate.of(2026, 3, 30),
                LocalDate.of(2026, 4, 1),
                LocalDate.of(2026, 4, 30));
    }

    @Test
    void deveCadastrarEdital() {
        Edital edital = criarEdital();

        service.cadastrar(edital);

        assertEquals(1, service.listar().size());
    }

    @Test
    void deveListarEditais() {
        service.cadastrar(criarEdital());
        service.cadastrar(criarEdital());

        assertEquals(2, service.listar().size());
    }

    @Test
    void deveEditarEdital() {
        Edital edital = criarEdital();
        service.cadastrar(edital);

        Edital novosDados = new Edital(
                "Edital de Pesquisa",
                2,
                2026,
                LocalDate.of(2026, 5, 1),
                LocalDate.of(2026, 5, 30),
                LocalDate.of(2026, 6, 1),
                LocalDate.of(2026, 6, 30));

        service.editar(edital.getId(), novosDados);

        assertEquals("Edital de Pesquisa",
                service.listar().get(0).getTitulo());
    }

    @Test
    void naoDeveCadastrarComDatasDeSubmissaoInvalidas() {
        Edital edital = new Edital(
                "Edital inválido",
                3,
                2026,
                LocalDate.of(2026, 3, 30),
                LocalDate.of(2026, 3, 1),
                LocalDate.of(2026, 4, 1),
                LocalDate.of(2026, 4, 30));

        assertThrows(
                IllegalArgumentException.class,
                () -> service.cadastrar(edital));

        assertEquals(0, service.listar().size());
    }

    @Test
    void naoDeveCadastrarComDatasDeAvaliacaoInvalidas() {
        Edital edital = new Edital(
                "Edital inválido",
                4,
                2026,
                LocalDate.of(2026, 3, 1),
                LocalDate.of(2026, 3, 30),
                LocalDate.of(2026, 4, 30),
                LocalDate.of(2026, 4, 1));

        assertThrows(
                IllegalArgumentException.class,
                () -> service.cadastrar(edital));
    }

    @Test
    void naoDeveEditarEditalInexistente() {
        Edital novosDados = criarEdital();

        assertThrows(
                IllegalArgumentException.class,
                () -> service.editar(999, novosDados));
    }
}
