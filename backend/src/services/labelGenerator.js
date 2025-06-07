const { spawn } = require("child_process");

module.exports.generateLabels = () => {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn("python", ["./python_scripts/generate_labels.py"]);
    
    pythonProcess.stdout.on("data", (data) => {
      console.log(`Python: ${data}`);
    });

    pythonProcess.stderr.on("data", (data) => {
      console.error(`Python Error: ${data}`);
    });

    pythonProcess.on("close", (code) => {
      if (code === 0) resolve();
      else reject(new Error(`Process exited with code ${code}`));
    });
  });
};