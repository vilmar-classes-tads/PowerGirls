
package br.edu.ifpe.dominio;

import java.util.ArrayList;
import java.util.List;

//Gerencia o cadastro, a edição, a listagem e a validação dos editais.
public class EditalService {

    private List<Edital> editais = new ArrayList<>();

    // Valida e adiciona um novo edital à lista.
    public void cadastrar(Edital edital) {
        validarDatas(edital);
        editais.add(edital);
    }

    // Localiza um edital pelo ID e atualiza seus dados.
    public void editar(int id, Edital novosDados) {

        validarDatas(novosDados);

        Edital editalEncontrado = buscarPorId(id);

        editalEncontrado.atualizar(
                novosDados.getTitulo(),
                novosDados.getNumero(),
                novosDados.getAno(),
                novosDados.getInicioSubmissao(),
                novosDados.getFimSubmissao(),
                novosDados.getInicioAvaliacao(),
                novosDados.getFimAvaliacao());
    }

    // Retorna uma cópia da lista de editais cadastrados.
    public List<Edital> listar() {
        return new ArrayList<>(editais);
    }

    private Edital buscarPorId(int id) {

        for (Edital edital : editais) {

            if (edital.getId() == id) {
                return edital;
            }
        }

        throw new IllegalArgumentException(
                "Edital não encontrado.");
    }

    // Verifica se as datas iniciais não são posteriores às finais.
    private void validarDatas(Edital edital) {

        if (edital.getInicioSubmissao()
                .isAfter(edital.getFimSubmissao())) {

            throw new IllegalArgumentException(
                    "O início da submissão não pode ser posterior ao fim.");
        }

        if (edital.getInicioAvaliacao()
                .isAfter(edital.getFimAvaliacao())) {

            throw new IllegalArgumentException(
                    "O início da avaliação não pode ser posterior ao fim.");
        }
    }
}
