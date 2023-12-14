import json
import socket
import time
import pandas as pd

def handle_date(obj):
    if isinstance(obj, pd.Timestamp):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    raise TypeError(f"Object of type '{type(obj).__name__}' is not JSON serializable")

def send_data_over_socket(file_path, host='localhost', port=9999, chunk_size=2):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
        s.listen(1)
        print(f"Listening for connections on {host}:{port}")

        last_sent_index = 0
        while True:
            conn, addr = s.accept()
            print(f"Connection from {addr}")
            try:
                with open(file_path, 'r') as file:
                    # Skip the lines that were already sent
                    for _ in range(last_sent_index):
                        next(file)

                    records = []
                    for line in file:
                        records.append(json.loads(line))
                        if len(records) == chunk_size:
                            chunk = pd.DataFrame(records)
                            print(chunk)
                            for record in chunk.to_dict(orient='records'):
                                serialize_data = json.dumps(record, default=handle_date).encode('utf-8')
                                conn.send(serialize_data + b'\n')
                                time.sleep(1)  # Adjust sleep time if needed
                                last_sent_index += 1

                            records = []
            except (BrokenPipeError, ConnectionResetError):
                print("Client disconnected.")
            finally:
                conn.close()
                print("Connection closed")

    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    send_data_over_socket("datasets/demo.json")
