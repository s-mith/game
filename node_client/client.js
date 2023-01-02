const net = require('net');
const prompt = require('prompt-sync')();

class ChatClient {
  constructor(host = 'localhost', port = 5000) {
    this.host = host;
    this.port = port;
    this.nickname = prompt('Choose a nickname: ');

    this.client = new net.Socket();
    this.client.connect(port, host, () => {
      console.log('Connected');
    });
  }

  receive() {
    this.client.on('data', data => {
      try {
        const message = data.toString();
        if (message === 'NICK') {
          this.client.write(this.nickname);
        } else if (message.startsWith('/nick')) {
          this.nickname = message.split()[1];
          console.log(`Your nickname has been changed to ${this.nickname}`);
        } else {
          console.log(message);
        }
      } catch (err) {
        console.log('An error occurred!');
        this.client.destroy();
      }
    });

    this.client.on('close', () => {
      console.log('Connection closed');
    });
  }

  write() {
    process.stdin.on('data', data => {
      const message = `${this.nickname}: ${data.toString().trim()}`;
      this.client.write(message);
    });
  }

  start() {
    this.receive();
    this.write();
  }
}

const host = prompt('Enter host: ');
const port = parseInt(prompt('Enter port: '), 10);

const client = new ChatClient(host, port);
client.start();