import { createClient } from 'redis';
import { print } from "redis";

const redisClient = createClient({ legacyMode: true });

redisClient.on('connect', () => console.log('Redis client connected to the server'));
redisClient.on('error', (error) => {
  console.log('Redis client not connected to the server: ', error.message);
});

redisClient.connect().catch(console.error);

const hashKey = 'HolbertonSchools';
const hashValues = {
  'Portland': '50',
  'Seattle': '80',
  'New York': '20',
  'Bogota': '20',
  'Cali': '40',
  'Paris': '2'
};

const storeHashes = () => {
  Object.entries(hashValues).forEach(([key, value]) => {
    redisClient.hSet(hashKey, key, value, print)
  });
}

const getAllHashes = () => {
  redisClient.hGetAll(hashKey, (error, result) => {
    if (error) console.error(error);
    const data = Object.assign({}, result);
    console.log(data);
  });
}

storeHashes();
getAllHashes();
