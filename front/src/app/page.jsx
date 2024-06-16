"use client";
import React, { useState, useEffect } from "react";
import { Button } from "@mui/material";
import AOS from "aos"; // 追加
import "aos/dist/aos.css"; // 追加

AOS.init();

export default function profile() {
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

  const onSelect = (image) => {
    setSelectedImage(image);
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
    <div>
      <h1 style={{ marginLeft: "520px", color: "black" }}>Home</h1>
      <div style={{ margin: "15px" }}></div>
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
              data-aos="fade-in"
              data-aos-delay="50"
              data-aos-duration="1000"
              variant="outlined"
              style={{ width: "250px", height: "250px" }}
              onClick={() => onSelect(image)}
            >
              <img
                style={{
                  width: "100%", // 画像の幅をボタンの幅に合わせます
                  height: "100%", // 画像の高さをボタンの高さに合わせます
                  objectFit: "cover", // 画像を切り取りながらアスペクト比を保持してボタンにフィットさせます
                }}
                src={image.urls.genImgUrl}
              />
            </Button>
          </div>
        ))}
      </div>
    </div>
  );
};

const ImageDetail = ({ image, onBack }) => {
  return (
    <div style={{ textAlign: "center" }}>
      <h1
        style={{
          marginTop: "30px",
          backgroundColor: "#edf6f9",
          color: "black",
          width: "200px",
          textAlign: "center",
          marginTop: "50px",
          marginLeft: "475px",
        }}
      >
        画像詳細
      </h1>
      <div
        style={{
          marginTop: "150px",
          display: "flex",
          justifyContent: "center",
          flexWrap: "wrap",
          gap: "100px",
          alignItems: "center",
        }}
      >
        <div>
          <img
            src={image.urls.orgImgUrl}
            style={{
              maxWidth: "100%",
              width: "400px",
              height: "400px",
            }}
          />
          <p style={{ color: "black" }}>オリジナル画像</p>
        </div>
        <div>
          <img
            src={image.urls.genImgUrl}
            style={{
              maxWidth: "100%",
              width: "400px",
              height: "400px",
            }}
          />
          <p style={{ color: "black" }}>生成画像</p>
        </div>
        <Button
          onClick={onBack}
          style={{
            textAlign: "center",
            width: "100px",
            height: "50px",
            marginLeft: "200px",
            marginRight: "200px",
            border: "solid",
          }}
        >
          Back
        </Button>
      </div>
    </div>
  );
};
