package br.edu.ifpe.dominio;

import java.util.Collections;
import java.util.LinkedHashSet;
import java.util.Set;

public final class Usuario {
    private final String nomeCompleto, cpf, emailInstitucional, senhaHash, campus, areaFormacao, titulacao;
    private final String nomeSocial, linkLattes, telefone;
    private final Sexo sexo;
    private final Set<Perfil> perfis;

    public Usuario(String nomeCompleto, String cpf, String emailInstitucional, String senhaHash,
                   String campus, String areaFormacao, String titulacao, String nomeSocial,
                   Sexo sexo, String linkLattes, String telefone, Set<Perfil> perfis) {
        this.nomeCompleto = nomeCompleto; this.cpf = cpf; this.emailInstitucional = emailInstitucional;
        this.senhaHash = senhaHash; this.campus = campus; this.areaFormacao = areaFormacao;
        this.titulacao = titulacao; this.nomeSocial = nomeSocial; this.sexo = sexo;
        this.linkLattes = linkLattes; this.telefone = telefone;
        this.perfis = Collections.unmodifiableSet(new LinkedHashSet<>(perfis));
    }
    public String getNomeCompleto() { return nomeCompleto; }
    public String getCpf() { return cpf; }
    public String getEmailInstitucional() { return emailInstitucional; }
    public String getSenhaHash() { return senhaHash; }
    public String getCampus() { return campus; }
    public String getAreaFormacao() { return areaFormacao; }
    public String getTitulacao() { return titulacao; }
    public String getNomeSocial() { return nomeSocial; }
    public Sexo getSexo() { return sexo; }
    public String getLinkLattes() { return linkLattes; }
    public String getTelefone() { return telefone; }
    public Set<Perfil> getPerfis() { return perfis; }
}
