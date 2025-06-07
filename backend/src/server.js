const express = require("express");
const cors = require("cors");
const uploadRoute = require("./routes/uploadRoute");
const searchRoute = require("./routes/searchRoute");
const labelRoute = require("./routes/labelRoute"); // NEW
const path = require("path");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());
app.use("/uploads", express.static(path.join(__dirname, "public/uploads")));

app.use("/api/upload", uploadRoute);
app.use("/api/search", searchRoute);
app.use("/api/labels", labelRoute);

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));