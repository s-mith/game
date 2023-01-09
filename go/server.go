package main

import (
	"fmt"
	"net"
	"strconv"
	"strings"
	"sync"
)

type user struct {
	socket   net.Conn
	nickname string
	address  net.Addr
}

func (u *user) nick(nickname string) {
	u.nickname = nickname
}

func (u *user) String() string {
	return fmt.Sprintf("%s (%s)", u.nickname, u.address)
}

type ChatServer struct {
	host   string
	port   int
	server net.Listener
	users  map[net.Conn]*user
	lock   sync.RWMutex
	wg     sync.WaitGroup
}

func (cs *ChatServer) broadcast(message string) {
	cs.lock.RLock()
	defer cs.lock.RUnlock()
	for client, _ := range cs.users {
		client.Write([]byte(message))
	}
}

func (cs *ChatServer) message(message string, client net.Conn) {
	cs.lock.RLock()
	defer cs.lock.RUnlock()
	for c, _ := range cs.users {
		if c != client {
			c.Write([]byte(message))
		}
	}
}

func (cs *ChatServer) kill(client net.Conn) {
	cs.lock.Lock()
	defer cs.lock.Unlock()
	client.Close()
	nickname := cs.users[client].nickname
	delete(cs.users, client)
	cs.broadcast(nickname + " left the chat!")
}

func (cs *ChatServer) handle(client net.Conn) {
	defer cs.wg.Done()
	defer cs.kill(client)
	for {

		buf := make([]byte, 1024)
		n, err := client.Read(buf)
		if err != nil {
			break
		}
		message := strings.TrimSpace(string(buf[:n]))
		if message == "" {
			continue
		}
		if message[0] == '/' {
			if message == "/quit" {
				break
			} else if strings.HasPrefix(message, "/nick") {
				nickname := strings.Split(message, " ")[1]
				cs.users[client].nick(nickname)
				client.Write([]byte("Nickname successfully changed to " + nickname))
			} else {
				client.Write([]byte("Invalid command!"))
			}
		} else {
			cs.message(message, client)
		}
	}
	cs.kill(client)
}

func (cs *ChatServer) receive() {
	defer cs.server.Close()
	for {
		client, err := cs.server.Accept()
		if err != nil {
			break
		}
		fmt.Println("Connected with",
			client.RemoteAddr())
		cs.wg.Add(1)
		client.Write([]byte("NICK"))
		buf := make([]byte, 1024)
		n, err := client.Read(buf)
		if err != nil {
			cs.kill(client)
			break
		}
		nickname := strings.TrimSpace(string(buf[:n]))
		// for key in cs.users {
		for key, user := range cs.users {
			if key == client {
				// remove the client from cs.users
				delete(cs.users, key)
			}
			if user.nickname == nickname {
				client.Write([]byte("Nickname already taken!"))
				cs.kill(client)
				break
			}
		}

		cs.users[client] = &user{client, nickname, client.RemoteAddr()}
		fmt.Println("Nickname of client is", nickname, "!")
		client.Write([]byte("Connected to the server!"))
		cs.broadcast(nickname + " joined the chat!")
		client.Write([]byte("Type your message:"))
		go cs.handle(client)
	}
}

func (cs *ChatServer) start() {
	fmt.Println("Server Started!")
	cs.wg.Add(1)
	go cs.receive()
	cs.wg.Wait()
}

func main() {
	fmt.Print("Enter host: ")
	var host string
	fmt.Scanln(&host)
	fmt.Print("Enter port: ")
	var port int
	fmt.Scanln(&port)
	server, err := net.Listen("tcp", host+":"+strconv.Itoa(port))
	if err != nil {
		fmt.Println(err)
		return
	}
	cs := &ChatServer{
		host:   host,
		port:   port,
		server: server,
		users:  make(map[net.Conn]*user),
	}
	cs.start()
}
