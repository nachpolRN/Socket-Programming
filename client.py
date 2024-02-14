import socket
import threading

# กำหนด host และ port
HOST = '127.0.0.1'
PORT = 8080

def receive_messages(s):
    while True:
        data = s.recv(1024)
        if data:
            print(data.decode())

# รับชื่อจากผู้ใช้เพื่อแสดงในการส่งข้อมูล
client_name = input("Enter your name: ")

# สร้าง socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # เชื่อมต่อกับ server
    s.connect((HOST, PORT))

    # ส่งชื่อของ client ไปยัง server เพื่อแสดงในข้อความ
    s.sendall(client_name.encode())

    # สร้าง thread สำหรับการรับข้อมูลจาก server
    receive_thread = threading.Thread(target=receive_messages, args=(s,))
    receive_thread.start()

    # รับข้อความจากผู้ใช้และส่งไปยัง server
    while True:
        message = input("")
        if message.lower() == 'exit':
            break
        full_message = f"{client_name}: {message}"
        s.sendall(full_message.encode())


