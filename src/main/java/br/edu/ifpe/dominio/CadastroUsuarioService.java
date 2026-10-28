package br.edu.ifpe.dominio;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.regex.Pattern;

/** Serviço de cadastro em memória para a Issue 0. Os dados não persistem após encerrar o programa. */
public class CadastroUsuarioService {
    private static final Pattern EMAIL_PATTERN = Pattern.compile("^[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}$", Pattern.CASE_INSENSITIVE);
    private final Map<String, Usuario> usuariosPorCpf = new LinkedHashMap<>();
    private final Map<String, Usuario> usuariosPorEmail = new LinkedHashMap<>();
    private final PasswordEncoder passwordEncoder;

    public CadastroUsuarioService() { this(new BCryptPasswordEncoder()); }
    public CadastroUsuarioService(PasswordEncoder passwordEncoder) {
        if (passwordEncoder == null) throw new IllegalArgumentException("O codificador de senha é obrigatório.");
        this.passwordEncoder = passwordEncoder;
    }

    public synchronized Usuario cadastrar(DadosCadastro dados) {
        validarCamposObrigatorios(dados);
        String cpf = normalizarCpf(dados.cpf());
        String email = normalizarEmail(dados.emailInstitucional());
        if (!cpfValido(cpf)) throw new IllegalArgumentException("CPF inválido.");
        if (!EMAIL_PATTERN.matcher(email).matches()) throw new IllegalArgumentException("E-mail institucional inválido.");
        if (dados.senha().length() < 6) throw new IllegalArgumentException("A senha deve ter pelo menos 6 caracteres.");
        if (usuariosPorCpf.containsKey(cpf)) throw new IllegalArgumentException("Já existe um usuário cadastrado com este CPF.");
        if (usuariosPorEmail.containsKey(email)) throw new IllegalArgumentException("Já existe um usuário cadastrado com este e-mail institucional.");

        Set<Perfil> perfis = new LinkedHashSet<>();
        perfis.add(new Perfil("ROLE_COORDENADOR"));
        perfis.add(new Perfil("ROLE_AVALIADOR"));
        Usuario usuario = new Usuario(dados.nomeCompleto().trim(), cpf, email,
                passwordEncoder.encode(dados.senha()), dados.campus().trim(), dados.areaFormacao().trim(),
                dados.titulacao().trim(), limparOpcional(dados.nomeSocial()), dados.sexo(),
                limparOpcional(dados.linkLattes()), limparOpcional(dados.telefone()), perfis);
        usuariosPorCpf.put(cpf, usuario);
        usuariosPorEmail.put(email, usuario);
        return usuario;
    }

    public synchronized Optional<Usuario> buscarPorCpf(String cpf) { return Optional.ofNullable(usuariosPorCpf.get(normalizarCpf(cpf))); }
    public synchronized Optional<Usuario> buscarPorEmail(String email) { return Optional.ofNullable(usuariosPorEmail.get(normalizarEmail(email))); }
    public synchronized int quantidadeUsuarios() { return usuariosPorCpf.size(); }

    private void validarCamposObrigatorios(DadosCadastro d) {
        if (d == null) throw new IllegalArgumentException("Os dados do cadastro são obrigatórios.");
        exigirTexto(d.nomeCompleto(), "Nome completo"); exigirTexto(d.cpf(), "CPF");
        exigirTexto(d.emailInstitucional(), "E-mail institucional"); exigirTexto(d.senha(), "Senha");
        exigirTexto(d.campus(), "Campus"); exigirTexto(d.areaFormacao(), "Área de formação");
        exigirTexto(d.titulacao(), "Titulação");
    }
    private void exigirTexto(String valor, String campo) {
        if (valor == null || valor.isBlank()) throw new IllegalArgumentException("O campo " + campo + " é obrigatório.");
    }
    private String normalizarCpf(String cpf) { return cpf == null ? "" : cpf.replaceAll("\\D", ""); }
    private String normalizarEmail(String email) { return email == null ? "" : email.trim().toLowerCase(Locale.ROOT); }
    private String limparOpcional(String valor) { return valor == null || valor.isBlank() ? null : valor.trim(); }

    private boolean cpfValido(String cpf) {
        if (cpf == null || !cpf.matches("\\d{11}") || cpf.chars().distinct().count() == 1) return false;
        int primeiro = calcularDigito(cpf, 9);
        int segundo = calcularDigito(cpf, 10);
        return cpf.charAt(9) - '0' == primeiro && cpf.charAt(10) - '0' == segundo;
    }
    private int calcularDigito(String cpf, int quantidade) {
        int soma = 0;
        for (int i = 0; i < quantidade; i++) soma += (cpf.charAt(i) - '0') * (quantidade + 1 - i);
        int resto = soma % 11;
        return resto < 2 ? 0 : 11 - resto;
    }

    public record DadosCadastro(String nomeCompleto, String cpf, String emailInstitucional, String senha,
            String campus, String areaFormacao, String titulacao, String nomeSocial, Sexo sexo,
            String linkLattes, String telefone) { }
}
