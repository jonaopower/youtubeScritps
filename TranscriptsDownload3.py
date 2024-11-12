import requests
import xml.etree.ElementTree as ET
import json
from modules.helpFunctions import extrair_video_id, is_url

def fetch_youtube_transcript(video_input):
    if is_url(video_input):
        video_id = extrair_video_id(video_input)
        video_url = video_input
    else:
        video_id = video_input
        video_url = f"https://www.youtube.com/watch?v={video_id}"

    url = f"https://youtubetranscript.com/?server_vid2={video_id}"

    headers = {
        "Accept": "application/xml, text/xml, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Host": "youtubetranscript.com",
        "Referer": f"https://youtubetranscript.com/?v={video_id}",
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, verify=True)

    if response.status_code == 200:
        root = ET.fromstring(response.text)
        transcript_texts = []

        paragraph = ""
        for text_element in root.findall('text'):
            text_content = text_element.text.strip()
            if text_content:
                paragraph += text_content + " "
                if text_content.endswith(('.', '!', '?')):
                    transcript_texts.append(paragraph.strip())
                    paragraph = ""
        if paragraph:
            transcript_texts.append(paragraph.strip())

        # Cria o JSON formatado dentro da função
        output_json = {
            "video_id": video_id,
            "video_url": video_url,
            "transcript": transcript_texts
        }
        json_output = json.dumps(output_json, indent=4, ensure_ascii=False)
        return json_output
    else:
        print(f"Erro: {response.status_code}")
        print(response.text)
        return None


# Exemplo de uso
# video_input = "https://www.youtube.com/watch?v=zEwTfBCm-U0"  # Pode ser a URL ou o ID do vídeo
video_input = "zEwTfBCm-U0"
json_output = fetch_youtube_transcript(video_input)

if json_output is not None:
    print(json_output)
else:
    print("Falha ao obter a transcrição.")


# # Exemplo de uso
# video_id = "zEwTfBCm-U0"  # ID do vídeo do YouTube
# # video_id = "https://www.youtube.com/watch?v=zEwTfBCm-U0"
# transcript_df = fetch_youtube_transcript(video_id)

# if transcript_df is not None:
#     # print("Transcrição do vídeo:")
#     for line in transcript_df:
#         print(line['text'])
#     # print(transcript_df)
# else:
#     print("Falha ao obter a transcrição.")
