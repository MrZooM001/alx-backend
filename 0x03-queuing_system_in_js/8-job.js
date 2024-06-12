const createPushNotificationsJobs = (jobs, queue) => {
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  jobs.forEach(job => {
    const notifyJob = queue.create('push_notification_code_3', job);

    notifyJob.on('enqueue', () => {
      console.log('Notification job created:', notifyJob.id);
    });

    notifyJob.on('complete', () => {
      console.log(`Notification job ${notifyJob.id} completed`);
    });

    notifyJob.on('failed', (error) => {
      console.log(`Notification job ${notifyJob.id} failed: ${error}`);
    });

    notifyJob.on('progress', (progress, data) => {
      console.log(`Notification job ${notifyJob.id} ${progress}% complete`);
    });

    notifyJob.save();
  });
};

export default createPushNotificationsJobs;
