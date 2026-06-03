# CraftScript

Linguagem de programação interpretada com temática **Minecraft**, desenvolvida como projeto de Analisador Léxico. O interpretador é escrito em Python puro e implementa todas as fases de compilação: análise léxica, sintática, semântica e execução.

---

## Sumário

- [Como rodar](#como-rodar)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Pipeline de execução](#pipeline-de-execução)
- [A linguagem CraftScript](#a-linguagem-craftscript)
  - [Tipos de dados](#tipos-de-dados)
  - [Declaração de variáveis](#declaração-de-variáveis)
  - [Operadores](#operadores)
  - [Entrada e saída](#entrada-e-saída)
  - [Condicionais](#condicionais)
  - [Laços](#laços)
  - [Funções](#funções)
- [Exemplos](#exemplos)
- [Erros comuns](#erros-comuns)

---

## Como rodar

**Requisito:** Python 3.8 ou superior.

```bash
# Clone o repositório (ou abra a pasta no VS Code)
cd CraftScript

# Execute o interpretador
py main.py
```

O interpretador lê o arquivo `teste.craft` por padrão. Para testar outro arquivo, altere a linha no `main.py`:

```python
with open("meu_programa.craft", "r", encoding="utf-8") as f:
```

---

## Estrutura do projeto

```
CraftScript/
│
├── main.py                  # Ponto de entrada — orquestra todas as fases
│
├── lexer/
│   ├── lexer.py             # Analisador léxico (tokenizador)
│   ├── token.py             # Classe Token
│   └── token_type.py        # Enumeração de todos os tipos de token
│
├── parser/
│   └── parser.py            # Analisador sintático (parser recursivo descendente)
│
├── nodes/
│   └── nodes.py             # Classes dos nós da AST (Árvore Sintática Abstrata)
│
├── semantic/
│   └── semantic.py          # Analisador semântico + tabela de símbolos
│
├── interpreter/
│   └── interpreter.py       # Interpretador (executa a AST)
│
└── teste.craft              # Programa de exemplo escrito em CraftScript
```

---

## Pipeline de execução

Quando você roda `py main.py`, o código do arquivo `.craft` passa por quatro fases em sequência:

```
Código-fonte (.craft)
        │
        ▼
┌───────────────┐
│  1. LÉXICO    │  Transforma o texto em tokens (unidades mínimas de significado)
│   lexer.py    │  Ex: "bloco pedra x = 10;" → [BLOCO, PEDRA, ID("x"), ATRIB, INT(10), PONTO_VIRG]
└──────┬────────┘
       │
       ▼
┌───────────────┐
│  2. SINTÁTICO │  Verifica a gramática e monta a Árvore Sintática Abstrata (AST)
│   parser.py   │  Ex: Declaration(tipo="pedra", nome="x", valor=Literal(10))
└──────┬────────┘
       │
       ▼
┌───────────────┐
│  3. SEMÂNTICO │  Valida tipos, verifica declarações e constrói tabela de símbolos
│  semantic.py  │  Ex: erro se tentar somar "pedra" com "fumaca"
└──────┬────────┘
       │
       ▼
┌───────────────┐
│  4. EXECUÇÃO  │  Percorre a AST e executa cada nó
│interpreter.py │  Ex: variaveis["x"] = 10
└───────────────┘
```

### Fase 1 — Léxico

O `Lexer` lê o código caractere por caractere e agrupa em tokens. Cada token tem um **tipo** (`TokenType`) e um **valor**.

Entrada:
```
bloco pedra vida = 10;
```

Tokens gerados:
```
BLOCO    → "bloco"
PEDRA    → "pedra"
ID       → "vida"
ATRIB    → "="
INT      → 10
PONTO_VIRG → ";"
```

### Fase 2 — Sintático

O `Parser` consome os tokens e verifica se seguem as **regras gramaticais** da linguagem. Se a ordem estiver errada, lança um erro com linha e coluna. Se estiver correta, monta a AST.

Entrada (tokens) → Saída (AST):
```
Declaration(
  tipo  = "pedra",
  nome  = "vida",
  valor = Literal(10)
)
```

### Fase 3 — Semântico

O `Semantico` percorre a AST e valida regras que a gramática não consegue verificar:

- Variável usada antes de ser declarada
- Tipo incompatível na atribuição (`bloco pedra x = "texto"` → erro)
- `dropar` (return) fora de uma função
- Chamar algo que não é função

Ao final de cada escopo, imprime a **tabela de símbolos**:

```
=== Escopo: global ===
  vida: tipo=pedra, categoria=var
  soma: tipo=funcao, categoria=func
  x:    tipo=pedra, categoria=var
```

### Fase 4 — Execução

O `Interpreter` usa o padrão **Visitor**: para cada tipo de nó da AST existe um método `visitar_NomeDoNo()`. Ele percorre a árvore e executa cada instrução.

---

## A linguagem CraftScript

Todo programa CraftScript começa com `mundo { }`:

```
mundo {
    // seu código aqui
}
```

### Tipos de dados

| Tipo CraftScript | Equivalente | Exemplo de valor |
|---|---|---|
| `pedra` | inteiro (`int`) | `10`, `-3`, `0` |
| `liquido` | decimal (`float`) | `3.14`, `0.5` |
| `fumaca` | texto (`string`) | `"Olá, mundo!"` |
| `bandeira` | booleano (`bool`) | `verdadeiro`, `falso` |
| `vazio` | sem retorno (`void`) | usado em funções |

### Declaração de variáveis

Sintaxe: `bloco <tipo> <nome> = <valor>;`

```
bloco pedra    quantidade = 64;
bloco liquido  preco      = 9.99;
bloco fumaca   jogador    = "Steve";
bloco bandeira ativo      = verdadeiro;
```

### Operadores

**Aritméticos:**
```
bloco pedra soma  = 5 + 3;   // 8
bloco pedra diff  = 10 - 4;  // 6
bloco pedra prod  = 3 * 4;   // 12
bloco liquido div = 7 / 2;   // 3.5
bloco pedra mod   = 10 % 3;  // 1
```

**Relacionais** (resultado é `bandeira`):
```
bloco bandeira maior   = 10 > 5;   // verdadeiro
bloco bandeira menor   = 3 < 1;    // falso
bloco bandeira igual   = 4 == 4;   // verdadeiro
bloco bandeira diferente = 4 != 5; // verdadeiro
```

**Lógicos** (operam em `bandeira`):
```
bloco bandeira e  = verdadeiro && falso;  // falso
bloco bandeira ou = verdadeiro || falso;  // verdadeiro
bloco bandeira n  = !verdadeiro;          // falso
```

**Concatenação de texto** (com `+`):
```
bloco fumaca nome = "Steve";
bloco fumaca msg  = "Jogador: " + nome;  // "Jogador: Steve"
```

### Entrada e saída

**Saída** — `mostrar`:
```
mostrar("Olá, mundo!");
mostrar("Valor:", x, "unidades");
```

**Entrada** — `coletar` (a variável deve ser declarada antes):
```
bloco fumaca nome = "";
coletar(nome);
mostrar("Bem-vindo,", nome);
```

### Condicionais

```
seVida(x > 0) {
    mostrar("positivo");
}

seVida(x > 0) {
    mostrar("positivo");
} senao {
    mostrar("zero ou negativo");
}
```

### Laços

**While** — `mina`:
```
bloco pedra i = 0;

mina(i < 5) {
    mostrar(i);
    i = i + 1;
}
```

**For** — `craftar`:
```
craftar(i = 0; i < 5; i = i + 1) {
    mostrar(i);
}
```

> No `craftar`, a variável de controle deve ser declarada antes do laço.

### Funções

Sintaxe: `spawnar <tipo_retorno> <nome>(<param1>, <param2>) { ... dropar <valor>; }`

```
spawnar pedra somar(a, b) {
    dropar a + b;
}

bloco pedra resultado = somar(10, 5);
mostrar("Resultado:", resultado);  // 15
```

Função sem retorno:
```
spawnar vazio saudar(nome) {
    mostrar("Olá,", nome);
}

saudar("Alex");
```

---

## Exemplos

### Exemplo completo

```
mundo {

    // Declarações
    bloco pedra  vida    = 100;
    bloco fumaca jogador = "Steve";

    mostrar("Jogador:", jogador);
    mostrar("Vida inicial:", vida);

    // Função
    spawnar pedra dano(base, critico) {
        dropar base + critico;
    }

    // Condicional
    bloco pedra ataque = dano(15, 5);

    seVida(ataque > 10) {
        mostrar("Ataque forte:", ataque);
    } senao {
        mostrar("Ataque fraco:", ataque);
    }

    // Laço
    bloco pedra i = 0;

    mina(i < 3) {
        vida = vida - ataque;
        mostrar("Vida restante:", vida);
        i = i + 1;
    }

    // Input
    bloco fumaca nome = "";
    coletar(nome);
    mostrar("Novo jogador:", nome);
}
```

---

## Erros comuns

| Erro | Causa | Correção |
|---|---|---|
| `Esperado X mas encontrou Y` | Erro de sintaxe — token fora de ordem | Verifique `;`, `{`, `)` faltando |
| `'x' não foi declarado antes do uso` | Variável usada sem `bloco` | Declarar com `bloco tipo x = valor;` |
| `'x' já foi declarado neste escopo` | Declaração duplicada | Remover a segunda declaração |
| `tipo declarado 'pedra' incompatível com 'fumaca'` | Tipo errado na atribuição | Usar o tipo correto ou converter |
| `'dropar' usado fora de uma função` | Return fora de `spawnar` | Mover o `dropar` para dentro da função |
| `Float inválido` | Número com dois pontos (ex: `3.1.4`) | Corrigir o número |
