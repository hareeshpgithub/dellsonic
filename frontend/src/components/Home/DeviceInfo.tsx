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
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import IconButton from "@mui/material/IconButton";
import InputAdornment from "@mui/material/InputAdornment";
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

const DeviceInfo = (props: { location: { state: any } }) => {
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

  const [showPassword, setShowPassword] = React.useState(false);

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

  const handleClickShowPassword = () => setShowPassword((show) => !show);

  const handleMouseDownPassword = (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    event.preventDefault();
  };

  const handleChange = (e: any) => {
    switch (e.target.name) {
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

    /* Pending 
    
    */
    sethostName("hareesh");
    setIp("192.168.2.12");
    setUserName("admin");
    setPassword("YourPaSsWoRd");

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
    axios
      .post(
        APIS.device_info,
        {
          host: hostName,
          ipaddress: ip,
          user: userName,
          password: password,
        },
        {
          timeout: APIS.timeout,
        }
      )
      .then((response) => {
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
            ThatResetsTheFileInput();
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
          ThatResetsTheFileInput();
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
          Get Device Details
        </Typography>
        <form className={classes.form}>
          <Box mb={2}>
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
              type={showPassword ? "text" : "password"}
              autoComplete=""
              value={password}
              onChange={handleChange}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle password visibility"
                      onClick={handleClickShowPassword}
                      onMouseDown={handleMouseDownPassword}
                      edge="end"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
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

export default DeviceInfo;
