//  App.tsx

import { useState, useEffect } from "react";
import "./App.css";

type Message = { message: string };

function App(): JSX.Element {
    const [data, setData] = useState<string | null>(null);
    const url: string = "http://localhost:3001";

    useEffect(() => {
        fetch(`${url}/api`)
            .then((res) => res.json())
            .then((data: Message) => setData(data.message));
    }, []);

    return (
        <>
            <h1>Vite + React</h1>
            <div className="card">
                <p>{!data ? "Loading..." : data}</p>
            </div>
        </>
    );
}

export default App;
