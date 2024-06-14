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

const drawerWidth = 240;

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
            <Box sx={{
                overflow: "auto", backgloudColor: subColor,

            }}>
                <List>
                    {["Inbox", "Starred", "Send email", "Drafts"].map((text, index) => (
                        <ListItem key={text} disablePadding>
                            <ListItemButton>
                                <ListItemIcon>
                                    {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
                                </ListItemIcon>
                                <Link href="/page1" underline="none" color="inherit">
                                    Page1
                                </Link>
                            </ListItemButton>
                        </ListItem>
                    ))}
                </List>
            </Box>
        </Drawer>
    );
};

export default SideBar;