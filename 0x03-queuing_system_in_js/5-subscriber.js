import { createClient } from 'redis';
import { print } from 'redis';

const redisSubscriber = createClient({ legacyMode: true });

redisSubscriber.on('connect', () => console.log('Redis client connected to the server'));
redisSubscriber.on('error', (error) => {
  console.log('Redis client not connected to the server:', error.message);
});

redisSubscriber.subscribe('holberton school channel');

redisSubscriber.on('message', (channel, message) => {
  console.log(message);
  if (message === "KILL_SERVER") {
    redisSubscriber.unsubscribe();
    redisSubscriber.quit();
  }
});
