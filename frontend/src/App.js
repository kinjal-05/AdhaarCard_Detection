import React, { useState } from "react";
import axios from "axios";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [message, setMessage] = useState("");
  const [extractedInfo, setExtractedInfo] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setPreview(URL.createObjectURL(file));
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select an image first!");
      return;
    }

    const formData = new FormData();
    formData.append("", selectedFile); // Ensure this key matches the Flask backend

    console.log("Submitting file:", selectedFile);
    setLoading(true); // Show the loading indicator

    try {
      const response = await axios.post("http://127.0.0.1:5000/extract-aadhaar", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      console.log(response.data); // Check the response data from the backend

      if (response.data.error) {
        alert("Error: " + response.data.error);
      } else {
        setMessage(response.data.message || "Extraction successful");
        setExtractedInfo(response.data);
      }
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Failed to process the image.");
      setMessage(error.response?.data?.error || "An error occurred");
    } finally {
      setLoading(false); // Hide the loading indicator
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h2>Aadhaar Card Upload</h2>

      {/* File input for image selection */}
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
      />
      <button onClick={handleUpload} style={{ marginLeft: "10px" }}>
        Upload
      </button>

      {/* Display uploaded image preview */}
      {preview && (
        <div>
          <h3>Uploaded Image:</h3>
          <img
            src={preview}
            alt="Uploaded Preview"
            style={{ maxWidth: "100%", border: "2px solid #ddd" }}
          />
        </div>
      )}

      {loading && <div className="alert alert-info mt-5">Processing...</div>}
      {/* {message && !loading && <div className="alert alert-info mt-5">{message}</div>} */}

      {/* Display extracted information if available */}
      {extractedInfo && !loading && (
        <div className="mt-5">
          {/* <h3>Extracted Information:</h3>
          <p><strong>Name:</strong> {extractedInfo.Name}</p>
          <p><strong>DOB:</strong> {extractedInfo.DOB}</p>
          <p><strong>Aadhaar Number:</strong> {extractedInfo["Aadhaar Number"]}</p> */}
          {extractedInfo.status === "exists" && (
            <p className="alert alert-warning">This Aadhaar ID is already registered.</p>
          )}
          {extractedInfo.status === "success" && (
            <p className="alert alert-success">Aadhaar ID successfully registered.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
