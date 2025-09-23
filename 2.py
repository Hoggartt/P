from netmiko import ConnectHandler

use_input = input("Использовать ввод пользователя? (y/N): ").lower() == "y"

if use_input:
    host = input("IP коммутатора: ").strip()
    username = input("Логин: ").strip()
    password = input("Пароль: ").strip()
    secret = input("Enable пароль (если нет, Enter): ").strip()
    interface = input("Интерфейс (например fa0/1): ").strip()
    action = input("Действие (shutdown / no shutdown / mode): ").lower().strip()
    mode = vlan = ""
    if action == "mode":
        mode = input("Режим (access/trunk): ").lower().strip()
        vlan = input("VLAN или VLANы через запятую: ").strip()

    device = {
        "device_type": "cisco_ios",  # SSH-подключение
        "host": host,
        "username": username,
        "password": password,
        "secret": secret,
        "port": 22,  # SSH
        "interface": interface,
        "action": action,
        "mode": mode,
        "vlan": vlan
    }
else:
    device = {
        "device_type": "cisco_ios",
        "host": "192.168.1.10",
        "username": "admin",
        "password": "cisco",
        "secret": "cisco",
        "port": 22,
        "interface": "fa0/1",
        "action": "mode",
        "mode": "access",
        "vlan": "10"
    }

conn = ConnectHandler(**device)
conn.enable()

cmds = [f"interface {device['interface']}"]

if device["action"] == "shutdown":
    cmds.append("shutdown")
elif device["action"] == "no shutdown":
    cmds.append("no shutdown")
elif device["action"] == "mode":
    if device["mode"] == "access":
        cmds += [f"switchport mode access", f"switchport access vlan {device['vlan']}"]
    elif device["mode"] == "trunk":
        cmds += [f"switchport mode trunk", f"switchport trunk allowed vlan {device['vlan']}"]

print("\nОтправляем команды:")
for c in cmds:
    print(" >", c)

print("\nРезультат выполнения команд:")
print(conn.send_config_set(cmds))

print("\nКонфигурация интерфейса:")
print(conn.send_command(f"show run interface {device['interface']}"))

save = input("\nСохраняем конфигурацию? (y/N): ").lower()
if save == "y":
    print(conn.send_command_timing("write memory"))

conn.disconnect()
print("\nСоединение закрыто")