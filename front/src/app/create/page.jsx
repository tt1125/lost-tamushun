"use client";
import React from "react";
import { TextField } from "@mui/material";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import { useState } from "react";
import SetImg from "@/component/SetImg";

export default function create() {
  const [age, setAge] = useState("");
  const [uploadImg, setUploadImg] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    setAge(event.target.value);
  };

  const handleFileChange = (event) => {
    setUploadImg(event.target.files[0]);
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        flexDirection: "column", // 追加: コンテンツを縦に並べる
      }}
    >
      <SetImg
        file={uploadImg}
        disabled={loading}
        handleFileChange={handleFileChange}
      />
      <TextField
        id="outlined-multiline-static"
        label="Multiline"
        multiline
        rows={4}
        defaultValue="Default Value"
        style={{ width: "500px", margin: "20px 0" }} // marginを追加して間隔を設定
      />
      <div
        style={{
          display: "flex", // 変更: inline-BLOCKからflexへ
          flexDirection: "column", // 追加: コンテンツを縦に並べる
          alignItems: "center", // 追加: 水平方向の中央揃え
        }}
      >
        <Box>
          <FormControl style={{ width: "200px", marginTop: "10px" }}>
            <InputLabel id="demo-simple-select-label">Age</InputLabel>
            <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              value={age}
              label="Age"
              onChange={handleChange}
            >
              <MenuItem value={10}>Ten</MenuItem>
              <MenuItem value={20}>Twenty</MenuItem>
              <MenuItem value={30}>Thirty</MenuItem>
            </Select>
          </FormControl>
        </Box>
        <Button
          style={{
            border: "2px solid black",
            width: "200px",
            marginTop: "10px",
          }}
        >
          送信
        </Button>
      </div>
    </div>
  );
}
