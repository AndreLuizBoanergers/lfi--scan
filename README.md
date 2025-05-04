# 🔍 LFI Scanner - Local File Inclusion Checker

Este script testa automaticamente URLs em busca de vulnerabilidades **LFI (Local File Inclusion)** usando uma wordlist padrão de arquivos sensíveis do sistema.

## ⚙️ Funcionalidades

- Testa múltiplas URLs com payloads LFI conhecidos.
- Detecta conteúdo vulnerável diretamente renderizado (ex: `/etc/passwd`, `.env`, configs).
- Detecta downloads forçados de arquivos sensíveis.
- Registra tudo em `resultados.txt`, incluindo o tipo de resposta (texto, download ou vazio).
- Suporte a interrupção com `Ctrl+C`.

---

## 📂 Estrutura

LFI_SCAN/
├── lista.txt # Lista de URLs para testar
├── main.py # Script principal
├── resultados.txt # Logs dos resultados
└── README.md # Este arquivo


---

## 📜 Exemplo de `lista.txt`

```txt
https://site.com/index.php?id=
https://alvo.com/download.php?file=
https://teste.com/view.php?path=


use  python main.py
