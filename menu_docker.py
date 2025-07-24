import paramiko
import getpass

def ssh_connect():
    hostname = input("Enter remote IP: ")
    username = input("Enter SSH username: ")
    password = getpass.getpass("Enter SSH password: ")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)
    return client

def docker_menu_ssh():
    client = ssh_connect()
    while True:
        print("""
--------------------------------------------------
      Docker Menu Based Program (SSH)
--------------------------------------------------
1. Launch new container
2. Stop the container
3. Remove the container
4. Start the container
5. List images
6. List all containers
7. Exit
""")
        choice = input("Enter your Choice: ")
        if choice == "1":
            name = input("Enter name of container: ")
            image = input("Enter the name of image: ")
            cmd = f"docker run -dit --name={name} {image}"
        elif choice == "2":
            name = input("Enter name of container: ")
            cmd = f"docker stop {name}"
        elif choice == "3":
            name = input("Enter name of container: ")
            cmd = f"docker rm -f {name}"
        elif choice == "4":
            name = input("Enter name of container: ")
            cmd = f"docker start {name}"
        elif choice == "5":
            cmd = "docker images"
        elif choice == "6":
            cmd = "docker ps -a"
        elif choice == "7":
            print("Exiting Docker menu.")
            break
        else:
            print("Enter proper option")
            continue

        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
        print(stderr.read().decode())

    client.close()

if __name__ == "__main__":
    docker_menu_ssh() 
