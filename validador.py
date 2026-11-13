import csv
from datetime import datetime
import re

# Exceção Personalizada

class FormatoInvalidoError(Exception):
    """Exceção lançada quando um campo não cumpre o padrão regex estabelecido."""
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        super().__init__(f"Valor '{valor}' é inválido para o campo '{campo}'.")

# Funções de Validação com Regex

def validar_email(email: str) -> bool:
    """Valida emails no formato usuario@dominio.extensao."""
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(padrao, email.strip()))

def validar_cpf(cpf: str) -> bool:
    """Valida CPFs nos formatos: 123.456.789-00 ou 12345678900."""
    padrao = r"^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$"
    return bool(re.match(padrao, cpf.strip()))

def validar_telefone(telefone: str) -> bool:
    """Valida telefones nos formatos: (98) 98765-4321, 98987654321, (98)3456-7890."""
    padrao = r"^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$"
    return bool(re.match(padrao, telefone.strip()))

def validar_data(data_str: str) -> bool:
    """Valida datas nos formatos DD/MM/AAAA ou AAAA-MM-DD com verificação de valores válidos."""
    padrao = r"^(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})$"
    if not re.match(padrao, data_str.strip()):
        return False
    
    # Validação lógica de data (ex: evita 31/02/2026)
    for formato in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            datetime.strptime(data_str.strip(), formato)
            return True
        except ValueError:
            pass
    return False

# Processamento de Arquivo e Relatório
def processar_arquivo_dados(caminho_arquivo: str) -> None:
    registros_validos = []
    registros_invalidos = []
    total_registros = 0

    print(f"--- Iniciando leitura do arquivo: {caminho_arquivo} ---")
    
    try:
        with open(caminho_arquivo, mode="r", encoding="utf-8") as arquivo:
            leitor_csv = csv.DictReader(arquivo)
            
            # Verificação prévia de colunas (Gera KeyError se faltar alguma)
            colunas_esperadas = {"email", "cpf", "telefone", "data"}
            colunas_existentes = set(leitor_csv.fieldnames or [])
            colunas_faltantes = colunas_esperadas - colunas_existentes
            
            if colunas_faltantes:
                raise KeyError(f"Coluna(s) ausente(s) no cabeçalho CSV: {', '.join(colunas_faltantes)}")

            for numero_linha, linha in enumerate(leitor_csv, start=2):
                total_registros += 1
                erros_linha = []

                # Validação de cada campo
                if not validar_email(linha["email"]):
                    erros_linha.append("E-mail inválido")
                if not validar_cpf(linha["cpf"]):
                    erros_linha.append("CPF inválido")
                if not validar_telefone(linha["telefone"]):
                    erros_linha.append("Telefone inválido")
                if not validar_data(linha["data"]):
                    erros_linha.append("Data inválida")

                # Se houver inconsistências, lança a exceção personalizada para registrar
                try:
                    if erros_linha:
                        raise FormatoInvalidoError(
                            campo="Múltiplos campos",
                            valor=" | ".join(erros_linha)
                        )
                    else:
                        registros_validos.append(linha)
                except FormatoInvalidoError as e:
                    registros_invalidos.append({
                        "linha": numero_linha,
                        "dados": linha,
                        "motivo": e.valor
                    })

    except FileNotFoundError:
        print(f"\n[ERRO CRÍTICO] O arquivo '{caminho_arquivo}' não foi encontrado.")
    except KeyError as e:
        print(f"\n[ERRO DE ESTRUTURA] {e}")
    except ValueError as e:
        print(f"\n[ERRO DE VALOR] Falha ao converter tipo de dado: {e}")
    except Exception as e:
        print(f"\n[ERRO INESPERADO] {e}")
    else:
        # Executado apenas se a leitura/processamento do arquivo ocorrer sem exceções de I/O ou estrutura
        gerar_relatorio(total_registros, registros_validos, registros_invalidos)
    finally:
        print("\n--- Processamento finalizado ---")


def gerar_relatorio(total: int, validos: list, invalidos: list) -> None:
    taxa_sucesso = (len(validos) / total * 100) if total > 0 else 0.0

    print("\n" + "="*50)
    print(f"{'RELATÓRIO DE PROCESSAMENTO DE DADOS':^50}")
    print("="*50)
    print(f"Total de registros analisados : {total}")
    print(f"Registros VÁLIDOS             : {len(validos)} ({taxa_sucesso:.1f}%)")
    print(f"Registros INVÁLIDOS           : {len(invalidos)} ({100 - taxa_sucesso:.1f}%)")
    print("-" * 50)

    if validos:
        print("\n[REGISTROS VÁLIDOS]:")
        for reg in validos:
            print(f"  ✓ {reg['email']} | CPF: {reg['cpf']} | Tel: {reg['telefone']} | Data: {reg['data']}")

    if invalidos:
        print("\n[REGISTROS INVÁLIDOS]:")
        for inv in invalidos:
            print(f"  ✗ Linha {inv['linha']}: {inv['motivo']}")
            print(f"    Dados originais: {inv['dados']}")

    print("="*50)


# Execução principal
if __name__ == "__main__":
    processar_arquivo_dados("dados.csv")