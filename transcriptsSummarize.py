# Nome do arquivo: process_transcript.py

import re
import os
import openai
import ssl
import urllib3
import httpx
import traceback

# Importa a função get_transcript do seu script existente
from transcriptsDownload import get_transcript

# Desabilita avisos de SSL (não recomendado para produção)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Desabilita verificações de SSL globalmente (não recomendado para produção)
ssl._create_default_https_context = ssl._create_unverified_context

# Define sua chave de API da OpenAI a partir da variável de ambiente
openai.api_key = os.environ.get('OPENAI_API_KEY')  # Certifique-se de definir esta variável de ambiente

# Cria um cliente HTTP personalizado com SSL desabilitado
http_client = httpx.Client(verify=False)

# Cria a instância da API OpenAI com o cliente HTTP personalizado
client = openai.OpenAI(
    http_client=http_client,
    api_key=openai.api_key
)

def split_transcript(transcript, max_chunk_size=10000):
    """
    Divide o transcript em sentenças e agrupa em chunks de até max_chunk_size caracteres.
    """
    # Divide o transcript em sentenças usando expressões regulares
    sentences = re.split(r'(?<=[.!?]) +', transcript)
    chunks = []
    current_chunk = ''
    for sentence in sentences:
        # Verifica se adicionar a próxima sentença excede o tamanho máximo do chunk
        if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
            current_chunk += sentence + ' '
        else:
            # Se o chunk atual não estiver vazio, adiciona-o à lista de chunks
            if current_chunk:
                chunks.append(current_chunk.strip())
            # Inicia um novo chunk com a sentença atual
            current_chunk = sentence + ' '
    # Adiciona o último chunk se não estiver vazio
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def process_chunk(chunk):
   
    """
    Envia um chunk para a API da OpenAI e retorna a resposta.
    """
    try:
        # Prepara o prompt para a API da OpenAI
        prompt = f"""
        A partir do seguinte texto, gere:

        1) Uma descrição resumida do vídeo para que eu possa adicionar como descrição no novo vídeo.
        2) Uma sugestão de título bem atrativo que gere interesse e curiosidade nas pessoas. o título deve ser super sensacionalista para atrair muitas pessoas.
        3) Hashtags relevantes para eu usar na publicação deste novo vídeo.

        Texto:
        {chunk}

        Forneça a saída no seguinte formato:

        Descrição:
        <Sua descrição aqui>

        Título:
        <Seu título aqui>

        Hashtags:
        <Suas hashtags aqui>
        """

        # Chama a API da OpenAI para gerar a descrição, título e hashtags
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {"role": "system", "content": "Você é um assistente útil extremamente especializado em marketing digital, SEO, produção de videos no Youtube, e que está com a função de gerar descrições bem resumidas e ricas em conteúdo, títulos atrativos e super sensacionalista para atrair muitas pessoas, e hashtags com base no texto fornecido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        content = response.choices[0].message.content.strip()
        return content
    except Exception as e:
        print(f"Ocorreu um erro durante o processamento do chunk: {e}")
        traceback.print_exc()
        return None

def consolidate_results(results):
    """
    Consolida todas as descrições, títulos e hashtags em uma única chamada à API da OpenAI.
    """
    try:
        # Prepara o prompt para consolidar os resultados
        prompt = f"""
        Você recebeu várias descrições, títulos e hashtags para um vídeo. Consolide todas elas em uma única descrição, um título atrativo e super sensacionalista para atrair muitas pessoas, e um conjunto de hashtags relevantes e que gere muito engajamento. 

        Aqui estão os resultados coletados:

        {"".join(results)}

        Forneça a saída no seguinte formato:

        Descrição Consolidada:
        <Descrição consolidada aqui>

        Título Consolidado:
        <Título consolidado aqui>

        Hashtags Consolidadas:
        <Hashtags consolidadas aqui>
        """

        # Chama a API da OpenAI para consolidar os resultados
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {"role": "system", "content": "Você é um assistente útil extremamente especializado em marketing digital, SEO, produção de videos no Youtube, e que está com a função de gerar descrições bem resumidas e ricas em conteúdo, títulos  atrativos e super sensacionalista para atrair muitas pessoas, e hashtags com base no texto fornecido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        consolidated_content = response.choices[0].message.content.strip()
        return consolidated_content
    except Exception as e:
        print(f"Ocorreu um erro durante a consolidação dos resultados: {e}")
        traceback.print_exc()
        return None

def main():
    # video_id = 'i11fFciD9zQ'  # Substitua pelo ID do seu vídeo no YouTube
    video_id = 'rFl0yH__B_o'

    # Obtém o transcript usando sua função existente
    transcript = get_transcript(video_id)
    if not transcript:
        print("Falha ao obter o transcript.")
        return

    # Divide o transcript em chunks
    chunks = split_transcript(transcript, max_chunk_size=10000)
    # print(f"O transcript foi dividido em {len(chunks)} chunks.")

    # Lista para armazenar os resultados de cada chunk
    chunk_results = []

    # Processa cada chunk
    for i, chunk in enumerate(chunks, 1):
        # print(f"\nProcessando chunk {i}/{len(chunks)}...")
        result = process_chunk(chunk)
        if result:
            # print(f"Resultados para o chunk {i}:\n")
            # print(result)
            chunk_results.append(result)
        else:
            print(f"Falha ao processar o chunk {i}.")

    # Consolidar os resultados após processar todos os chunks
    if chunk_results:
        # print("\nConsolidando todos os resultados...")
        consolidated_output = consolidate_results(chunk_results)
        if consolidated_output:
            # print("\nResultados Consolidados:\n")
            print(consolidated_output)
        else:
            print("Falha ao consolidar os resultados.")
    else:
        print("Nenhum resultado para consolidar.")

if __name__ == "__main__":
    main()
