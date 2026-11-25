package br.edu.ifpe.dominio;

public class Main {

    public static void main(String[] args) {

        EditalService editalService = new EditalService();

        System.out.println("================================");
        System.out.println("     SISTEMA DE EDITAIS");
        System.out.println("================================");
        System.out.println("Aplicacao iniciada com sucesso!");
        System.out.println("Servico de editais inicializado.");
        System.out.println("Editais cadastrados: " + editalService.listar().size());
    }
}
