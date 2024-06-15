"use client";
import React, { useState } from "react";
import {
  Button,
  TextField,
  Box,
  Grid,
  Typography,
  Container,
} from "@mui/material";
import { getAuth } from "firebase/auth";
import FetchPost from "@/fetch/post";

export default function Search() {
  const fetchPost = new FetchPost();
  const [images, setImages] = useState([]);
  const [description, setDescription] = useState("");

  const handleSearch = async () => {
    // 固定値で画像のURLと説明を設定
    // const orgImgUrl = "https://picsum.photos/id/237/300/200";
    // const genImgUrl = "https://picsum.photos/id/238/300/200";
    // const desc = "This is a sample description.";
    const currentUser = getAuth().currentUser;
    const uid = currentUser?.uid;
    console.log("hoge");
    const posts = await fetchPost.fetchUserPosts(uid);
    const { orgImgUrl, genImgUrl, description } = posts[0];
    setImages([orgImgUrl, genImgUrl]);
    setDescription(description);
  };

  return (
    <Container
      maxWidth="sm"
      style={{
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
      }}
    >
      <Box
        flexGrow={1}
        display="flex"
        alignItems="center"
        justifyContent="center"
      >
        {images.length > 0 && (
          <Grid
            container
            spacing={2}
            justifyContent="center"
            alignItems="center"
          >
            {images.map((url, index) => (
              <Grid item xs={6} key={index}>
                <img
                  src={url}
                  alt={`Image ${index + 1}`}
                  style={{ width: "100%", height: "auto", borderRadius: "8px" }}
                />
              </Grid>
            ))}
            <Grid item xs={12}>
              <Typography variant="body1">{description}</Typography>
            </Grid>
          </Grid>
        )}
      </Box>

      <Box mb={4} textAlign="center">
        <TextField
          id="search-input"
          label="Search"
          variant="outlined"
          fullWidth
          margin="normal"
        />
        <Button variant="contained" color="primary" onClick={handleSearch}>
          Search
        </Button>
      </Box>
    </Container>
  );
}
