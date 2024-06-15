"use client";
import Icon from "../../component/icon";
import React, { useState, useEffect } from "react";
import { Button } from "@mui/material";
export default function profile() {
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
    <div style={{ margin: "10px" }}>
      <Icon />
      <div
        style={{
          display: "flex", // gridからflexに変更
          flexWrap: "wrap", // 複数行に対応
          justifyContent: "center", // 中央揃え
          alignItems: "center", // アイテムを中央揃え
          margin: "10px",
          gap: "50px", // アイテム間の隙間
        }}
      >
        {data.map((image, index) => (
          <div key={index}>
            <Button
              variant="outlined"
              style={{ width: "250px", height: "250px" }}
            >
              <img src={image.urls.small} alt={image.description} />
            </Button>
          </div>
        ))}
      </div>
    </div>
  );
}
