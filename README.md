# SAT Solver

## Visão Geral

Este projeto implementa um solver de SAT (Satisfatibilidade) utilizando o algoritmo **DPLL (Davis-Putnam-Logemann-Loveland)**. O programa lê fórmulas Booleanas no formato **DIMACS CNF** e determina se a fórmula é satisfatível (SAT) ou insatisfatível (UNSAT). Se a fórmula for satisfatível, ele gera uma atribuição de valores de verdade que satisfaz a fórmula.

## Funcionalidades

- **Suporte ao formato DIMACS CNF**: As fórmulas Booleanas de entrada devem ser fornecidas nesse formato padrão.
- **Algoritmo DPLL**: Implementa o algoritmo recursivo DPLL para resolver o problema SAT.
- **Simplificações**:
  1. Eliminação de cláusulas duplicadas.
  2. Eliminação de literais puros.
  3. Resolução de literais simples.
  4. Eliminação de literais opostos.
- **Heurísticas**:
  - Utiliza a heurística **MOM (Máximo número de Ocorrências em cláusulas de Mínimo comprimento)** para seleção de literais, melhorando o desempenho.


## Uso

1. Certifique-se de que seu arquivo de entrada CNF está no **formato DIMACS**.
2. Execute o programa com o seguinte comando:

```bash
python sat_solver.py <arquivo_de_entrada.cnf>
```

O solver exibirá o resultado da seguinte forma:
- **SAT**: Se a fórmula for satisfatível, e exibirá uma atribuição válida de valores de verdade aos literais.
- **UNSAT**: Se a fórmula for insatisfatível.

O programa irá gerar um arquivo de saída com o mesmo nome do arquivo de entrada, mas com a extensão `.res`.

### Exemplo de Execução

Se você tem um arquivo `exemplo.cnf` no formato DIMACS, pode executá-lo com o seguinte comando:

```bash
python sat_solver.py exemplo.cnf
```
A saída será exibida no terminal e salva em `exemplo.res`. Se a fórmula for satisfatível, o conteúdo do arquivo `.res` será algo como:

```bash
SAT
1 -2 3 0
```

Isso significa que:
- O literal `1` é verdadeiro,
- O literal `2` é falso,
- O literal `3` é verdadeiro,
- O `0` no final indica o término da lista de literais.

Se a fórmula for insatisfatível, o arquivo conterá apenas a palavra `UNSAT`.

### Formato de Entrada (DIMACS CNF)

O formato esperado para o arquivo de entrada segue o padrão **DIMACS CNF**, que é amplamente utilizado para representar problemas de satisfatibilidade Booleana. O formato é simples e consiste em:

- **Linhas começando com `c`**: Comentários (são ignorados pelo solver).
- **Linhas começando com `p`**: Especificações do problema. Por exemplo: `p cnf 3 4` significa que há 3 literais e 4 cláusulas.
- **Cláusulas**: Cada linha contém uma cláusula representada por uma lista de inteiros (positivos para literais e negativos para suas negações). As cláusulas são finalizadas com o número `0`.

#### Exemplo de Arquivo DIMACS

Um exemplo simples de arquivo DIMACS CNF (`exemplo.cnf`):

```bash
c Exemplo de um problema SAT
p cnf 3 3
1 -3 0
2 3 -1 0
-2 0
```


Neste exemplo:
- A primeira linha é um comentário.
- A segunda linha indica que temos 3 literais e 3 cláusulas.
- As três linhas seguintes representam as cláusulas do problema.

## Autores

- **Julia Retore**
- **Lucas Thomas**

## Licença

Este projeto é licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.
