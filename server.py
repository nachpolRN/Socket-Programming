import socket
import threading

# กำหนด host และ port
HOST = '127.0.0.1'
PORT = 8080

# เก็บ client ที่เชื่อมต่อเข้ามา
clients = []

def handle_client(conn, addr):
    with conn:
        print('Connected by', addr)
        client_name = conn.recv(1024).decode()  # รับชื่อของผู้ใช้ที่เชื่อมต่อเข้ามา
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f'Received from {client_name}: {data.decode()}')
            # ส่งข้อมูลให้กับ client ทุกคนที่เชื่อมต่อ
            for client in clients:
                if client != conn:
                    client.sendall(data)
                    print(f'Sent to {client.getpeername()}: {data.decode()}')


# สร้าง socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # ผูก socket กับ address และ port
    s.bind((HOST, PORT))
    # รอการเชื่อมต่อจาก client
    s.listen()
    print('<<Start a Server>>')
    while True:
        # รอเข้ารับการเชื่อมต่อ
        conn, addr = s.accept()
        clients.append(conn)  # เก็บ client ที่เชื่อมต่อเข้ามา
        print('Accepted connection from', addr)
        # สร้าง thread ใหม่สำหรับการจัดการ client นี้
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
