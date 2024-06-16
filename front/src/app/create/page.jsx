"use client";
import React, { useState } from "react";
import {
  TextField,
  Button,
  Box,
  InputLabel,
  MenuItem,
  FormControl,
  Select,
} from "@mui/material";
import SetImg from "@/component/SetImg";
import { enqueueSnackbar } from "notistack";
import Upload from "@/fetch/upload";
import FetchPost from "@/fetch/post";
import { useAuth } from "@/context/AuthContext";

export default function Create() {
  const upload = new Upload();
  const [option, setOption] = useState("");
  const [uploadImg, setUploadImg] = useState(null);
  const [loading, setLoading] = useState(false);
  const [imageUrl, setImageUrl] = useState(null); // アップロードされた画像のURLを保存するステート

  const handleOptionChange = (event) => {
    setOption(event.target.value);
  };

  const handleFileChange = (event) => {
    setUploadImg(event.target.files[0]);
  };

  console.log("setUploadImg", uploadImg);

  const handleSubmit = async () => {
    console.log("uploadImg", uploadImg);
    if (!uploadImg) {
      enqueueSnackbar("画像を選択してください", { variant: "error" });
      return;
    }
    upload.uploadImg(uploadImg , option);


    setLoading(true);
    const uploader = new Upload();
    try {
      const url = await uploader.uploadImg(uploadImg);
      setImageUrl(url);
      enqueueSnackbar("画像がアップロードされました", { variant: "success" });
    } catch (error) {
      enqueueSnackbar("画像のアップロードに失敗しました", { variant: "error" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        flexDirection: "column",
        // 追加: コンテンツを縦に並べる
      }}
    >

      <SetImg
        file={uploadImg}
        disabled={loading}
        handleFileChange={handleFileChange}
      />
      <div
        style={{
          display: "flex", // 変更: inline-BLOCKからflexへ
          flexDirection: "column", // 追加: コンテンツを縦に並べる
          alignItems: "center",
          margin: "30px", // 追加: 水平方向の中央揃え
        }}
      >
        <Box>
          <FormControl style={{ width: "200px", marginTop: "30px" }}>
            <InputLabel id="demo-simple-select-label">Option</InputLabel>
            <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              value={option}
              label="世界の選択"
              onChange={handleOptionChange}
            >
              <MenuItem value={"harry_potter"}>ハリーポッター</MenuItem>
              <MenuItem value={"disney"}>ディズニー</MenuItem>
              <MenuItem value={"gundam"}>ガンダム</MenuItem>
              <MenuItem value={"pokemon"}>ポケモン</MenuItem>
              <MenuItem value={"star_wars"}>スターウォーズ</MenuItem>
              <MenuItem value={"marvel"}>マーベル</MenuItem>
              <MenuItem value={"egipt"}>エジプト</MenuItem>

              
            </Select>
          </FormControl>
        </Box>
        <Button
          style={{
            border: "2px solid black",
            width: "200px",
            marginTop: "30px",
          }}
          onClick={handleSubmit}
          disabled={loading}
        >
          送信
        </Button>
        {imageUrl && (
          <Box mt={4}>
            <img src={imageUrl} alt="Uploaded" style={{ width: "100%" }} />
          </Box>
        )}
      </div>
    </div>
  );
}
