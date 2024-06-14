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

const drawerWidth = 240;
const name = ["Home", "Create", "Profile", "About"];

const SideBar = () => {
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
        <List>
          {[<HomeIcon />, <CreateIcon />, <PersonIcon />, <InfoIcon />].map(
            (text, index) => (
              <ListItem key={text} style={{ marginTop: "5px" }}>
                <ListItemButton>
                  <ListItemIcon>
                    <div>
                      <div key={index}>{text}</div>
                    </div>
                    <Link
                      href={name[index]}
                      underline="none"
                      color="inherit"
                      style={{ marginLeft: "50px" }}
                    >
                      {name[index]}
                    </Link>
                  </ListItemIcon>
                </ListItemButton>
              </ListItem>
            )
          )}
        </List>
      </Box>
      <Box
        sx={{
          overflow: "auto",
        }}
      >
        <List style={{ marginTop: "450px" }}>
          <ListItem>
            <ListItemButton>
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
