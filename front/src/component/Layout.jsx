"use client";

import { useState } from "react";
import Box from "@mui/material/Box";
import { Drawer } from "@mui/material";
import SideBar from "./SideBar";

export default function Layout({ children }) {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  const toggleDrawer = (isOpen) => {
    setIsDrawerOpen(isOpen);
  };

  return (
    <Box
      style={{
        display: "flex",
        width: "100vw",
        height: "100vh",
      }}
    >
      <div
        style={{
          position: "fixed",
          width: "100vw",
          height: "100vh",
        }}
      ></div>
      <SideBar />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          height: "100%",
          position: "relative",
        }}
      >
        <div className="w-full">{children}</div>
      </Box>
    </Box>
  );
}
