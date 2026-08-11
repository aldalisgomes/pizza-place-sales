Pizza Place Sales — Modelagem, Ingestão e Análise de Dados

Visão Geral do Projeto
Este estudo de caso aborda o pipeline de dados da fictícia **Pizza Place**, desde a extração de dados denormalizados até o suporte à tomada de decisão.

O objetivo foi reestruturar uma base de dados relacional que apresentava problemas de redundância e anomalias de atualização, aplicando as **Formas Normais (1FN e 3FN)**, automatizando a carga de dados no **SQL Server** via **Python** e extraindo informações  de negócio utilizando **T-SQL**.

---
Tecnologias Utilizadas

* **Linguagem / Bibliotecas:** Python (Pandas, SQLAlchemy, PyODBC)
* **Banco de Dados:** SQL Server (T-SQL)
* **Containerização:** Docker & Docker Compose
* **IDE / Ferramentas:** VS Code (Extensions: SQL Server, Python)
* **Modelagem de Dados:** Lucidchart (Notações Peter Chen e Crow's Foot)
* **Controle de Versão:** Git & GitHub

---

Arquitetura do Banco & Modelagem ER

Governança e Qualidade de Dados
Foi desenvolvido um **Dicionário de Dados**  para a modelagem física, garantindo a integridade do banco através de Constraints:
* **Primary Keys (PK) e Foreign Keys (FK):** Para garantir o relacionamento correto entre os pedidos, pizzas, categorias e ingredientes.
* **CHECK Constraints:** Para as regras de negócio no banco (ex: `price > 0`, `quantity > 0`, validação do ano limite em `date` e padronização dos tamanhos `IN ('S', 'M', 'L', 'XL', 'XXL')`).

Processo de Normalização
1. **Primeira Forma Normal (1FN):** A coluna de ingredientes continha múltiplos valores separados por vírgula no arquivo de origem. Foi feita a decomposição desses valores e a criação da tabela associativa `pizza_type_ingredients`.
2. **Terceira Forma Normal (3FN):** As categorias das pizzas estavam armazenadas de forma redundante como texto na tabela de tipos. Foram isoladas em uma nova tabela dimensão chamada `categories` com identificador numérico único.
3. **Regras de Negócio Aplicadas via Python:**
   * Adição de *Mozzarella Cheese* em pizzas que não contavam com queijo.
   * Adição de *Tomato Sauce* como padrão para receitas sem molho específico.



Esquema Relacional (Diagrama ER)

```text
[ categories ]
      │ (1)
      │
      └───────< (N) [ pizza_types ] ───(1)───────< (N) [ pizzas ]
                         │                                  │ (1)
                         │ (1)                              │
                         │                                  └───────< (N) [ order_details ]
                         └───────< (N)                                         │ (N)
                                    [ pizza_type_ingredients ]                 │
                         ┌───────< (N)                                         │
                         │ (1)                                                 │ (1)
                  [ ingredients ]                                         [ orders ]
