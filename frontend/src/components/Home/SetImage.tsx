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

const SetImage = (props: { location: { state: any } }) => {
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

    const [mainScreen, setMainScreen] = useState(true);
    const [imagesScreen, setImagesScreen] = useState(false);
    const [setScreen, setSetScreen] = useState(false);

    const [nextScreen, setNextScreen] = useState(false);

    const [sonicVersion, setSonicVersion] = useState("");
    const [currentVersion, setCurrentVersion] = useState("");

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
        if (e.target.value === currentVersion) {
            setSetScreen(false)
        } else {
            setSetScreen(true)
        }
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

    const handleSetClick = (e: any) => {
        e.preventDefault();

        axios
            .post(
                APIS.set_image,
                {
                    host: hostname,
                    ip: ip,
                    user: userName,
                    password: password,
                    image: sonicVersion
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
                    alert('Rebooting now, Please check after 10 min')
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
        setNextScreen(true)
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

                    const currentValue: string = data[0][0].split(": ")[1];
                    setCurrentVersion(currentValue)

                    setAvailableVersions(availableVersionsFromApi);
                    setWebsocketFlag(false);
                    setFlag(true);
                    setMessage("Executed successfully!");
                    setTimeout(() => {
                        setMessage("");
                        setImagesScreen(true);
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
                    Set Sonic Image
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
                    </Box>
                    {!lockFields && (
                        <Box mt={2}>
                            <Button
                                variant="contained"
                                style={{ textAlign: "center" }}
                                fullWidth
                                onClick={handleClick}
                                disabled={nextScreen}
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
                                <Typography variant="h6">Next</Typography>
                            </Button>
                        </Box>
                    )}

                    <TextField
                        variant="outlined"
                        margin="normal"
                        required
                        fullWidth
                        id="currentVersion"
                        label="Current Version"
                        name="currentVersion"
                        autoComplete=""
                        value={currentVersion}
                        InputProps={{ readOnly: true }}
                        style={{ display: imagesScreen ? 'block' : 'none' }}
                    />

                    <div style={{ display: imagesScreen ? 'block' : 'none' }}>
                        <Box mt={1}>
                            <Select
                                labelId="sonicVersion"
                                id="sonicVersion"
                                value={sonicVersion}
                                label="sonicVersion"
                                fullWidth
                                onChange={selectSonicVersion}
                                style={{ color: 'white' }}
                            >
                                <MenuItem value="" disabled>
                                    Select Version
                                </MenuItem>
                                {availableVersions.map((version) => (
                                    <MenuItem key={version} value={version}>
                                        {version}
                                    </MenuItem>
                                ))}
                            </Select>
                        </Box>

                        <Box mt={2}>
                            <Button
                                variant="contained"
                                style={{ display: setScreen ? 'block' : 'none', textAlign: "center" }}
                                fullWidth
                                onClick={handleSetClick}
                                disabled={buttonState}
                                sx={{ textTransform: "none" }}
                            >
                                <Typography variant="h6">Set</Typography>
                            </Button>
                        </Box>
                    </div>

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

export default SetImage;
