#с пользовательским интерфейсом

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException


host = input("IP коммутатора: ").strip()
username = input("Логин: ").strip()
password = input("Пароль: ").strip()
secret = input("Enable пароль (если нет, просто Enter): ").strip()

print("\nВыберите тип коммутатора:")
print("1 — Cisco IOS (Catalyst)")
print("2 — Cisco NX-OS (Nexus)")
print("3 — HP ProCurve / Aruba")
print("4 — Juniper JunOS")
print("5 — Xyxel")
print("6 — Extel")

choice = input("Номер [1]: ").strip() or "1"
device_types = {
    "1": "cisco_ios",
    "2": "cisco_nxos",
    "3": "hp_procurve",
    "4": "juniper",
    "5": "xyxel",
    "6": "extel",
}
device_type = device_types.get(choice, "cisco_ios")
interface = input("\nИнтерфейс (например fa0/1 или ge-0/0/1): ").strip()

print("\nДействие с интерфейсом:")
print("shutdown — выключить порт")
print("no shutdown — включить порт")
print("mode — настроить VLAN и режим")

action = input("Что делаем: ").strip().lower()

mode = vlan = ""
if action == "mode":
    print("\nРежим интерфейса:")
    print("access — один VLAN (например компьютер, IP-телефон)")
    print("trunk — несколько VLAN (например между коммутаторами)")
    mode = input("Режим (access/trunk): ").strip().lower()
    vlan = input("Введите VLAN или VLANы через запятую (например 10 или 10,20,30): ").strip()

device = {
    "device_type": device_type,
    "host": host,
    "username": username,
    "password": password,
    "secret": secret,
    "port": 22
}

try:
    conn = ConnectHandler(**device)
    if device_type in ["cisco_ios", "cisco_nxos", "hp_procurve", "xyxel", "extel"]:
        conn.enable()
    print(f"\nУспешно подключились к {host} ({device_type})")
    commands = [f"interface {interface}"]

    if action == "shutdown":
        commands.append("shutdown")
    elif action == "no shutdown":
        commands.append("no shutdown")
    elif action == "mode":
        if mode == "access":
            commands += [
                "switchport mode access",
                f"switchport access vlan {vlan}",
                "description подключение к клиенту"
            ]
        elif mode == "trunk":
            commands += [
                "switchport mode trunk",
                f"switchport trunk allowed vlan {vlan}",
                "description транк между коммутаторами"
            ]
    print("\nОтправляем команды:")
    for cmd in commands:
        print(" ", cmd)

    output = conn.send_config_set(commands)
    print("\n--- Результат ---\n", output)

    cfg_cmd = f"show run interface {interface}" if device_type in ["cisco_ios", "cisco_nxos", "hp_procurve", "xyxel", "extel"] else f"show configuration interfaces {interface}"
    print(f"\n--- Конфигурация {interface} ---\n")
    print(conn.send_command(cfg_cmd))

    save = input("\nСохраняем конфигурацию? (y/N): ").strip().lower()
    if save == "y":
        if hasattr(conn, "save_config"):
            save_output = conn.save_config()
        else:
            save_output = conn.send_command_timing("write memory")
        print("\n--- Результат сохранения ---\n", save_output)

    conn.disconnect()
    print("\nСоединение закрыто")

except NetmikoTimeoutException:
    print(f"\nНе удалось подключиться к {host}. Проверь IP и SSH.")
except NetmikoAuthenticationException:
    print(f"\nНеверный логин или пароль для {host}.")
except Exception as e:
    print(f"\nОшибка: {e}")
_________
from netmiko import ConnectHandler


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

conn = ConnectHandler(
    device_type=device["device_type"],
    host=device["host"],
    username=device["username"],
    password=device["password"],
    secret=device["secret"],
    port=device["port"]
)
conn.enable()
print(f"Подключились к {device['host']} ({device['device_type']})")
commands = [f"interface {device['interface']}"]

if device["action"] == "shutdown":
    commands.append("shutdown")
elif device["action"] == "no shutdown":
    commands.append("no shutdown")
elif device["action"] == "mode":
    if device["mode"] == "access":
        commands += [
            "switchport mode access",
            f"switchport access vlan {device['vlan']}",
            "description Подключение клиентского устройства"
        ]
    elif device["mode"] == "trunk":
        commands += [
            "switchport mode trunk",
            f"switchport trunk allowed vlan {device['vlan']}",
            "description Транк между коммутаторами"
        ]
print("\nОтправляем команды на устройство:")
for cmd in commands:
    print("  >", cmd)
output = conn.send_config_set(commands)
print("\nРезультат выполнения команд\n", output)

cfg_cmd = f"show run interface {device['interface']}"
cfg_output = conn.send_command(cfg_cmd)
print(f"\nКонфигурация интерфейса {device['interface']}\n", cfg_output)

print("\nСохраняем конфигурацию на устройстве...")
save_output = conn.send_command_timing("write memory")
print("\nРезультат сохранения\n", save_output)

conn.disconnect()
print("\nСоединение закрыто")
