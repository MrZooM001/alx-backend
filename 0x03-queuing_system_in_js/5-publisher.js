import { createClient } from 'redis';
import { print } from 'redis';

const publisherClient = createClient({ legacyMode: true });

publisherClient.on('connect', () => console.log('Redis client connected to the server'));
publisherClient.on('error', (error) => {
  console.log('Redis client not connected to the server:', error.message);
});

const publishMessage = (message, time) => {
  setTimeout(() => {
    console.log('About to send', message);
    publisherClient.publish('holberton school channel', message);
  }, time);
}

publishMessage("Holberton Student #1 starts course", 100);
publishMessage("Holberton Student #2 starts course", 200);
publishMessage("KILL_SERVER", 300);
publishMessage("Holberton Student #3 starts course", 400);
