import socket
import sys
import threading
import time

# whole client server code : must be split into two files
#  - server code
#  - client code

global gps_position


# DDBoat 17 (Server)
def handle_client(conn, addr, gps):
    global gps_position
    print("Connection established with {}".format(addr))

    try:
        while True:
            # rmc_ok, rmc_data = gps.read_rmc_non_blocking()
            # if rmc_ok:
            #     print ("RMC Data",rmc_data,rmc_ok)
            #     gps_position = "%f;%s;%f;%s\0" % (rmc_data[0], rmc_data[1], rmc_data[2], rmc_data[3])
            try:
                conn.sendall(gps_position.encode())
                print("Sent GPS Position to {}: {}".format(addr, gps_position))
                break
            except (socket.error, BrokenPipeError):
                print("Client {} disconnected unexpectedly.".format(addr))
                break  # Exit loop when client disconnects
            time.sleep(0.01)  # save computations (wait a bit)
    except Exception as e:
        print("Server error with {}: {}".format(addr, e))
    finally:
        print("Connection closed with {}".format(addr))
        conn.close()


def robot1_server():
    global gps_position
    gps_position = "0.0;N;0.0;E\0"
    sys.path.append('/home/pi/git/drivers-ddboat-v2')
    import gps_driver_v2 as gps_drv
    gps = gps_drv.GpsIO(tty_dev=1)
    gps.set_filter_speed("0")

    def gps_reading_thread():
        global gps_position
        print("GPS reading thread started")
        while True:
            rmc_ok = False
            try:
                rmc_ok, rmc_data = gps.read_rmc_non_blocking()
            except Exception as e:
                print("GPS reading thread error: {}".format(e))
            if rmc_ok:
                gps_position = "%f;%s;%f;%s\0" % (rmc_data[0], rmc_data[1], rmc_data[2], rmc_data[3])
                print("RMC Data", rmc_data, rmc_ok)
            time.sleep(0.1)

    gps_thread = threading.Thread(target=gps_reading_thread)
    gps_thread.daemon = True
    gps_thread.start()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5000))  # Listen on all available interfaces
    server_socket.listen(15)  # Allow up to 15 clients
    print("DDBoat 10 (Server) is waiting for connections...")

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr, gps))
        client_thread.start()


# Robot 2 (Client)
def robot2_client_loop(server_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 5000))
    print("Connected to DDBoat 17 (Server)")

    # def signal_handler(sig, frame):
    #     print("Closing client connection gracefully...")
    #     client_socket.close()
    #     sys.exit(0)

    # signal.signal(signal.SIGINT, signal_handler)

    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print("Received GPS Position from DDBoat 17: {}".format(data))
            time.sleep(0.01)
    except Exception as e:
        print("Client error: {}".format(e))
    finally:
        client_socket.close()


# Robot 2 (Client)
def robot2_client_onetime(server_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 5000))
    print("Connected to DDBoat 17 (Server)")

    # def signal_handler(sig, frame):
    #     print("Closing client connection gracefully...")
    #     client_socket.close()
    #     sys.exit(0)

    # signal.signal(signal.SIGINT, signal_handler)

    data = ""
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            last_two_chars = server_ip[-2:]
            print("Received GPS Position from DDBoat {}: {}".format(last_two_chars, data))
            break
    except Exception as e:
        print("Client error: {}".format(e))
    finally:
        client_socket.close()
    return data


if __name__ == "__main__":
    robot1_server()
