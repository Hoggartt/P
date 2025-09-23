from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",  # SSH
    "host": "172.16.6.244",
    "username": "ertine",
    "password": "admin",
    "secret": "enable_password",
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
