from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from urllib.request import urlretrieve
from zipfile import ZipFile, ZIP_DEFLATED



def WebScraping():

    anexos_link = []
    anexos_text = ['Anexo I.', 'Anexo II.']

    try:
        #abrir navegador na pagina do site
        driver = webdriver.Chrome()
        driver.get("https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos")
        driver.maximize_window()

        #pegar os links dos anexos
        for text in anexos_text:
            try:
                anexo_element = driver.find_element(By.LINK_TEXT, text)
                href = anexo_element.get_attribute("href")
                if href:
                    anexos_link.append(href)
                else:
                    print(f"Link para {text} não encontrado")
            except Exception as e:
                print(f"Erro ao encontrar o link para {text}: {e}")

        #criar pasta para salvar os arquivos
        os.makedirs("downloads/Procedimentos_e_Eventos_em_Saúde", exist_ok=True)

        #baixar os arquivos
        for href in anexos_link:
            fileName = os.path.join("downloads/Procedimentos_e_Eventos_em_Saúde", os.path.basename(href))
            try:
                urlretrieve(href, fileName)
                print(f"Arquivo baixado: {fileName}")
            except Exception as e:
                print(f"Erro ao baixar o arquivo {fileName}: {e}")

    finally:
        driver.quit()

    # adicionar os arquivos baixados ao zip
    arquivoZip = ZipFile("downloads/Procedimentos_e_Eventos_em_Saúde/anexos.zip","w", compression=ZIP_DEFLATED)
    for arquivo in os.listdir("downloads/Procedimentos_e_Eventos_em_Saúde"):
        if arquivo.endswith(".pdf"):
            arquivoZip.write(os.path.join("downloads/Procedimentos_e_Eventos_em_Saúde", arquivo), arquivo)
    arquivoZip.close()


WebScraping() #uso para testar o script