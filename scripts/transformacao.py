import os
import pandas as pd
from re import search
import fitz
from tabula import read_pdf
from zipfile import ZipFile, ZIP_DEFLATED


def extrair_descricoes(pdf_path):
   # Extrai as descrições de AMB e OD da terceira página do PDF.
    descricao_amb = ""
    descricao_od = ""
    
    # Abrir o PDF com fitz
    doc = fitz.open(pdf_path)

    # Carregar a terceira página (índice 2)
    pagina = doc.load_page(2)
    
    texto = pagina.get_text("text")
        
    if texto:
        # Procurar a descrição de AMB
        match_amb = search(r"AMB\s*[:\-]?\s*(.*?Seg\..*?)\s*(?=OD|HCO|HSO|REF|PAC|DUT|$)", texto)  
        if match_amb:
            descricao_amb = match_amb.group(1).strip() 

        # Procurar a descrição de OD
        match_od = search(r"OD\s*[:\-]?\s*(.*?Seg\..*?)\s*(?=AMB|HCO|HSO|REF|PAC|DUT|$)", texto)  
        if match_od:
            descricao_od = match_od.group(1).strip()
    
    return descricao_amb, descricao_od


def processar_pdf(pdf_path):
    # Processa o PDF e extrai as tabelas
    try:
        tabelas = read_pdf(pdf_path, pages="all", lattice=True, multiple_tables=True)
        return tabelas
    except Exception as e:
        print(f"Erro ao processar o PDF: {e}")
        return None


def gerar_csv_e_zip(df_final):
    # Salvar como CSV estruturado, dividindo blocos por vírgulas
    df_final.to_csv("downloads/Procedimentos_e_Eventos_em_Saúde/tabelas_estruturadas.csv", index=False, encoding="utf-8")

    # Compactar o arquivo CSV em um zip
    with ZipFile("downloads/Procedimentos_e_Eventos_em_Saúde/tabelas_estruturadas.zip", "w", compression=ZIP_DEFLATED) as arquivoZip:
        arquivoZip.write("downloads/Procedimentos_e_Eventos_em_Saúde/tabelas_estruturadas.csv", "tabelas_estruturadas.csv")


def verificar_arquivo_pdf():
    # Verifica se o arquivo PDF já foi baixado
    try:
        for file in os.listdir("downloads/Procedimentos_e_Eventos_em_Saúde"):
            if file.startswith("Anexo_I_"):
                return os.path.join("downloads/Procedimentos_e_Eventos_em_Saúde", file)
    except FileNotFoundError:
        print("Nenhum arquivo PDF correspondente foi encontrado.")
        return None


def transformacao():
    pdf_path = verificar_arquivo_pdf()
    
    if pdf_path is None:
        return

    # Extrair descrições de AMB e OD
    descricao_amb, descricao_od = extrair_descricoes(pdf_path)
    
    # Processar as tabelas do PDF
    tabelas = processar_pdf(pdf_path)
    
    if tabelas is None:
        return

    
    df_final = pd.DataFrame()  
    
    for tabela in tabelas:
        if not tabela.empty:
            # Remover quebras de linha e espaços em branco
            tabela = tabela.applymap(lambda x: x.replace("\r", " ") if isinstance(x, str) else x) 
            df_final = pd.concat([df_final, tabela], ignore_index=True)

    # Renomear colunas para evitar duplicatas
    df_final.columns = ["PROCEDIMENTO", "RN", "VIGÊNCIA", descricao_amb, descricao_od, "HCO", "HSO", "REF", "PAC", "DUT", "SUBGRUPO", "GRUPO", "CAPÍTULO"]

    # Gerar o CSV e compactar em ZIP
    gerar_csv_e_zip(df_final)



transformacao() #uso para testar o script
