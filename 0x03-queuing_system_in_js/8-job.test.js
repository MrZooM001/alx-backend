import { createPushNotificationsJobs } from './8-job';
import { createQueue } from 'kue';
import { expect } from 'chai';

const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account'
  },
  {
    phoneNumber: '4153518781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4153518743',
    message: 'This is the code 4321 to verify your account'
  },
  {
    phoneNumber: '4153118782',
    message: 'This is the code 4321 to verify your account'
  },
  {
    phoneNumber: '4158718781',
    message: 'This is the code 4562 to verify your account'
  },
  {
    phoneNumber: '4153818782',
    message: 'This is the code 4321 to verify your account'
  },
];

describe('createPushNotificationsJobs', () => {
  let queue;

  before(() => {
    queue = createQueue({ name: 'push_notification_code_test' });
    queue.testMode.enter();
  });

  after(() => {
    queue.testMode.exit();
    queue.shutdown(1000, err => {
      if (err) {
        console.error('Error on Shutdown:', err);
      } else {
        console.log('Kue queue shutdown sucessfully');
      }
    });
  });

  afterEach(() => {
    queue.testMode.clear();
  });

  it('creating a job foreach input', () => {
    createPushNotificationsJobs(jobs, queue);
    queue.on('Job complete', (id, result) => {
      queue.testMode.jobs((error, jobs) => {
        if (error) {
          throw error;
        }
        expect(jobs.length).to.be.equal(6);
        jobs.forEach(job => {
          expect(job.type).to.be.equal('push_notification_code_3');
          expect(job.data.phoneNumber).to.be.defined;
          expect(job.data.message).to.be.defined;
        });
      });
    });
  });

  it('Throws an error if jobs argument is not Array', () => {
    expect(() => {
      createPushNotificationsJobs({}, queue);
    }).to.throw('Jobs is not an array');
  });
});
