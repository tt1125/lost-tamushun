import Button from "@mui/material/Button"; // 正しいインポートパス

const Icon = () => {
  return (
    <Button
      sx={{
        display: "flex",
        justifyContent: "center", // 中央に配置
        alignItems: "center", // 中央に配置
        margin: "auto",
        width: "100px",
        height: "100px",
        borderRadius: "50px", // ボタンを円形に
        border: "2px solid black", // ボーダーを表示
        padding: "0", // パディングを0に
        overflow: "hidden", // はみ出た画像を隠す
        "&:hover": {
          // ホバー状態のスタイル
          borderColor: "red",
        },
      }}
    >
      <img
        src="/img.jpg"
        alt=""
        style={{ width: "100%", height: "100%", objectFit: "cover" }}
      />
    </Button>
  );
};

export default Icon;
