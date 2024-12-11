//  App.tsx

import { useState, useEffect } from "react";
import "./App.css";

function App() {
    const [data, setData] = useState(null);
    const url = "http://localhost:3001";

    useEffect(() => {
        fetch(`${url}/api`)
            .then((res) => res.json())
            .then((data) => setData(data.message));
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
