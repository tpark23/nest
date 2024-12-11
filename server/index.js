// backend/index.js

const express = require("express");
const app = express();
const port = 3001;

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`);
});

app.get("/", (req, res) => {
    res.send("Hello World!");
});

app.get("/api", (req, res) => {
    res.json({ message: "Hello World! I'm JSON" });
});
