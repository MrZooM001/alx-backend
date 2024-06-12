import { createQueue } from 'kue';

const queue = createQueue({ name: 'push_notification_code' });

const jobData = {
  phoneNumber: "+202-333-6666",
  message: "Welcome Welcome to hotel transylvania",
}

const job = queue.create('push_notification_code', jobData);

job.on('complete', () => {
  console.log('Notification job completed');
});

job.on('failed', (error) => {
  console.log('Notification job failed');
});

job.save((error) => {
  if (error) {
    console.log(error);
    return;
  }
  console.log('Notification job created:', job.id);
});
