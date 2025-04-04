import { useState } from "react";
import "./App.css";

async function getRecommendations(type: string, itemId: string) {
  try {
    const response = await fetch(
      `http://localhost:5000/api/recommendations/${type}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ item_id: itemId }),
      }
    );

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    const data = await response.json();
    return data.recommendations;
  } catch (error) {
    console.error("Failed to fetch recommendations:", error);
    return [];
  }
}

function App() {
  const [collabId, setCollabId] = useState<string>("");
  const [contentId, setContentId] = useState<string>("");
  const [collabRecommendations, setCollabRecommendations] = useState<string[]>(
    []
  );
  const [contentRecommendations, setContentRecommendations] = useState<
    string[]
  >([]);

  const fetchCollaborative = async () => {
    const result = await getRecommendations("collaborative", collabId);
    setCollabRecommendations(result);
  };

  const fetchContent = async () => {
    const result = await getRecommendations("content", contentId);
    setContentRecommendations(result);
  };

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <h2>Select Content IDs</h2>
      <div style={{ marginBottom: "20px" }}>
        <label>
          Collaborative Content ID:
          <input
            type="text"
            value={collabId}
            onChange={(e) => setCollabId(e.target.value)}
            style={{ margin: "0 10px" }}
          />
          <button onClick={fetchCollaborative}>
            Get Collaborative Recommendations
          </button>
        </label>
        <br />
        <br />
        <label>
          Content-Based Content ID:
          <input
            type="text"
            value={contentId}
            onChange={(e) => setContentId(e.target.value)}
            style={{ margin: "0 10px" }}
          />
          <button onClick={fetchContent}>Get Content Recommendations</button>
        </label>
      </div>

      <h2>Recommendations</h2>
      <table
        style={{
          margin: "0 auto",
          textAlign: "center",
          border: "1px solid #ddd",
        }}
      >
        <thead>
          <tr>
            <th></th>
            <th>Article 1</th>
            <th>Article 2</th>
            <th>Article 3</th>
            <th>Article 4</th>
            <th>Article 5</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Collaborative</td>
            {collabRecommendations.map((item, index) => (
              <td key={index}>{item}</td>
            ))}
          </tr>
          <tr>
            <td>Content</td>
            {contentRecommendations.map((item, index) => (
              <td key={index}>{item}</td>
            ))}
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default App;
