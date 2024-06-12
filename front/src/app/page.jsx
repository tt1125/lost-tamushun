"use client";

import FetchUser from "@/fetch/user";
import { Button } from "@mui/material";

export default function Home() {
  const fetchUser = new FetchUser();

  const logoutClicked = () => {
    fetchUser.logout();
  };

  return (
    <main>
      lost tamushun home
      <Button onClick={logoutClicked}>ログアウト</Button>
    </main>
  );
}
