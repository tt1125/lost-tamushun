"use client";

import Layout from "@/component/Layout";
import { AuthProvider } from "@/context/AuthContext";
import { ThemeProvider, Typography, createTheme } from "@mui/material";
import { mainColor, subColor } from "@/global/global";

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

  return (
    <html>
      <body style={{ margin: "0", backgroundColor: "blue" }}>
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
