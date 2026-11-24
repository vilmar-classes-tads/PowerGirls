package br.edu.ifpe.dominio;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class ProjetoTest {

    private Projeto criarProjeto() {
        return new Projeto(
                "Projeto de Extensão",
                "Descrição inicial do projeto.",
                List.of("Educação", "Tecnologia"),
                "Estudantes",
                "Educação",
                "Campus Recife",
                List.of(4, 10),
                true
        );
    }

    @Test
    void deveCriarProjetoComoRascunho() {
        Projeto projeto = criarProjeto();

        assertEquals(StatusProjeto.RASCUNHO, projeto.getStatus());
    }

    @Test
    void deveEditarProjetoEmRascunho() {
        Projeto projeto = criarProjeto();

        projeto.editarProjeto(
                "Novo título",
                "Novo resumo",
                List.of("Inclusão", "Ensino"),
                "Comunidade",
                "Direitos Humanos",
                "Campus Olinda",
                List.of(4, 5),
                true
        );

        assertEquals("Novo título", projeto.getTitulo());
        assertEquals("Novo resumo", projeto.getResumo());
        assertEquals("Campus Olinda", projeto.getCampus());
    }

    @Test
    void deveSubmeterProjetoComTermoAceito() {
        Projeto projeto = criarProjeto();

        projeto.submeter();

        assertEquals(StatusProjeto.SUBMETIDO, projeto.getStatus());
    }

    @Test
    void naoDeveSubmeterProjetoSemAceitarTermo() {
        Projeto projeto = new Projeto(
                "Projeto de Extensão",
                "Descrição inicial.",
                List.of("Educação"),
                "Estudantes",
                "Educação",
                "Campus Recife",
                List.of(4),
                false
        );

        assertThrows(
                IllegalStateException.class,
                projeto::submeter
        );

        assertEquals(StatusProjeto.RASCUNHO, projeto.getStatus());
    }

    @Test
    void naoDeveEditarProjetoSubmetido() {
        Projeto projeto = criarProjeto();

        projeto.submeter();

        assertThrows(
                IllegalStateException.class,
                () -> projeto.editarProjeto(
                        "Título alterado",
                        "Resumo alterado",
                        List.of("Tecnologia"),
                        "Estudantes",
                        "Educação",
                        "Campus Recife",
                        List.of(4),
                        true
                )
        );

        assertEquals("Projeto de Extensão", projeto.getTitulo());
    }

    @Test
    void devePermitirEditarProjetoEmCorrecao() {
        Projeto projeto = criarProjeto();

        projeto.submeter();
        projeto.enviarParaCorrecao();

        projeto.editarProjeto(
                "Projeto corrigido",
                "Resumo atualizado",
                List.of("Educação"),
                "Comunidade",
                "Educação",
                "Campus Recife",
                List.of(4, 10),
                true
        );

        assertEquals("Projeto corrigido", projeto.getTitulo());
        assertEquals(StatusProjeto.EM_CORRECAO, projeto.getStatus());
    }

    @Test
    void naoDeveEnviarProjetoEmRascunhoParaCorrecao() {
        Projeto projeto = criarProjeto();

        assertThrows(
                IllegalStateException.class,
                projeto::enviarParaCorrecao
        );
    }

    @Test
    void naoDeveCriarProjetoComPalavrasChaveNulas() {
        assertThrows(
                IllegalArgumentException.class,
                () -> new Projeto(
                        "Projeto de Extensão",
                        "Descrição inicial.",
                        null,
                        "Estudantes",
                        "Educação",
                        "Campus Recife",
                        List.of(4),
                        true
                )
        );
    }

    @Test
    void naoDeveCriarProjetoComOdsNulos() {
        assertThrows(
                IllegalArgumentException.class,
                () -> new Projeto(
                        "Projeto de Extensão",
                        "Descrição inicial.",
                        List.of("Educação"),
                        "Estudantes",
                        "Educação",
                        "Campus Recife",
                        null,
                        true
                )
        );
    }

    @Test
    void naoDeveSubmeterProjetoMaisDeUmaVez() {
        Projeto projeto = criarProjeto();

        projeto.submeter();

        assertThrows(
                IllegalStateException.class,
                projeto::submeter
        );

        assertEquals(StatusProjeto.SUBMETIDO, projeto.getStatus());
    }
}
