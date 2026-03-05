import React, { useState, useEffect } from "react";

interface Message {
    text: string;
}

const App: React.FC = () => {
    const [message, setMessage] = useState<Message | null>(null);

    useEffect(() => {
        fetch("http://localhost:5000")
            .then((response) => response.text())
            .then((data) => setMessage({ text: data }));
    }, []);

    return (
        <div className="App">
            <h1>{message ? message.text : "Loading..."}</h1>
        </div>
    );
};

export default App;
