import { createClient, print } from 'redis';

const redisClient = createClient({ legacyMode: true });

redisClient.on('connect', () => console.log('Redis client connected to the server'));
redisClient.on('error', (error) => {
    console.log('Redis client not connected to the server: ', error.message);
});

redisClient.connect().catch(console.error);

function setNewSchool(schoolName, value) {
    redisClient.set(schoolName, value, print);
};

function displaySchoolValue(schoolName) {
    redisClient.get(schoolName, (error, result) => {
        if (error) {
            console.log(error);
            return;
        }
        console.log(result);
    });
};

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
