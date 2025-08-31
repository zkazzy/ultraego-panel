import os, sys, time, requests

# Cores
CIANO = "\033[96m"; VERDE = "\033[92m"; VERMELHO = "\033[91m"; AMARELO = "\033[93m"; RESET = "\033[0m"

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def efeito_digitacao(texto, delay=0.02):
    for c in texto:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def animacao_carregamento():
    limpar_tela()
    efeito_digitacao(f"{CIANO}🚀 Iniciando o KZPainel UltraEgo by Kazzy...", 0.05)
    for i in range(11):
        sys.stdout.write(f"\r{AMARELO}🔄 Carregando [{'█'*i}{'░'*(10-i)}]{RESET}")
        sys.stdout.flush()
        time.sleep(0.2)
    print(f"\n{VERDE}✅ Sistema pronto, Kazzy!{RESET}")
    time.sleep(1)

def mostrar_logo_kazzy():
    print(f"""{CIANO}
██╗  ██╗ █████╗ ███████╗███████╗██╗   ██╗
██║ ██╔╝██╔══██╗╚══███╔╝╚══███╔╝╚██╗ ██╔╝
█████╔╝ ███████║  ███╔╝   ███╔╝  ╚████╔╝ 
██╔═██╗ ██╔══██║ ███╔╝   ███╔╝    ╚██╔╝  
██║  ██╗██║  ██║███████╗███████╗   ██║   
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝    
{RESET}""")
    print(f"{AMARELO}🔧 Painel desenvolvido por Kazzy — versão ULTRAEGO 7.1{RESET}")

def verificar_token(token):
    headers = {"Authorization": token}
    try:
        res = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        if res.status_code == 200:
            return res.json()
        elif res.status_code == 401:
            print(f"{VERMELHO}❌ Token inválido ou expirado.{RESET}")
        else:
            print(f"{VERMELHO}⚠️ Erro ao verificar token — Código: {res.status_code}{RESET}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"{VERMELHO}❌ Erro de conexão: {e}{RESET}")
        return None

def sair_de_servidores(token):
    headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers)
        guilds = res.json()
        count = 0
        for guild in guilds:
            gid = guild["id"]
            name = guild.get("name", "Desconhecido")
            r = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{gid}", headers=headers)
            if r.status_code == 204:
                print(f"{VERDE}✅ Saiu de: {name}{RESET}")
                count += 1
            elif r.status_code == 429:
                retry = r.json().get("retry_after", 5)
                print(f"{AMARELO}⏳ Rate limit! Aguardando {retry} segundos...{RESET}")
                time.sleep(retry)
            else:
                print(f"{VERMELHO}❌ Falha ao sair de: {name} — Código: {r.status_code}{RESET}")
            time.sleep(2)
        print(f"\n{VERDE}✅ Saiu de {count} servidores com sucesso.{RESET}")
    except Exception as e:
        print(f"{VERMELHO}❌ Erro: {e}{RESET}")

def limpar_mensagens_enviadas(token):
    headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers)
        channels = res.json()
        total = 0
        for channel in channels:
            cid = channel.get("id")
            if not cid:
                continue
            msgs = requests.get(f"https://discord.com/api/v9/channels/{cid}/messages?limit=50", headers=headers).json()
            for msg in msgs:
                if msg.get("author", {}).get("id") != "":
                    mid = msg["id"]
                    r = requests.delete(f"https://discord.com/api/v9/channels/{cid}/messages/{mid}", headers=headers)
                    if r.status_code == 204:
                        print(f"{VERDE}✅ Mensagem apagada: {mid}{RESET}")
                        total += 1
                    time.sleep(2)
        print(f"\n{VERDE}✅ Total de mensagens apagadas: {total}{RESET}")
    except Exception as e:
        print(f"{VERMELHO}❌ Erro: {e}{RESET}")

def apagar_mensagens_com_midia(token):
    headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers)
        channels = res.json()
        total = 0
        for channel in channels:
            cid = channel.get("id")
            if not cid:
                continue
            msgs = requests.get(f"https://discord.com/api/v9/channels/{cid}/messages?limit=50", headers=headers).json()
            for msg in msgs:
                if msg.get("author", {}).get("id") != "" and (msg.get("attachments") or msg.get("embeds")):
                    mid = msg["id"]
                    r = requests.delete(f"https://discord.com/api/v9/channels/{cid}/messages/{mid}", headers=headers)
                    if r.status_code == 204:
                        print(f"{VERDE}✅ Mídia apagada: {mid}{RESET}")
                        total += 1
                    time.sleep(2)
        print(f"\n{VERDE}✅ Total de mídias apagadas: {total}{RESET}")
    except Exception as e:
        print(f"{VERMELHO}❌ Erro: {e}{RESET}")

def remover_amigos(token):
    headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=headers)
        amigos = res.json()
        total = 0
        for amigo in amigos:
            uid = amigo["id"]
            nome = amigo.get("user", {}).get("username", "Desconhecido")
            r = requests.delete(f"https://discord.com/api/v9/users/@me/relationships/{uid}", headers=headers)
            if r.status_code == 204:
                print(f"{VERDE}✅ Amigo removido: {nome}{RESET}")
                total += 1
            else:
                print(f"{VERMELHO}❌ Falha ao remover: {nome} — Código: {r.status_code}{RESET}")
            time.sleep(2)
        print(f"\n{VERDE}✅ Total de amigos removidos: {total}{RESET}")
    except Exception as e:
        print(f"{VERMELHO}❌ Erro: {e}{RESET}")

def limpar_dms_usuario(token, uid, total_desejado):
    headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
    try:
        res = requests.post(
            "https://discord.com/api/v9/users/@me/channels",
            headers=headers,
            json={"recipient_id": uid}
        )
        if res.status_code != 200:
            print(f"{VERMELHO}❌ Erro ao abrir canal com usuário. Código: {res.status_code}{RESET}")
            return

        cid = res.json()["id"]
        apagadas = 0
        ultima_id = None

        while apagadas < total_desejado:
            params = {"limit": 50}
            if ultima_id:
                params["before"] = ultima_id

            msgs = requests.get(
                f"https://discord.com/api/v9/channels/{cid}/messages",
                headers=headers,
                params=params
            ).json()

            if not msgs:
                break

            for msg in msgs:
                if msg.get("author", {}).get("id") != uid:
                    mid = msg["id"]
                    r = requests.delete(
                        f"https://discord.com/api/v9/channels/{cid}/messages/{mid}",
                        headers=headers
                    )
                    if r.status_code == 204:
                        print(f"{VERDE}✅ Mensagem apagada: {mid}{RESET}")
                        apagadas += 1
                    elif r.status_code == 429:
                        retry = r.json().get("retry_after", 5)
                        print(f"{AMARELO}⏳ Rate limit! Aguardando {retry} segundos...{RESET}")
                        time.sleep(retry)
                    time.sleep(2)

                if apagadas >= total_desejado:
                    break

            ultima_id = msgs[-1]["id"]

        print(f"\n{VERDE}✅ Total de mensagens apagadas: {apagadas}{RESET}")

    except Exception as e:
        print(f"{VERMELHO}❌ Erro: {e}{RESET}")


def apagar_midias_usuario(token, uid, total_desejado):
    headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
    try:
        res = requests.post(
            "https://discord.com/api/v9/users/@me/channels",
            headers=headers,
            json={"recipient_id": uid}
        )
        if res.status_code != 200:
            print(f"{VERMELHO}❌ Erro ao abrir canal com usuário. Código: {res.status_code}{RESET}")
            return

        cid = res.json()["id"]
        apagadas = 0
        ultima_id = None

        while apagadas < total_desejado:
            params = {"limit": 50}
            if ultima_id:
                params["before"] = ultima_id

            msgs = requests.get(
                f"https://discord.com/api/v9/channels/{cid}/messages",
                headers=headers,
                params=params
            ).json()

            if not msgs:
                break

            for msg in msgs:
                if msg.get("author", {}).get("id") != uid and (msg.get("attachments") or msg.get("embeds")):
                    mid = msg["id"]
                    r = requests.delete(
                        f"https://discord.com/api/v9/channels/{cid}/messages/{mid}",
                        headers=headers
                    )
                    if r.status_code == 204:
                        print(f"{VERDE}✅ Mídia apagada: {mid}{RESET}")
                        apagadas += 1
                    elif r.status_code == 429:
                        retry = r.json().get("retry_after", 5)
                        print(f"{AMARELO}⏳ Rate limit! Aguardando {retry} segundos...{RESET}")
                        time.sleep(retry)
                    time.sleep(2)

                if apagadas >= total_desejado:
                    break

            ultima_id = msgs[-1]["id"]

        print(f"\n{VERDE}✅ Total de mídias apagadas: {apagadas}{RESET}")

    except Exception as e:
        print(f"{VERMELHO}❌ Erro: {e}{RESET}")

def main():
    animacao_carregamento()
    mostrar_logo_kazzy()

    # Pegando variáveis de ambiente do Render
    token = os.environ.get("DISCORD_TOKEN")
    uid = os.environ.get("TARGET_USER_ID")
    delete_limit = int(os.environ.get("DELETE_LIMIT", "50"))

    if not token:
        print(f"{VERMELHO}❌ Nenhum token encontrado na variável de ambiente DISCORD_TOKEN.{RESET}")
        return

    usuario = verificar_token(token)
    if not usuario:
        print(f"{VERMELHO}❌ Token inválido ou erro de conexão.{RESET}")
        return

    print(f"{VERDE}✅ Logado como {usuario['username']}#{usuario['discriminator']}{RESET}")

    # Executa todas as funções na ordem
    sair_de_servidores(token)
    limpar_mensagens_enviadas(token)
    apagar_mensagens_com_midia(token)
    remover_amigos(token)

    if uid:
        limpar_dms_usuario(token, uid, delete_limit)
        apagar_midias_usuario(token, uid, delete_limit)
    else:
        print(f"{AMARELO}⚠️ Nenhum TARGET_USER_ID definido. Pulando funções específicas de usuário.{RESET}")

if __name__ == "__main__":
    main()
