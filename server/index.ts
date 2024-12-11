// index.ts

import express, { Request, Response } from "express";

const app = express();
const PORT = process.env.PORT || 3001;

app.listen(PORT, () => {
    console.log(`Example app listening on port ${PORT}`);
});

app.get("/", (req: Request, res: Response) => {
    res.send("Hello World!");
});

app.get("/api", (req: Request, res: Response) => {
    res.json({ message: "Hello World! I'm JSON" });
});
