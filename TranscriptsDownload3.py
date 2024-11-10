import requests
import xml.etree.ElementTree as ET
# import pandas as pd


def fetch_youtube_transcript(video_id):
    # Define o endpoint atualizado e o payload com o ID do vídeo
    # Substitua pelo endpoint atualizado, se necessário
    url = f"https://youtubetranscript.com/?server_vid2={video_id}"

    # Define os headers da requisição conforme capturado no modo de debug do Chrome
    headers = {
        "Accept": "application/xml, text/xml, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cookie": "_ga=GA1.1.516055162.1730140858; _ga_HWDD7ERPNX=GS1.1.1730140858.1.1730140877.41.0.0",
        "Host": "youtubetranscript.com",
        "Referer": f"https://youtubetranscript.com/?v={video_id}",
        "Sec-Ch-Ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }

    # Faz a requisição GET com a verificação SSL desativada
    response = requests.get(url, headers=headers, verify=False)

    # Verifica se a resposta foi bem-sucedida
    if response.status_code == 200:
        # Parseia o XML
        root = ET.fromstring(response.text)
        transcript_data = []

        # Extrai cada elemento de texto e suas informações de tempo
        for text_element in root.findall('text'):
            start_time = text_element.get('start')
            duration = text_element.get('dur')
            text_content = text_element.text
            transcript_data.append({
                "start_time": float(start_time),
                "duration": float(duration),
                "text": text_content
            })

        # Converte para DataFrame para melhor visualização e manipulação
        # transcript_df = pd.DataFrame(transcript_data)
        return transcript_data
    else:
        print(f"Erro: {response.status_code}")
        print(response.text)
        return None


# Exemplo de uso
video_id = "zEwTfBCm-U0"  # ID do vídeo do YouTube
transcript_df = fetch_youtube_transcript(video_id)

if transcript_df is not None:
    # print("Transcrição do vídeo:")
    for line in transcript_df:
        print(line['text'])
    # print(transcript_df)
else:
    print("Falha ao obter a transcrição.")
