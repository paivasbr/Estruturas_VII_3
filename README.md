# Estruturas_VII_3
3º Relatório :books: :octocat:

## <h3 align="center"> Análise Dinâmica Implícita de uma Barra Bidimensional via Método de Newmark com Dois Elementos Finitos</h3>

**_Disciplina:_** Tópicos em Engenharia de Estruturas VII - Introdução à Análise Não Linear de Estruturas.

### **_Introdução_**

<p align="justify">A análise dinâmica de estruturas sujeitas a impacto é um tema fundamental na engenharia estrutural. Este trabalho visa aplicar o método dos elementos finitos na análise dinâmica implícita (Newmark-beta) considerando linearidade e, posteriormente, não linearidade física via método de Newton-Raphson.</p>

### **_Metodologia_**

#### **_Formulação Linear com 2 Elementos_**

 <p align="justify">Adaptou-se o algoritmo de Newmark implícito fornecido com um único elemento para uma malha com dois elementos finitos, aumentando assim a precisão da discretização espacial. As matrizes globais de rigidez e massa foram montadas a partir de suas versões locais, considerando condições de contorno fixas no nó 0.</p>
