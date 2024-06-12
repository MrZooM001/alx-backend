const express = require('express');
import { createClient } from 'redis';
import { promisify } from 'util';
import { createQueue } from 'kue';

const client = createClient();
const queue = createQueue();
const app = express();

client.on('connect', () => {
    console.log('Redis client connected to the server');
});

client.on('error', (error) => {
    console.error('Redis client not connected to the server:', error);
});


const reserveSeat = (number) => {
    client.set('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
    const getAsync = promisify(client.get).bind(client);
    const seats = await getAsync('available_seats');
    return parseInt(seats);
};

reserveSeat(50);
let reservationEnabled = true;

app.get('/available_seats', async (req, res) => {
    const seats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats: seats });
});

app.get('/reserve_seat', (req, res) => {
    if (!reservationEnabled) {
        return res.json({ status: 'Reservation are blocked' });
    }

    const job = queue.create('reserve_seat', {}).save((err) => {
        if (!err) {
            return res.json({ status: 'Reservation in process' });
        }
        return res.json({ status: 'Reservation failed' });
    });

    job.on('complete', () => {
        console.log(`Seat reservation job ${job.id} completed`);
    }).on('failed', (errMessage) => {
        console.log(`Seat reservation job ${job.id} failed: ${errMessage}`);
    });
});

app.get('/process', (req, res) => {
    res.json({ status: 'Queue processing' });
    queue.process('reserve_seat', async (job, done) => {
        const seats = await getCurrentAvailableSeats();
        if (seats > 0) {
            reserveSeat(seats - 1);
            if (seats - 1 === 0) {
                reservationEnabled = false;
            }
            done();
        } else {
            done(new Error('Not enough seats available'));
        }
    });
});

app.listen(1245, () => {
    console.log(`Express server listening on port 1245`);
});
