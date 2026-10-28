package br.edu.ifpe.dominio;

import java.util.Objects;

public final class Perfil {
    private final String nome;

    public Perfil(String nome) {
        if (nome == null || nome.isBlank()) throw new IllegalArgumentException("O nome do perfil é obrigatório.");
        this.nome = nome.trim();
    }

    public String getNome() { return nome; }
    @Override public boolean equals(Object obj) { return this == obj || obj instanceof Perfil p && nome.equals(p.nome); }
    @Override public int hashCode() { return Objects.hash(nome); }
    @Override public String toString() { return nome; }
}
