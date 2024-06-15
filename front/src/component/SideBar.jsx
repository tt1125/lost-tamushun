"use client";
import {
  Box,
  Drawer,
  Link,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  Toolbar,
} from "@mui/material";
import InboxIcon from "@mui/icons-material/MoveToInbox";
import MailIcon from "@mui/icons-material/Mail";
import React from "react";
import { subColor } from "@/global/global";
import CreateIcon from "@mui/icons-material/Create";
import HomeIcon from "@mui/icons-material/Home";
import PersonIcon from "@mui/icons-material/Person";
import InfoIcon from "@mui/icons-material/Info";
import Button from "@mui/material/Button";
import LogoutIcon from "@mui/icons-material/Logout";
import FetchUser from "@/fetch/user";
import { useRouter } from "next/navigation";
import ChatIcon from "@mui/icons-material/Chat";
import Icon from "./icon";

const fetchUser = new FetchUser();

const drawerWidth = 240;
const name = ["Home", "Create", "Profile", "Search", "About"];

const logoutClicked = () => {
  fetchUser.logout();
};

const SideBar = () => {
  const router = useRouter();
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: {
          width: drawerWidth,
          boxSizing: "border-box",
        },
      }}
    >
      <Toolbar />

      <Box
        sx={{
          overflow: "auto",
        }}
      >
        <Icon onClick={() => router.push("/profile")} />
        <List style={{ marginTop: "20px" }}>
          {[
            <HomeIcon />,
            <CreateIcon />,
            <PersonIcon />,
            <ChatIcon />,
            <InfoIcon />,
          ].map((text, index) => (
            <ListItem key={text} style={{ marginTop: "10px" }}>
              <ListItemButton>
                <ListItemIcon>
                  <div>
                    <div key={index}>{text}</div>
                  </div>
                  <Link
                    onClick={() => {
                      if (name[index] === "Home") {
                        router.push("/");
                      } else {
                        router.push("/" + name[index].toLowerCase());
                      }
                    }}
                    underline="none"
                    color="inherit"
                    style={{ marginLeft: "50px" }}
                  >
                    {name[index]}
                  </Link>
                </ListItemIcon>
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Box>
      <Box
        sx={{
          overflow: "auto",
        }}
      >
        <List style={{ marginTop: "250px" }}>
          <ListItem>
            <ListItemButton onClick={logoutClicked}>
              <LogoutIcon style={{ color: "inherit" }} />
              <Link
                underline="none"
                style={{
                  marginLeft: "50px",
                  color: "inherit",
                }}
              >
                Logout
              </Link>
            </ListItemButton>
          </ListItem>
        </List>
      </Box>
    </Drawer>
  );
};

export default SideBar;
