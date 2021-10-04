import requests
import time

token = input("BotToken> ")

headers = {
    "Content-Type": "Application/Json",
    "Authorization": f"Bot {token}"
}
response = requests.get(url="https://discord.com/api/v9/users/@me", headers=headers)
if response.status_code != 200:
    print("Tokenが無効です。")
    print("5秒後に自動的に閉じます。")
    time.sleep(5)
    exit()

with open("debug.txt", "r") as file:
    debug_mode = file.readline()
if debug_mode == "false":
    debug_mode_bool = False
elif debug_mode == "true":
    print("Debugモードで起動します。")
    debug_mode_bool = True

while True:
    command = input("BotCLI> ")
    args = command.split(" ")
    if args[0] == "help":
        print("// Commands")
        print("servers : 参加しているサーバーのリストを表示")
        print("channels <server id(Require)> : 指定したサーバーのIDのチャンネルを取得")
        print("messages <channel id(Require)> <limit> : 指定したチャンネルのIDのメッセージを最大100件まで取得")
        print("send <channel id(Require)> <message(Require)> : 指定したチャンネルIDのチャンネルへメッセージを送信します。")
        print("embed <channel id(Require)> <title(Require)> <description(Require)> : 指定したチャンネルIDのチャンネルへ、埋め込みメッセージを送信します。")
        print("kick <server id(Require)> <user id(Require)> : 指定したサーバーでユーザーをKickします")
        print("ban <server id(Require)> <user id(Require)> <Reason(Require)> : 指定したサーバーでユーザーをBanします")
        print("banlist <server id(Require)> : 指定したサーバーのBanリストを取得します")
    if args[0] == "servers":
        print("サーバーリストを取得中です。")
        headers = {
            "Content-Type": "Application/Json",
            "Authorization": f"Bot {token}"
        }
        response = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers).json()
        print("// Servers")
        for guild in response:
            guild_name = guild["name"]
            guild_id = guild["id"]
            print(f"{guild_name}({guild_id})")
        if debug_mode_bool == True:
            print("// Headers")
            print("Content-Type: Application/Json")
            print(f"Authorization: Bot {token}")
            print("// Params")
            print("Null")
            print("Connection methods: GET")
            print("Run command: servers")
            print("// Full json response")
            print(response.json())
    elif args[0] == "channels":
        print("チャンネルリストを取得中です。")
        try:
            server_id = args[1]
        except IndexError:
            print("ServerIDが未入力です。")
            continue
        headers = {
            "Content-Type": "Application/Json",
            "Authorization": f"Bot {token}"
        }
        response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/channels", headers=headers).json()
        print("// Channels")
        for channel in response:
            ch_name = channel["name"]
            ch_id = channel["id"]
            print(f"{ch_name}({ch_id})")
        if debug_mode_bool == True:
            print("// Headers")
            print("Content-Type: Application/Json")
            print(f"Authorization: Bot {token}")
            print("// Params")
            print("Null")
            print("Connection methods: GET")
            print("Run command: channels")
            print("// Full json response")
            print(response.json())
    elif args[0] == "messages":
        print("メッセージを取得中です。")
        try:
            channel_id = args[1]
        except IndexError:
            print("ChannelIDが未入力です。")
            continue
        headers = {
            "Content-Type": "Application/Json",
            "Authorization": f"Bot {token}"
        }
        try:
            limit = args[2]
            url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}"
        except IndexError:
            url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=100"
        response = requests.get(url=url, headers=headers).json()
        print("// Messages")
        print("// 一番上のメッセージが最新です")
        try:
            for message in response:
                sender = message["author"]["username"] + "#" + message["author"]["discriminator"]
                content = message["content"]
                print(f"{sender} >> {content}")
        except TypeError:
            print("何らかのエラーが発生しました。")
            print("5秒後に自動的にプログラムを終了します。")
            time.sleep(5)
            exit()
        if debug_mode_bool == True:
            print("// Headers")
            print("Content-Type: Application/Json")
            print(f"Authorization: Bot {token}")
            print("// Params")
            print("Null")
            print("Connection methods: GET")
            print("Run command: messages")
            print("// Full json response")
            print(response.json())
    elif args[0] == "send":
        try:
            channel_id = args[1]
            send_message = args[2]
        except IndexError:
            print("チャンネルIDまたはメッセージ内容が未入力です。")
            continue
        headers = {
            "Content-Type": "Application/Json",
            "Authorization": f"Bot {token}"
        }
        params = {
            "content": send_message
        }
        response = requests.post(url=f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=params).json()
        print("メッセージを送信しました。")
        if debug_mode_bool == True:
            print("// Headers")
            print("Content-Type: Application/Json")
            print(f"Authorization: Bot {token}")
            print("// Params")
            print(f"content: {send_message}")
            print("Connection methods: POST")
            print("Run command: send")
            print("// Full json response")
            print(response.json())
    elif args[0] == "embed":
        try:
            channel_id = args[1]
            title = args[2]
            description = args[3]
        except IndexError:
            print("1つまたは複数の引数の内容が未入力です。")
            continue
        headers = {
            "Content-Type": "Application/Json",
            "Authorization": f"Bot {token}"
        }
        params = {
            "embeds": [
                {
                    "title": title,
                    "description": description
                }
            ]
        }
        response = requests.post(url=f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=params).json()
        print("埋め込みメッセージを送信しました。")
        if debug_mode_bool == True:
            print("// Headers")
            print("Content-Type: Application/Json")
            print(f"Authorization: Bot {token}")
            print("// Params")
            embed_json_data = params["embeds"][0]
            print(f"embeds: {embed_json_data}")
            print("Connection methods: POST")
            print("Run command: embed")
            print("// Full json response")
            print(response.json())
    elif args[0] == "kick":
        try:
            server_id = args[1]
            user_id = args[2]
        except IndexError:
            print("1つまたは2つの引数が未入力です。")
        headers = {
            "Content-Type": "Application/Json",
            "Authorization": f"Bot {token}"
        }
        response = requests.delete(url=f"https://discord.com/api/v9/guilds/{server_id}/members/{user_id}", headers=headers)
        print("ユーザーをKickしました。")
        if debug_mode_bool == True:
            print("// Headers")
            print("Content-Type: Application/Json")
            print(f"Authorization: Bot {token}")
            print("// Params")
            print("Null")
            print("Connection methods: DELETE")
            print("Run command: kick")
            print("// Full json response")
            print(response.json())
    elif args[0] == "ban":
        try:
            server_id = args[1]
            user_id = args[2]
            reason = args[3]
        except IndexError:
            print("1つまたは2つの引数が未入力です。")
        headers = {
            "Content-Type": "Application/Json",
            "Authorization": f"Bot {token}"
        }
        params = {
            "reason": reason
        }
        response = requests.put(url=f"https://discord.com/api/v9/guilds/{server_id}/bans/{user_id}", headers=headers, json=params)
        print("ユーザーをBanしました。")
        if debug_mode_bool == True:
            print("// Headers")
            print("Content-Type: Application/Json")
            print(f"Authorization: Bot {token}")
            print("// Params")
            print(f"reason: {reason}")
            print("Connection methods: PUT")
            print("Run command: ban")
            print("// Full json response")
            print(response.json())
    elif args[0] == "banlist":
        try:
            server_id = args[1]
        except IndexError:
            print("引数が未入力です。")
            continue
        headers = {
            "Content-Type": "Application/Json",
            "Authorization": f"Bot {token}"
        }
        response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/bans", headers=headers)
        print("// Banリスト")
        for ban_user in response:
            base_user_json = ban_user["user"]
            username = base_user_json["username"]
            usertag = base_user_json["discriminator"]
            userfull = username + "#" + usertag
            userid = base_user_json["id"]
            reason = base_user_json["reason"]
            print(f"名前: {userfull}({userid})")
            print(f"理由: {reason}")
            print()
        if debug_mode_bool == True:
            print("// Headers")
            print("Content-Type: Application/Json")
            print(f"Authorization: Bot {token}")
            print("// Params")
            print("NULL")
            print("Connection methods: GET")
            print("Run command: banlist")
            print("// Full json response")
            print(response.json())