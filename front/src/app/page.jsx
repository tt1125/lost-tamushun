"use client";
import React, { useState, useEffect } from "react";
import { Button } from "@mui/material";

export default function Home() {
  const [data, setData] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);

  const fetchData = () => {
    fetch("/fallbackData.json")
      .then((response) => response.json())
      .then((data) => setData(data));
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSelectImage = (image) => {
    setSelectedImage(image);
  };

  const handleBack = () => {
    setSelectedImage(null);
  };

  return (
    <div>
      {selectedImage ? (
        <ImageDetail image={selectedImage} onBack={handleBack} />
      ) : (
        <ImageList data={data} onSelect={handleSelectImage} />
      )}
    </div>
  );
}

const ImageList = ({ data, onSelect }) => {
  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        alignItems: "center",
        gap: "70px",
        overflow: "hidden",
      }}
    >
      {data.map((image, index) => (
        <div key={index}>
          <Button
            variant="outlined"
            style={{ width: "250px", height: "250px" }}
            onClick={() => onSelect(image)}
          >
            <img src={image.urls.small} alt={image.description} />
          </Button>
        </div>
      ))}
    </div>
  );
};

const ImageDetail = ({ image, onBack }) => {
  return (
    <div style={{ textAlign: "center" }}>
      <Button onClick={onBack}>Back</Button>
      <div>
        <img
          src={image.urls.full}
          alt={image.description}
          style={{ maxWidth: "100%" }}
        />
        <p>{image.description}</p>
      </div>
    </div>
  );
};
