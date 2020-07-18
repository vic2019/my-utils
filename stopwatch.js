const childProcess = require('child_process');

const startTime = new Date().getTime();

childProcess.exec(process.argv.slice(2).join(' '), (err, stdout, stderr) => {
  const endTime = new Date().getTime();
  err ? console.error(err) : null;
  stdout ? console.log(stdout) : null;
  stderr ? console.error(stderr) : null;
  console.log(`${endTime - startTime} milliseconds\n`);
});