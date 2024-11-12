from urllib.parse import urlparse, parse_qs

def extrair_video_id(url):
    # Analisa a URL e obtém os parâmetros da query string
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    # Obtém o valor do parâmetro 'v'
    video_id = query_params.get('v')
    if video_id:
        return video_id[0]  # Retorna o primeiro ID encontrado
    else:
        return None


def is_url(string):
    try:
        result = urlparse(string)
        # A valid URL should have at least scheme and netloc
        return all([result.scheme, result.netloc])
    except ValueError:
        return False