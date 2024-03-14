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
  InputLabel,
  Select,
  MenuItem
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

socket.addEventListener("open", () => { });

const UploadImage = (props: { location: { state: any } }) => {
  const [flag, setFlag] = useState(false);
  const [websocketFlag, setWebsocketFlag] = useState(false);
  const [message, setMessage] = useState("");
  const [websocketMessage, setWebsocketMessage] = useState("");

  const classes = useStyles();
  const [loading, setLoading] = useState(false);
  const [buttonState, setButtonState] = useState(false);

  const [hostname, setHostName] = useState("");
  const [ip, setIp] = useState("");
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [imagepath, setImagepath] = useState("");



  const [mainScreen, setMainScreen] = useState(true);
  const [imagesScreen, setImagesScreen] = useState(true);
  const [sonicVersion, setSonicVersion] = useState("");

  const [lockFields, setLockFields] = useState(false);
  const [availableVersions, setAvailableVersions] = useState([]);

  useEffect(() => { });
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

  const selectSonicVersion = (e: any) => {
    setSonicVersion(e.target.value)
  }

  const handleChange = (e: any) => {
    switch (e.target.name) {
      case "hostname":
        setHostName(e.target.value);
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
      case "imagepath":
        setImagepath(e.target.value);
    }
  };

  function ThatResetsTheFileInput() {
    setHostName("")
    setIp("");
    setUserName("");
    setPassword("");
  }

  function LockInput() {
    // setLockFields(true);
  }

  const handleProgressClick = (e: any) => {
    e.preventDefault();
    axios
      .post(
        APIS.show_progress,
        {
          host: hostname,
          ip: ip,
          user: userName,
          password: password,
          image: imagepath
        },
        {
          timeout: APIS.timeout,
        }
      )
      .then((response) => {
        setButtonState(false);
        setLoading(false);
        if (response && (response.status === 200 || response.status === 201)) {
          const data = response.data;

          setWebsocketFlag(false);
          setFlag(true);

          setMessage("Successful!");

          setImagesScreen(true);
          const textBasedString = data[0].join('\n');
          console.log(data)
          console.log(textBasedString)
          alert(textBasedString);

          setTimeout(() => {
            setMessage("");
            setImagesScreen(true);
          }, 2000);
        } else {
          setWebsocketFlag(false);
          setFlag(false);
          setLoading(false);
          setMessage("some error occurred");
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", "error.txt");
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
  }

  const handleDeployClick = (e: any) => {
    e.preventDefault();
    axios
      .post(
        APIS.deploy_image,
        {
          host: hostname,
          ip: ip,
          user: userName,
          password: password,
          image: imagepath
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
          setMessage("Successful!");
          setImagesScreen(true);
          alert("This will take 10-15 Min, please check Set Sonic after some time")
          setTimeout(() => {
            setMessage("");
            setImagesScreen(true);
          }, 2000);
        } else {
          setWebsocketFlag(false);
          setFlag(false);
          setLoading(false);
          setMessage("some error occurred");
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", "error.txt");
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
  }

  const handleClick = (e: any) => {
    e.preventDefault();
    if (!hostname) {
      setFlag(false);
      setMessage("Please Enter Host Name");
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
        APIS.image_list,
        {
          host: hostname,
          ip: ip,
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
          const data = response.data;
          const availableIndex = data[0].indexOf('Available: ');
          const availableVersionsFromApi = data[0].slice(availableIndex + 1).map((version: any) => version.trim());

          setAvailableVersions(availableVersionsFromApi);
          setWebsocketFlag(false);
          setFlag(true);
          setMessage("Executed successfully!");
          setTimeout(() => {
            setMessage("");
            // ThatResetsTheFileInput();
            // LockInput()
          }, 2000);
        } else {
          setWebsocketFlag(false);
          setFlag(false);
          setLoading(false);
          setMessage("some error occurred");
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", "error.txt");
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
          Deploy Sonic New Image
        </Typography>
        <form className={classes.form} style={{ display: mainScreen ? 'block' : 'none' }}>
          <Box mb={2}>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="hostname"
              label="Host Name"
              name="hostname"
              autoComplete=""
              value={hostname}
              onChange={handleChange}
              InputProps={{ readOnly: lockFields }}
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
              InputProps={{ readOnly: lockFields }}
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
              InputProps={{ readOnly: lockFields }}
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
              InputProps={{ readOnly: lockFields }}
            />
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="imagepath"
              label="Image Path"
              name="imagepath"
              type="text"
              autoComplete=""
              value={imagepath}
              onChange={handleChange}
              InputProps={{ readOnly: lockFields }}
            />
          </Box>
          {!lockFields && (
            <Box mt={2}>
              <Button
                variant="contained"
                style={{ display: "block", textAlign: "center" }}
                fullWidth
                onClick={handleDeployClick}
                disabled={buttonState}
                sx={{ textTransform: "none" }}
              >
                <Typography variant="h6">Deploy</Typography>
              </Button>
            </Box>

          )}
          <Box mt={2}>
            <Button
              variant="contained"
              style={{ display: imagesScreen ? 'block' : 'none', textAlign: "center" }}
              fullWidth
              onClick={handleProgressClick}
              disabled={buttonState}
              sx={{ textTransform: "none" }}
            >
              <Typography variant="h6">Check Progress</Typography>
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

export default UploadImage;
