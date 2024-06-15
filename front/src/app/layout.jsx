"use client";

import Layout from "@/component/Layout";
import { AuthProvider } from "@/context/AuthContext";
import { ThemeProvider, Typography, createTheme } from "@mui/material";
import { SnackbarProvider } from "notistack";
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
    router.prefetch("/search");
    router.prefetch("/about");
  }, []);

  return (
    <html>
      <body style={{ margin: "0", backgroundColor: "#caf0f8" }}>
        <ThemeProvider theme={theme}>
          <AuthProvider>
            <Typography color="white" component="div">
              <Layout>
                <SnackbarProvider
                  anchorOrigin={{
                    vertical: "bottom",
                    horizontal: "right",
                  }}
                  maxSnack={3}
                  style={{ maxWidth: 300 }}
                />
                {children}
              </Layout>
            </Typography>
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
