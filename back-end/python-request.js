const { spawn } = require('child_process');

function predictionRequest(params) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python3', ['./main.py', ...params]);

    let outputData = '';
    pythonProcess.stdout.on('data', (data) => {
      outputData += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
      reject(new Error(`stderr: ${data}`));  // Reject the promise on error
    });

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        try {
          const jsonData = JSON.parse(outputData);
          console.log('Result from Python:', jsonData);
          resolve(jsonData);  // Resolve the promise with the JSON data
        } catch (error) {
          reject(new Error('Failed to parse JSON output'));
        }
      } else {
        reject(new Error(`Python script exited with code ${code}`));
      }
    });
  });
}

module.exports = { predictionRequest };
