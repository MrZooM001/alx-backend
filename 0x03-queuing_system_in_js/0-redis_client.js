import { createClient } from 'redis';

const redisClient = createClient({ legacyMode: true });

redisClient.on('connect', () => console.log('Redis client connected to the server'));
redisClient.on('error', (error) => {
    console.log('Redis client not connected to the server: ', error.message);
});

redisClient.connect().catch(console.error);
