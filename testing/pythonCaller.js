const { spawn } = require('child_process');

function predictionRequest() {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python3', ['./simpleScript.py']);

    let outputData = '';
    pythonProcess.stdout.on('data', (data) => {
      outputData += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        try {
          const jsonData = JSON.parse(outputData);
          resolve(jsonData);
        } catch (error) {
          reject('Failed to parse JSON output');
        }
      } else {
        reject(`Python script exited with code ${code}`);
      }
    });
  });
}

module.exports = { predictionRequest };
