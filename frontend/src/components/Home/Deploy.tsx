import React, { useEffect, useState } from "react";
import { createTheme } from "@mui/material/styles";
import { makeStyles } from "@mui/styles";
import {
  Button,
  TextField,
  CssBaseline,
  Box,
  Typography,
  Container,
  CircularProgress,
} from "@mui/material";
import { red, blue, green, lightBlue, orange } from "@mui/material/colors";
import axios from "axios";
import { APIS } from "../../config";
import socket from "./websocket";

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

const timeoutDuration = 15 * 60 * 1000;
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

socket.addEventListener("open", () => {});

const DeviceBackup = (props: { location: { state: any } }) => {
  const [flag, setFlag] = useState(false);
  const [websocketFlag, setWebsocketFlag] = useState(false);
  const [message, setMessage] = useState("");
  const [websocketMessage, setWebsocketMessage] = useState("");

  const classes = useStyles();
  const [loading, setLoading] = useState(false);
  const [buttonState, setButtonState] = useState(false);

  const [hostName, sethostName] = useState("");
  const [ip, setIp] = useState("");
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");

  const [file, setFile] = useState(null);
  // const [fileName, setFileName] = useState("");

  useEffect(() => {});
  socket.addEventListener("message", (event) => {
    const message = JSON.parse(event.data);
    console.log(message);
    if (message.message) {
      const extractedText = message.message;
      setWebsocketMessage(extractedText);
      setWebsocketFlag(true);
    }
    if (message.debug) {
      const debugMessage = message.debug;
      console.log(debugMessage);
    }
  });

  const handleChange = (e: any) => {
    switch (e.target.name) {
      case "file":
        setFile(e.target.files[0]);
        // const reader = new FileReader();
        // reader.onload = (event) => {
        //   const fileContent = event.target?.result as string;
        //   console.log(fileContent);

        //   try {
        //     const data = yaml.load(fileContent) as { [key: string]: any };

        //     const managementIP = data["management_ip"];
        //     const hostName = data["host_name"];

        //     console.log("Management IP:", managementIP);
        //     console.log("Host Name:", hostName);
        //   } catch (error) {
        //     console.error("Error parsing YAML:", error);
        //   }
        // };
        // reader.readAsText(e.target.files[0]);
        // setFileName(
        //   e.target.value
        //     .substring(e.target.value.lastIndexOf("\\") + 1)
        //     .replace(".txt", ".yml")
        // );
        break;
      case "hostname":
        sethostName(e.target.value);
        break;
      case "ip":
        setIp(e.target.value);
        break;
      case "username":
        setUserName(e.target.value);
        break;
      case "password":
        setPassword(e.target.value);
        break;
    }
  };

  function ThatResetsTheFileInput() {
    sethostName("");
    setIp("");
    setUserName("");
    setPassword("");
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
    if (!hostName) {
      setFlag(false);
      setMessage("Please Enter the Host name");
      setTimeout(() => {
        setMessage("");
      }, 2000);
      return;
    } else if (!ip) {
      setFlag(false);
      setMessage("Please Enter IP Address");
      setTimeout(() => {
        setMessage("");
      }, 2000);
      return;
    } else if (!userName) {
      setFlag(false);
      setMessage("Please Enter User name");
      setTimeout(() => {
        setMessage("");
      }, 2000);
      return;
    } else if (!password) {
      setFlag(false);
      setMessage("Please Enter Password");
      setTimeout(() => {
        setMessage("");
      }, 2000);
      return;
    }
    setButtonState(true);
    setLoading(true);
    const data = new FormData();
    data.append("file", file);
    data.append("host", hostName);
    data.append("ip", ip);
    data.append("user", userName);
    data.append("password", password);
    axios
      .post(APIS.device_deploy, data, {
        timeout: timeoutDuration,
      })
      .then((response) => {
        console.log(response);
        setButtonState(false);
        setLoading(false);
        if (response && (response.status === 200 || response.status === 201)) {
          setWebsocketFlag(false);
          setFlag(true);
          setMessage("Executed successfully!");
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", hostName + ".txt");
          document.body.appendChild(link);
          link.click();
          setTimeout(() => {
            setMessage("");
            ThatResetsTheFileInput();
          }, 2000);
        } else {
          setWebsocketFlag(false);
          setFlag(false);
          setLoading(false);
          setMessage("some error occurred");
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", hostName + ".txt");
          document.body.appendChild(link);
          link.click();
          setTimeout(() => {
            setMessage("");
          }, 2000);
        }
      })
      .catch((error) => {
        console.log(error);
        let msg =
          error.response?.data?.detail ||
          error.message ||
          error ||
          "some error occurred";
        setButtonState(false);
        setLoading(false);
        setWebsocketFlag(false);
        setFlag(false);
        setMessage(msg);
        const url = window.URL.createObjectURL(
          new Blob([error.response?.data])
        );
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "error.txt");
        document.body.appendChild(link);
        link.click();
        setTimeout(() => {
          setMessage("");
        }, 5000);
      });
  };

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        {/* <Avatar className={classes.avatar}>
          <CloudUploadOutlined />
        </Avatar> */}
        <Typography component="h1" variant="h5">
          Deploy Inventory - New Switch
        </Typography>
        <form className={classes.form}>
          <Box mb={2}>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="file"
              inputProps={{ accept: "application/x-yaml" }}
              type="file"
              name="file"
              onChange={handleChange}
            />
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="hostname"
              label="Host Name"
              name="hostname"
              value={hostName}
              autoComplete=""
              autoFocus
              onChange={handleChange}
            />
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="ip"
              label="IP Address"
              name="ip"
              autoComplete=""
              value={ip}
              onChange={handleChange}
            />
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="username"
              label="User"
              name="username"
              autoComplete=""
              value={userName}
              onChange={handleChange}
            />
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="password"
              label="Password"
              name="password"
              type="password"
              autoComplete=""
              value={password}
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
              <Typography variant="h6">Execute</Typography>
            </Button>
          </Box>
          <Box mt={1}>
            {websocketFlag && (
              <h3 className={classes.success}>{websocketMessage}</h3>
            )}
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

export default DeviceBackup;
