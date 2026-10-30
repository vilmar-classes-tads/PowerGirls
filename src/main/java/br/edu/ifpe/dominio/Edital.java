
package br.edu.ifpe.dominio;

import java.time.LocalDate;



//Representa um edital e armazena suas informações.
public class Edital {

    private final int id;
    private static int proximoId = 1;

    private String titulo;
    private int numero;
    private int ano;

    private LocalDate inicioSubmissao;
    private LocalDate fimSubmissao;

    private LocalDate inicioAvaliacao;
    private LocalDate fimAvaliacao;

    // Cria um edital e gera seu identificador automaticamente.
    public Edital(String titulo, int numero, int ano,
            LocalDate inicioSubmissao, LocalDate fimSubmissao,
            LocalDate inicioAvaliacao, LocalDate fimAvaliacao) {

        this.id = proximoId++;

        this.titulo = titulo;
        this.numero = numero;
        this.ano = ano;
        this.inicioSubmissao = inicioSubmissao;
        this.fimSubmissao = fimSubmissao;
        this.inicioAvaliacao = inicioAvaliacao;
        this.fimAvaliacao = fimAvaliacao;
    }

    public int getId() {
        return id;
    }

    public String getTitulo() {
        return titulo;
    }

    public int getNumero() {
        return numero;
    }

    public int getAno() {
        return ano;
    }

    public LocalDate getInicioSubmissao() {
        return inicioSubmissao;
    }

    public LocalDate getFimSubmissao() {
        return fimSubmissao;
    }

    public LocalDate getInicioAvaliacao() {
        return inicioAvaliacao;
    }

    public LocalDate getFimAvaliacao() {
        return fimAvaliacao;
    }

    public void atualizar(String titulo, int numero, int ano,
            LocalDate inicioSubmissao, LocalDate fimSubmissao,
            LocalDate inicioAvaliacao, LocalDate fimAvaliacao) {

        this.titulo = titulo;
        this.numero = numero;
        this.ano = ano;
        this.inicioSubmissao = inicioSubmissao;
        this.fimSubmissao = fimSubmissao;
        this.inicioAvaliacao = inicioAvaliacao;
        this.fimAvaliacao = fimAvaliacao;
    }
}
