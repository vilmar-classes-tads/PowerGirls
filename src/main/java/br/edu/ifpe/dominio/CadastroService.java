package br.edu.ifpe.

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.regex.Pattern;

/** Serviço de cadastro com persistência simulada por Map em memória. */
public class CadastroService {
    private static final Pattern EMAIL_VALIDO = Pattern.compile("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$");
    private final Map<String, Usuario> usuariosPorCpf = new LinkedHashMap<>();
    private final Map<String, Usuario> usuariosPorEmail = new LinkedHashMap<>();

    public synchronized Usuario cadastrar(String nome, String cpf, String email, String senha) {
        if (nome == null || nome.isBlank()) throw new IllegalArgumentException("Nome é obrigatório.");
        String cpfNormalizado = normalizarCpf(cpf);
        String emailNormalizado = email == null ? "" : email.trim().toLowerCase();
        if (!cpfNormalizado.matches("\\d{11}")) throw new IllegalArgumentException("CPF deve conter 11 dígitos.");
        if (!EMAIL_VALIDO.matcher(emailNormalizado).matches()) throw new IllegalArgumentException("Informe um e-mail válido.");
        if (senha == null || senha.length() < 6) throw new IllegalArgumentException("A senha deve ter pelo menos 6 caracteres.");
        if (usuariosPorCpf.containsKey(cpfNormalizado)) throw new IllegalArgumentException("Este CPF já está cadastrado.");
        if (usuariosPorEmail.containsKey(emailNormalizado)) throw new IllegalArgumentException("Este e-mail institucional já cadastrado.");

        // A issue não exige autenticação real; não armazenamos a senha em texto puro.
        String hashSimulado = Integer.toHexString(senha.hashCode());
        Usuario usuario = new Usuario(nome.trim(), cpfNormalizado, emailNormalizado, hashSimulado);
        usuariosPorCpf.put(cpfNormalizado, usuario);
        usuariosPorEmail.put(emailNormalizado, usuario);
        return usuario;
    }

    public synchronized Usuario buscarPorCpf(String cpf) {
        return usuariosPorCpf.get(normalizarCpf(cpf));
    }

    public synchronized Usuario buscarPorEmail(String email) {
        return email == null ? null : usuariosPorEmail.get(email.trim().toLowerCase());
    }

    public synchronized int quantidadeUsuarios() { return usuariosPorCpf.size(); }

    public synchronized Map<String, Usuario> listarPorCpf() {
        return Collections.unmodifiableMap(new LinkedHashMap<>(usuariosPorCpf));
    }

    private static String normalizarCpf(String cpf) {
        return cpf == null ? "" : cpf.replaceAll("\\D", "");
    }
}
