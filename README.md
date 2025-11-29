Este repositório documenta o projeto prático desenvolvido para a disciplina de **Matemática Discreta**. O objetivo central é demonstrar a aplicação de conceitos de **Teoria dos Grafos** e **Álgebra Linear** na análise de dados reais, focando especificamente na modelagem de redes bipartidas e sua projeção através de operações matriciais.

---


## Fundamentação Matemática

O núcleo do projeto baseia-se na manipulação da **Matriz de Incidência ($A$)** para realizar projeções de grafos:

$$A = \text{Matriz de Incidência (Alunos} \times \text{Tecnologias)}$$

As projeções são obtidas pelas seguintes operações de Álgebra Linear:

**Matriz de Similaridade (Rede de Alunos):**
    $$M_{sim} = A \times A^T$$
    *Representa o número de nós vizinhos compartilhados entre dois alunos.*

**Matriz de Coocorrência (Rede de Tecnologias):**
    $$M_{cooc} = A^T \times A$$
    *Representa a frequência com que duas tecnologias compartilham a mesma aresta de origem.*

---

## Como Executar

1. Clone este repositório:
    ```bash
    git clone https://github.com/polianarodz/bipartite-matrix-projections.git
    cd bipartite-matrix-projections
    ```
2.  instale as dependencias:
    ```bash
    pip install pandas numpy networkx matplotlib
    ```
3.  Execute o script principal. (`python trabalho.py`)
4.  Os grafos gerados e as métricas serão salvos na pasta `/resultados`.

---
*Desenvolvido para fins educacionais.*
