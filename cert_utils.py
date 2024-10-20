import os
# import httpx

def configure_ssl(cert_path: str):
    """
    Configura o ambiente Python para confiar no certificado fornecido.
    
    Args:
        cert_path (str): Caminho para o arquivo de certificado .pem.
    """
    expanded_cert_path = os.path.expanduser(cert_path)

    if not os.path.isfile(expanded_cert_path):
        raise FileNotFoundError(f"O certificado não foi encontrado no caminho: {expanded_cert_path}")

    os.environ['REQUESTS_CA_BUNDLE'] = expanded_cert_path
    os.environ['CURL_CA_BUNDLE'] = expanded_cert_path
    print(f"Certificado configurado: {expanded_cert_path}")

def setup_ssl():
    """
    Configura o ambiente Python para usar um certificado SSL especificado e retorna um cliente HTTPX configurado.
    
    Returns:
        httpx.Client: Cliente HTTPX configurado.
    """
    cert_path = '~/combined_certificates.pem'
    configure_ssl(cert_path)
    
    # Testa a conexão HTTPS para garantir que o certificado está funcionando
    # test_https_connection()

#     # Cria e retorna um cliente HTTPX configurado
#     return create_httpx_client(cert_path)

# def test_https_connection(url: str = 'https://huggingface.co'):
#     """
#     Testa uma conexão HTTPS para verificar se o certificado está configurado corretamente.
    
#     Args:
#         url (str): URL para testar a conexão. Padrão é 'https://huggingface.co'.
#     """
#     response = httpx.get(url, verify=os.getenv('REQUESTS_CA_BUNDLE'))
#     print(f"Teste de conexão: {response.status_code}")

# def create_httpx_client(cert_path: str) -> httpx.Client:
#     """
#     Cria um cliente HTTPX configurado para usar um certificado SSL específico.
    
#     Args:
#         cert_path (str): Caminho para o arquivo de certificado .pem.
        
#     Returns:
#         httpx.Client: Cliente HTTPX configurado.
#     """
#     expanded_cert_path = os.path.expanduser(cert_path)
#     return httpx.Client(verify=expanded_cert_path)