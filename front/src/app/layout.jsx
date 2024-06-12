import { AuthProvider } from "@/context/AuthContext";
import { ThemeProvider, createTheme } from "@mui/material";

export default function RootLayout({ children }) {
  // const theme = createTheme({
  //   palette: {
  //     primary: {
  //       main: mainColor
  //     },
  //     secondary: {
  //       main: subColor

  //     },
  //   },
  // });

  return (
    <html>
      <body>
        {/* <ThemeProvider theme={theme}> */}
        <AuthProvider>{children}</AuthProvider>
        {/* </ThemeProvider> */}
      </body>
    </html>
  );
}
