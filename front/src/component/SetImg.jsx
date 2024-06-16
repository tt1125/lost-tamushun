import { Image } from "@mui/icons-material";
import { Button, Typography } from "@mui/material";

export default function SetImg({ file, disabled, handleFileChange }) {
  return (
    <div className="w-full">
      <Button
        variant="outlined"
        component="label"
        disabled={disabled}
        sx={{
          minHeight: "400px",
          width: "700px",
          borderRadius: "20px",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Typography
          variant="body1"
          align="center"
          className="whitespace-pre-wrap overflow-y-scroll"
          sx={{ fontSize: "12px", fontWeight: "bold", scrollbarWidth: "none" }}
          component="div"
        >
          <div>
            <Image sx={{ fontSize: "100px" }} />
            {file ? (
              <div>
                {file.name}
                <br />
                {file.size}
              </div>
            ) : (
              <div>画像ファイルを選択</div>
            )}
          </div>
        </Typography>
        <input
          type="file"
          hidden
          multiple={false}
          onChange={handleFileChange}
        />
      </Button>
    </div>
  );
}
