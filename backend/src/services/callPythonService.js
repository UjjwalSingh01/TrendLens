const axios = require("axios");
const FormData = require("form-data");
const fs = require("fs");
const path = require("path"); // ADDED

module.exports = async (filePath) => {
  try {
    const form = new FormData();
    form.append("file", fs.createReadStream(filePath), {
      filename: path.basename(filePath),
      contentType: "image/jpeg"
    });

    const response = await axios.post(
      "http://localhost:8000/process",
      form,
      {
        headers: {
          ...form.getHeaders(),
          "Content-Type": "multipart/form-data"
        },
        timeout: 30000
      }
    );

    return response.data;
  } catch (err) {
    throw new Error(
      err.response?.data?.detail || 
      err.message || 
      "Python service error"
    );
  }
};