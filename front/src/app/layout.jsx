"use client";

import Layout from "@/component/Layout";
import { AuthProvider } from "@/context/AuthContext";
import { ThemeProvider, Typography, createTheme } from "@mui/material";
import { mainColor, subColor } from "@/global/global";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function RootLayout({ children }) {
  const theme = createTheme({
    palette: {
      primary: {
        main: mainColor,
      },
      secondary: {
        main: subColor,
      },
    },
  });
  const router = useRouter();

  useEffect(() => {
    router.prefetch("/");
    router.prefetch("/create");
    router.prefetch("/chat");
    router.prefetch("/about");
  }, []);

  return (
    <html>
      <body style={{ margin: "0", backgroundColor: "#caf0f8" }}>
        <ThemeProvider theme={theme}>
          <AuthProvider>
            <Typography color="white" component="div">
              <Layout>{children}</Layout>
            </Typography>
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
