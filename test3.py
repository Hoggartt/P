from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.236.20",  # рабочий IP интерфейса для SSH
    "username": "admin",
    "password": "cisco123",
    "secret": "cisco123",
    "port": 22,
}

interface = "FastEthernet0/1"  # интерфейс, который нужно отключить
action = "shutdown"            # отключаем

try:
    conn = ConnectHandler(**device)
    conn.enable()

    conn.send_config_set([f"interface {interface}", action])
    print(f"{interface} успешно отключен ({action})")

except Exception as e:
    print("Ошибка при подключении или выполнении команд:", e)

finally:
    if conn:
        conn.disconnect()
