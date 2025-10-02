from netmiko import ConnectHandler
import time

device = {
    "device_type": "cisco_ios",
    "host": "192.168.236.10",
    "username": "admin",
    "password": "cisco123",
    "secret": "cisco123",
    "port": 22,
}

interface = "FastEthernet0/0"
action = "shutdown"  # или "no shutdown"

conn = None
try:
    conn = ConnectHandler(**device)
    conn.enable()

    conn.write_channel("configure terminal\n")
    time.sleep(1)

    conn.write_channel(f"interface {interface}\n")
    time.sleep(1)

    conn.write_channel(f"{action}\n")
    time.sleep(1)

    conn.write_channel("end\n")
    time.sleep(1)

    print(f"{interface} успешно выполнено: {action}")

except Exception as e:
    print("Ошибка при подключении или выполнении команд:", e)

finally:
    if conn:
        conn.disconnect()
