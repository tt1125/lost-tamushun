"use client";

import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import { useState } from "react";
import Link from "@mui/material/Link";
import FetchUser from "@/fetch/user";
import { useRouter } from "next/navigation";

export default function Login() {
  const fetchUser = new FetchUser();

  const router = useRouter();

  const [createUserShown, setCreateUserShown] = useState(false);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");

  const changeName = (e) => setName(e.target.value);
  const changeEmail = (e) => setEmail(e.target.value);
  const changePassword = (e) => setPassword(e.target.value);
  //変える？

  const changeUserShown = () => {
    setCreateUserShown(!createUserShown);
    setEmail("");
    setPassword("");
    setName("");
  };

  const loginClicked = () => {
    fetchUser.loginWithEmail(email, password);
    router.push("/");
  };

  const signUpClicked = () => {
    fetchUser.createUser(name, email, password);
    router.push("/");
  };

  return (
    <main
      style={{
        height: "100vh",
        width: "100%",
        backgroundColor: "gray",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {!createUserShown ? (
        <div
          style={{
            textAlign: "center",
            backgroundColor: "white",
            padding: "70px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <h1>ログイン</h1>
          <TextField
            value={email}
            id="outlined-basic"
            label="メールアドレス"
            variant="outlined"
            sx={{ width: "250px", margin: "10px" }}
            onChange={changeEmail}
          />
          <TextField
            value={password}
            id="outlined-basic"
            label="パスワード"
            variant="outlined"
            sx={{ width: "250px", margin: "10px" }}
            onChange={changePassword}
          />
          <Button
            onClick={loginClicked}
            variant="contained"
            style={{ width: "200px", margin: "10px" }}
          >
            ログイン
          </Button>
          <Link onClick={changeUserShown} style={{ marginTop: "30px" }} sx={{ ":hover": { cursor: "pointer" } }}>
            新規登録はこちら
          </Link>
        </div>
      ) : (
        <div
          style={{
            textAlign: "center",
            backgroundColor: "white",
            padding: "70px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <h1>新規登録</h1>
          <TextField
            value={name}
            id="outlined-basic"
            label="ユーザー名"
            variant="outlined"
            sx={{ width: "250px", margin: "10px" }}
            onChange={changeName}
          />
          <TextField
            value={email}
            id="outlined-basic"
            label="メールアドレス"
            variant="outlined"
            sx={{ width: "250px", margin: "10px" }}
            onChange={changeEmail}
          />
          <TextField
            value={password}
            id="outlined-basic"
            label="パスワード"
            variant="outlined"
            sx={{ width: "250px", margin: "10px" }}
            onChange={changePassword}
          />
          <Button
            onClick={signUpClicked} //ここ押したらユーザーの新規作成
            variant="contained"
            style={{ width: "200px", margin: "10px" }}
          >
            登録
          </Button>
          <Link onClick={changeUserShown} style={{ marginTop: "30px" }} sx={{ ":hover": { cursor: "pointer" } }}>
            ログイン画面に戻る
          </Link>
        </div>
      )}
    </main>
  );
}
