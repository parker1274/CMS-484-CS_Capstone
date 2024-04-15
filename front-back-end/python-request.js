const { spawn } = require('child_process');
const path = require('path');


// Outcome prediction function
function predictionRequest(params) {
    return new Promise((resolve, reject) => {

        const pythonScriptPath = '/Users/jkran/code/school/CMS-484-CS_Capstone/python-code/run_models.py';

        // const pythonProcess = spawn('python3', ['./python-files/main.py', ...params]);

        console.log(pythonScriptPath)

        const pythonProcess = spawn('python3', [pythonScriptPath, ...params]);


        let outputData = '';
        pythonProcess.stdout.on('data', (data) => {
        outputData += data.toString();
        console.log(outputData)
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

// Actionable data function
function actionableDataRequest(params) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python3', ['./python-files/actionableData.py', ...params]);

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

// Team performance insight (tpi) function
function tpiRequest(params) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python3', ['./python-files/tpiData.py', ...params]);

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


module.exports = { predictionRequest, actionableDataRequest, tpiRequest };
