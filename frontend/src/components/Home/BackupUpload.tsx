import React, { useEffect, useState, useRef } from "react";
import { createTheme } from "@mui/material/styles";
import { makeStyles } from "@mui/styles";
import {
  Button,
  TextField,
  CssBaseline,
  Box,
  Typography,
  Container,
  Avatar,
  CircularProgress,
} from "@mui/material";
import { CloudUploadOutlined } from "@mui/icons-material";
import { red, blue, green, lightBlue, orange } from "@mui/material/colors";
import axios from "axios";
import { APIS } from "../../config";
const theme = createTheme({
  palette: {
    primary: blue,
    secondary: red,
    success: green,
    error: red,
    info: lightBlue,
    warning: orange,
  },
});
const socket = new WebSocket("ws://localhost:8080");
socket.addEventListener("open", () => {
  console.log("WebSocket connection is open");
});
socket.addEventListener("message", (event) => {
  const blob = event.data;
  const reader = new FileReader();
  reader.onload = function () {
    const text = reader.result;
    // Handle the received text from the backend
    console.log(text);
  };
  reader.readAsText(blob);
  // Handle the received output from the backend
});
const useStyles = makeStyles({
  paper: {
    marginTop: theme.spacing(2),
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: "100%", // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
  success: {
    color: "green",
    textAlign: "center",
  },
  error: {
    color: "red",
    textAlign: "center",
  },
  searchBar: {
    height: "30px",
    width: "200px",
    [theme.breakpoints.up("sm")]: {
      height: "40px",
    },
  },
});

const BackupUpload = (props: { location: { state: any } }) => {
  const reload = (props.location && props.location.state) || {};
  const [flag, setFlag] = useState(false);
  const [message, setMessage] = useState("");

  const classes = useStyles();
  const [loading, setLoading] = useState(false);
  const [buttonState, setButtonState] = useState(false);

  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {}, [reload.time]);

  const handleChange = (e: any) => {
    switch (e.target.name) {
      case "file":
        setFile(e.target.files[0]);
        setFileName(
          e.target.value
            .substring(e.target.value.lastIndexOf("\\") + 1)
            .replace(".txt", ".yml")
        );
        break;
    }
  };

  function ThatResetsTheFileInput() {
    setFile(null);
    // Reset the file input field
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  }

  const handleClick = (e: any) => {
    e.preventDefault();
    if (!file) {
      setFlag(false);
      setMessage("Please select a file");
      setTimeout(() => {
        setMessage("");
      }, 2000);
      return;
    }
    setButtonState(true);
    setLoading(true);
    const data = new FormData();
    data.append("file", file);
    console.log(APIS.upload_backup);
    axios
      .post(APIS.upload_backup, data)
      .then((response) => {
        setButtonState(false);
        setLoading(false);
        if (response && (response.status === 200 || response.status === 201)) {
          ThatResetsTheFileInput();
          setFlag(true);
          setMessage("Uploaded successfully!");
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", fileName);
          document.body.appendChild(link);
          link.click();
          setTimeout(() => {
            setMessage("");
          }, 2000);
        } else {
          setFlag(false);
          ThatResetsTheFileInput();
          setMessage("some error occurred");
          setTimeout(() => {
            setMessage("");
          }, 2000);
        }
      })
      .catch((error) => {
        let msg =
          error.response?.data?.detail ||
          error.message ||
          error ||
          "some error occurred";
        setButtonState(false);
        setLoading(false);
        setFlag(false);
        setMessage(msg);
        ThatResetsTheFileInput();
        setTimeout(() => {
          setMessage("");
        }, 5000);
      });
  };

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Avatar className={classes.avatar}>
          <CloudUploadOutlined />
        </Avatar>
        <Typography component="h1" variant="h5">
          Upload Backup Configuration
        </Typography>
        <form className={classes.form}>
          <Box mb={2}>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="file"
              inputProps={{ accept: "text/plain" }}
              type="file"
              name="file"
              inputRef={fileInputRef}
              onChange={handleChange}
            />
          </Box>
          <Box mt={2}>
            <Button
              variant="contained"
              style={{ display: "block", textAlign: "center" }}
              fullWidth
              onClick={handleClick}
              disabled={buttonState}
              sx={{ textTransform: "none" }}
            >
              {loading && (
                <CircularProgress
                  size={30}
                  sx={{
                    color: green,
                    position: "absolute",
                    top: "50%",
                    left: "50%",
                    marginTop: "-12px",
                    marginLeft: "-12px",
                  }}
                />
              )}
              <Typography variant="h6">Upload</Typography>
            </Button>
          </Box>

          <Box mt={1}>
            {flag && <h3 className={classes.success}>{message}</h3>}
          </Box>
          <Box mt={1}>
            {!flag && <h3 className={classes.error}>{message}</h3>}
          </Box>
        </form>
      </div>
    </Container>
  );
};

export default BackupUpload;
