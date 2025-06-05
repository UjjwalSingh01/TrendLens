const axios = require("axios");
const fs = require("fs");
const FormData = require("form-data");

module.exports = async function callPythonService(filePath) {
  const form = new FormData();
  form.append("file", fs.createReadStream(filePath));
  
  const response = await axios.post(
    process.env.PYTHON_SERVICE_URL + "/process", 
    form,
    { headers: form.getHeaders() }
  );
  
  return response.data;
};