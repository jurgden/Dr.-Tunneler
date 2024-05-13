import paramiko 
import logging 
import argparse

# Set up logging 
logging.basicConfig(level=logging.DEBUG)

def setup_remote_port_forwarding(server, ssh_port, username, password, remote_host, remote_port, local_port):
    
    # Begin Error Handling
    try: 
        # Create our SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server, port+ssh_port, username=username, password=password)
        logging.info("SSH connection established")

        # Set up the remote port forwarding 
        # The '-R' flag will be represented by this code
        transport = client.get_transport()
        reverse_forwarding = transport.request_port_forward(remote_host, remote_port, local_port)
        logging.info(f"Port forwarding set up from remote {remote_host}:{remote_port} to local port {local_port}")


        # Keep the tunnel open
        transport.accept()

    except Exception as e:
        logging.error(f"Failed to forward ports: {e}")
    finally:
        # Handle the closure of the connection gracefully
        client.close()


def main():
    parser = argparse.ArgumentParser(description="Set up remote port forwarding for SSH.")
    parser.add_argument('--server', required=True, help="SSH server IP or hostname")
    parser.add_argument('--ssh-port', type=int, default=22, help="SSH server port")
    parser.add_argument('--username', required=True, help="SSH username")
    parser.add_argument('--password', required=True, help="SSH password")
    parser.add_argument('--remote_host', required=True, help="Remote host IP where port is forwarded")
    parser.add_argument('--remote_port', type=int, required=True, help="Remote port number to forward")
    parser.add_argument('--local_port', type=int, required=True, help="Local port number on server")

    args = parser.parse_args()

    setup_remote_port_forwarding(
        server=args.server,
        ssh_port=args.ssh_port,
        username=args.username,
        password=args.password,
        remote_host=args.remote_host,
        remote_port=args.remote_port,
        local_port=args.local_port
    )


if __name__ == '__main__':
    main()