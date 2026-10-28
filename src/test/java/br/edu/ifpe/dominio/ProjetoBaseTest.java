package br.edu.ifpe.dominio;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

class ProjetoBaseTest {
    @Test
    void deveIndicarQueEstruturaFoiInicializada() {
        assertEquals("estrutura Maven inicializada", ProjetoBase.status());
    }
}
