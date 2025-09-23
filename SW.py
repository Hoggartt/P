#без пользовательского интерфейса

from netmiko import ConnectHandler

# Настройки коммутатора
device = {
    "device_type": "cisco_ios",
    "host": "192.168.1.10",
    "username": "admin",
    "password": "cisco",
    "secret": "cisco",
    "port": 22,
    "interface": "fa0/1",
    "action": "mode",      # shutdown / no shutdown / mode
    "mode": "access",      # access / trunk
    "vlan": "10"
}

# Подключаемся
conn = ConnectHandler(
    device_type=device["device_type"],
    host=device["host"],
    username=device["username"],
    password=device["password"],
    secret=device["secret"],
    port=device["port"]
)
conn.enable()

print("Подключились к", device["host"])

# Формируем команды
commands = [f"interface {device['interface']}"]

if device["action"] == "shutdown":
    commands.append("shutdown")
elif device["action"] == "no shutdown":
    commands.append("no shutdown")
elif device["action"] == "mode":
    if device["mode"] == "access":
        commands += [
            "switchport mode access",
            f"switchport access vlan {device['vlan']}"
        ]
    elif device["mode"] == "trunk":
        commands += [
            "switchport mode trunk",
            f"switchport trunk allowed vlan {device['vlan']}"
        ]

# Отправляем команды
output = conn.send_config_set(commands)
print("\nРезультат выполнения команд:\n", output)

# Проверяем конфигурацию интерфейса
cfg_cmd = f"show run interface {device['interface']}"
cfg_output = conn.send_command(cfg_cmd)
print("\nКонфигурация интерфейса:\n", cfg_output)

# Сохраняем конфигурацию
save_output = conn.send_command_timing("write memory")
print("\nСохранение конфигурации:\n", save_output)

conn.disconnect()
print("Соединение закрыто")
