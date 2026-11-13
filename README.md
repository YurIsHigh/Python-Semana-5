# Processador e Validador de Dados com Python

Este projeto realiza a leitura de arquivos CSV contendo informações cadastrais, faz a validação dos formatos através de **Expressões Regulares (Regex)**, gerencia falhas com **Tratamento de Exceções** e exibe um **Relatório Formatado** final.

---

## 1. Justificativa das Validações Regex Aplicadas

1. **E-mail (`validar_email`)**
   - **Padrão:** `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
   - **Explicação:**
     - `^` e `$`: Garantem que toda a string deve se ajustar ao padrão.
     - `[a-zA-Z0-9._%+-]+`: Permite caracteres alfanuméricos e símbolos comuns em nomes de usuário.
     - `@`: Caractere obrigatório divisor de domínio.
     - `\.[a-zA-Z]{2,}`: Valida a extensão do domínio (ex: `.com`, `.br`, `.edu.br`).

2. **CPF (`validar_cpf`)**
   - **Padrão:** `^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$`
   - **Explicação:**
     - `\d{3}`: Três dígitos numéricos.
     - `\.?`: Ponto opcional (aceita tanto com pontuação quanto apenas os números).
     - `-?`: Hífen opcional antes dos últimos dois dígitos verificadores.

3. **Telefone (`validar_telefone`)**
   - **Padrão:** `^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$`
   - **Explicação:**
     - `\(?\d{2}\)?`: DDD com parênteses opcionais.
     - `\s?`: Espaço em branco opcional.
     - `\d{4,5}-?\d{4}`: Aceita telefones fixos (4 dígitos iniciais) ou celulares (5 dígitos iniciais), com ou sem hífen.

4. **Data (`validar_data`)**
   - **Padrão Regex:** `^(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})$`
   - **Explicação:** Valida o formato textual em `DD/MM/AAAA` ou `AAAA-MM-DD`. Em seguida, utiliza `datetime.strptime` para garantir que a data existe no calendário (ex: rejeita `31/02/2026`).

---

## 2. Exceções Tratadas

- **`FileNotFoundError`**: Capturada no bloco `try` principal para evitar a interrupção do script caso o arquivo `dados.csv` informado não esteja no diretório.
- **`KeyError`**: Verificada ao conferir os nomes dos cabeçalhos do arquivo CSV. Caso alguma coluna obrigatória (`email`, `cpf`, `telefone`, `data`) esteja ausente, o erro é tratado amigavelmente.
- **`ValueError`**: Capturada para tratar possíveis erros de conversão de tipos de dados durante o processamento.
- **`FormatoInvalidoError` (Exceção Personalizada)**: Herda da classe base `Exception`. É utilizada para sinalizar registros que não obedeceram às regras de negócio das regexes.

---

## 3. Exemplo de Entrada e Saída

### Arquivo de Entrada (`dados.csv`)
```csv
email,cpf,telefone,data
joao.silva@example.com,123.456.789-00,(98) 98888-7777,10/11/2026
maria.erro@dominio,12345678900,98977776666,2026-05-15
carlos.souza@test.org,999.888.777-66,983232-1111,31/02/2026
