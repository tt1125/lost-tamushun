'use client'

import Layout from "@/component/Layout";
import { AuthProvider } from "@/context/AuthContext";
import { ThemeProvider, createTheme } from "@mui/material";
import { mainColor, subColor } from "@/global/global"

export default function RootLayout({ children }) {
  const theme = createTheme({
    palette: {
      primary: {
        main: mainColor
      },
      secondary: {
        main: subColor

      },
    },
  });

  return (
    <html >
      <body style={{ margin: "0", backgroundColor: mainColor }}>
        <ThemeProvider theme={theme}>
          <AuthProvider>
            <Layout>
              {children}
            </Layout>
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
