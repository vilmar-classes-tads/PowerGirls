package br.edu.ifpe.dominio;

import java.util.Collections;
import java.util.EnumSet;
import java.util.Set;

/** Entidade de domínio que representa um usuário cadastrado. */
public class Usuario {
    private final String nome;
    private final String cpf;
    private final String email;
    private final String senhaHash;
    private final Set<Perfil> perfis;

    public Usuario(String nome, String cpf, String email, String senhaHash) {
        this(nome, cpf, email, senhaHash, EnumSet.of(Perfil.ROLE_COORDENADOR, Perfil.ROLE_AVALIADOR));
    }

    public Usuario(String nome, String cpf, String email, String senhaHash, Set<Perfil> perfis) {
        this.nome = exigirTexto(nome, "Nome");
        this.cpf = exigirTexto(cpf, "CPF");
        this.email = exigirTexto(email, "E-mail").toLowerCase();
        this.senhaHash = exigirTexto(senhaHash, "Hash da senha");
        if (perfis == null || perfis.isEmpty()) {
            throw new IllegalArgumentException("O usuário deve possuir ao menos um perfil.");
        }
        this.perfis = Collections.unmodifiableSet(EnumSet.copyOf(perfis));
    }

    private static String exigirTexto(String valor, String campo) {
        if (valor == null || valor.isBlank()) throw new IllegalArgumentException(campo + " é obrigatório.");
        return valor.trim();
    }

    public String getNome() { return nome; }
    public String getCpf() { return cpf; }
    public String getEmail() { return email; }
    public String getSenhaHash() { return senhaHash; }
    public Set<Perfil> getPerfis() { return perfis; }
}
