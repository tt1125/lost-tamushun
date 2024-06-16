"use client";
import React, { useState, useEffect } from "react";
import { Button } from "@mui/material";

export default function Home() {
  // dataを空の配列で初期化
  const [data, setData] = useState([]);

  const fetchData = () => {
    // 'public' ディレクトリからデータを取得するようにパスを修正
    fetch("/fallbackData.json")
      .then((response) => response.json())
      .then((data) => setData(data));
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div>
      <h1 style={{ marginLeft: "520px" }}>Home</h1>
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
              variant="outlined"
              style={{ width: "250px", height: "250px" }}
              onClick={() => onSelect(image)}
            >
              <img src={image.urls.genImgUrl} />
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
          <p>オリジナル画像</p>
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
          <p>生成画像</p>
        </div>
        <Button
          onClick={onBack}
          style={{
            textAlign: "center",
            width: "100px",
            height: "50px",
            marginLeft: "200px",
            marginRight: "200px",
          }}
        >
          Back
        </Button>
      </div>
    </div>
  );
};

