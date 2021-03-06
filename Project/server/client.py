# Client.py
# SENG 299 chatroom project

import sys, socket, random, os, select

class Client():
    def __init__(self):
        ##
        ## instance of Client stores info:
        ##		ip - user's IP address
        ##		alias - user's current alias
        ## when new Client first created, by default they are assigned an alias of a random alphanumeric string
        ##
        self.ip = socket.gethostbyname(socket.gethostname())
        #self.alias = os.urandom(16)
        #self.port = random.randint(5000, 90000)
        self.port = 9999 #int(sys.argv[1])
        self.host = socket.gethostname()

        server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_conn.connect((self.host, self.port))

        list_sockets = [sys.stdin, server_conn]
        server_conn.sendall("/connect general")
    # def changeAlias(newAlias):     - update user alias

    ## listen to receive messages
        while True:
            read_sockets, write_sockets, error_sockets = select.select(list_sockets, [], [])
            for sock in read_sockets:
                if sock is server_conn:
                    msg = sock.recv(1024)
                    print(msg)

                else:
                    characters = raw_input("> ")
                    server_conn.sendall(characters)
                    print ('\033[A                             \033[A') #print ("\033[1A[\033[2K")



def main():

	client = Client()

if __name__ == "__main__":
	main()
