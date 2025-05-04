# 🔍 LFI Scanner - Local File Inclusion Checker

Este é um scanner básico para detecção de **LFI (Local File Inclusion)** em URLs. Ele testa automaticamente diversas *payloads* conhecidas contra uma lista de URLs e identifica se há retorno de arquivos do servidor, como `/etc/passwd`, `wp-config.php`, `.env`, etc.

---

## 🚀 Como usar

1. Crie um arquivo `lista.txt` com uma URL por linha que você deseja testar:

```
https://site.com/index.php?page=
https://alvo.com/download.php?file=
https://exemplo.org/view.php?id=
```

2. Execute o script:

```bash
python main.py
```

3. Os resultados serão salvos no arquivo `resultados.txt` automaticamente. Também serão exibidos no terminal em tempo real.

---

## 📦 Requisitos

- Python 3.x
- `requests`

Instalar o `requests` se não tiver:

```bash
pip install requests
```

---

## 📁 Estrutura de Pastas

```
LFI_SCAN/
├── lista.txt         # Lista de URLs para testar
├── main.py           # Script principal (scanner LFI)
├── resultados.txt    # Logs dos resultados (saída do script)
└── README.md         # Este arquivo de instruções
```

---

## 🧪 O que o script faz?

- Pega cada URL da lista.
- Injeta diversos payloads de LFI no primeiro parâmetro `?x=` encontrado.
- Verifica:
  - Se o retorno tem conteúdo típico de LFI (`root:x:`, `define(`, etc).
  - Se for download forçado, verifica o tamanho para detectar vazamento.
- Classifica como:
  - `✔️ TEXTO` → conteúdo legível na resposta
  - `💾 DOWNLOAD` → arquivo foi retornado para download
  - `⚠️ DOWNLOAD VAZIO` → arquivo existe mas está vazio
  - `❌` → falha no payload
  - `🧨 ERRO` → erro de rede

---

## 🛑 Cancelar o processo

Pode parar o script com `Ctrl+C` a qualquer momento. Ele vai sair de forma limpa e digna.

---

## ⚠️ Disclaimer

Este script é apenas para **fins educacionais**. O uso contra sistemas sem autorização é **ilegal**. Utilize com responsabilidade e somente em ambientes de teste ou com permissão explícita.

---
