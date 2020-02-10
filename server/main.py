# Import stuff
import os
import threading
import traceback

# Run code in SPAM-MENU
spam_folder = os.path.dirname(os.path.abspath(__file__))
os.chdir(spam_folder)

# Import database files
from database.utils import get_date, get_time
from database.sockets import Server
from database.common_menu import LoginRegister

# Start the server
HOST = "localhost"
PORT = 8039
print(f"SPAM server started at {HOST} at port {PORT}")
server = Server(HOST, PORT)

login = LoginRegister()

def client_thread(code, BUFF_LENGTH = 4096):
    print("Connection receieved!")
    code, msg = server.recieve_string(BUFF_LENGTH)
    if code == '101':
        user_details = msg.split('/')
    elif code == '102':
        user_details = msg.split('/')
        verify = login.check_login(user_details[0], user_details[1])
        server.send_string(verify)
    elif code == '105':
        msg = msg.split('_')
        try:
            os.makedirs(f'data/logs/{msg[0]}')
        except:
            pass
        server.recv_file(f'data/logs/users/{msg[0]}/{msg[1]}', BUFF_LENGTH)
    elif code == '111':
        server.send_file(f'data/menus/{msg}.csv', BUFF_LENGTH)
    elif code == '112':
        server.send_file(f'data/{msg}', BUFF_LENGTH)
    elif code == '120':
        server.recv_file(f'data/{msg}', BUFF_LENGTH)
    elif code == '180':
        pass
    log_msg = (f"{get_time()} - {code} {msg}")
    log = open(f'data/logs/daily_logs/{get_date()}', 'a+')
    log.write(log_msg+'\n')
    print(log_msg)
    server.send_string("0")

while True:
    server.start_conn()
    try:
        code = 0
        threading.Thread(target=client_thread, args=(code, 4096)).start()
        if code == '180':
            server.close_conn()
            print(f"Connection closed with {server.ip}")
            break
    except:
        print("Oops! Something went wrong!")
        traceback.print_exc()
        server.close_conn()
server.close_server()

# Receive connection type
# 1) Login
# 2) Change Cart
# 3) Checkout
# dict of those functions

#print("Server stopped")