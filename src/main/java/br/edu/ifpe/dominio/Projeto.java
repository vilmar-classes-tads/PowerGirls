package br.edu.ifpe.dominio;

import java.util.List;

public class Projeto {

    private String titulo;
    private String resumo;
    private List<String> palavrasChave;
    private String publicoAlvo;
    private String areaTematica;
    private String campus;
    private List<Integer> ods;
    private boolean termoCompromissoAceito;
    private StatusProjeto status;

    public Projeto(
            String titulo,
            String resumo,
            List<String> palavrasChave,
            String publicoAlvo,
            String areaTematica,
            String campus,
            List<Integer> ods,
            boolean termoCompromissoAceito
    ) {
        this.status = StatusProjeto.RASCUNHO;

        editarProjeto(
                titulo,
                resumo,
                palavrasChave,
                publicoAlvo,
                areaTematica,
                campus,
                ods,
                termoCompromissoAceito
        );
    }

    public void editarProjeto(
            String titulo,
            String resumo,
            List<String> palavrasChave,
            String publicoAlvo,
            String areaTematica,
            String campus,
            List<Integer> ods,
            boolean termoCompromissoAceito
    ) {
        if (status != StatusProjeto.RASCUNHO
                && status != StatusProjeto.EM_CORRECAO) {
            throw new IllegalStateException(
                    "Não é permitido editar um projeto submetido."
            );
        }

        this.titulo = exigirTexto(titulo, "Título");
        this.resumo = exigirTexto(resumo, "Resumo");
        this.palavrasChave = copiarLista(palavrasChave, "Palavras-chave");
        this.publicoAlvo = exigirTexto(publicoAlvo, "Público-alvo");
        this.areaTematica = exigirTexto(areaTematica, "Área temática");
        this.campus = exigirTexto(campus, "Campus");
        this.ods = copiarLista(ods, "ODS");
        this.termoCompromissoAceito = termoCompromissoAceito;
    }

    public void submeter() {
        if (status != StatusProjeto.RASCUNHO
                && status != StatusProjeto.EM_CORRECAO) {
            throw new IllegalStateException(
                    "Somente projetos em rascunho ou correção podem ser submetidos."
            );
        }

        if (!termoCompromissoAceito) {
            throw new IllegalStateException(
                    "É necessário aceitar o Termo de Compromisso."
            );
        }

        status = StatusProjeto.SUBMETIDO;
    }

    public void enviarParaCorrecao() {
        if (status != StatusProjeto.SUBMETIDO) {
            throw new IllegalStateException(
                    "Somente projetos submetidos podem entrar em correção."
            );
        }

        status = StatusProjeto.EM_CORRECAO;
    }

    private String exigirTexto(String valor, String campo) {
        if (valor == null || valor.isBlank()) {
            throw new IllegalArgumentException(
                    campo + " é obrigatório."
            );
        }

        return valor.trim();
    }

    private <T> List<T> copiarLista(List<T> lista, String campo) {
        if (lista == null) {
            throw new IllegalArgumentException(
                    campo + " não pode ser nulo."
            );
        }

        return List.copyOf(lista);
    }

    public String getTitulo() { return titulo; }
    public String getResumo() { return resumo; }
    public List<String> getPalavrasChave() { return palavrasChave; }
    public String getPublicoAlvo() { return publicoAlvo; }
    public String getAreaTematica() { return areaTematica; }
    public String getCampus() { return campus; }
    public List<Integer> getOds() { return ods; }
    public boolean isTermoCompromissoAceito() {
        return termoCompromissoAceito;
    }
    public StatusProjeto getStatus() { return status; }
}
