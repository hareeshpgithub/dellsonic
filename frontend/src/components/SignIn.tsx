import React, { useState } from "react";
import {
  Avatar,
  Button,
  TextField,
  CssBaseline,
  Box,
  Typography,
  Container,
} from "@mui/material";
import { makeStyles } from "@mui/styles";

import LockOpenOutlined from "@mui/icons-material/LockOpenOutlined";

import { useNavigate } from "react-router-dom";
import axios from "axios";
import { APIS } from "./../config";
import { createTheme } from "@mui/material/styles";

const theme = createTheme();

const useStyles = makeStyles({
  root: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  paper: {
    marginTop: theme.spacing(8),
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
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
});

export default function SignIn() {
  const classes = useStyles();
  const [flag, setFlag] = useState(false);
  const [message, setMessage] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleChange = (e: any) => {
    switch (e.target.name) {
      case "username":
        setUsername(e.target.value);
        break;
      case "password":
        setPassword(e.target.value);
        break;
    }
  };

  const handleClick = (e: any) => {
    if (username && password) {
      e.preventDefault();

      axios
        .post(APIS.login, {
          name: username,
          password: password,
        })
        .then((response: any) => {
          if (
            response &&
            (response.status === 200 || response.status === 201)
          ) {
            localStorage.setItem("user", JSON.stringify(response.data.detail));
            setFlag(true);
            setMessage("Logged in successfully!");
            setTimeout(() => {
              navigate("/");
            }, 1000);
          } else {
            setFlag(false);
            setMessage("Some error occurred");
          }
        })
        .catch((error: any) => {
          let msg =
            error.response?.data.detail ||
            error.message ||
            "some error occurred";
          setFlag(false);
          setMessage(msg);
        });
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Avatar className={classes.avatar}>
          <LockOpenOutlined />
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign in
        </Typography>
        <form className={classes.form}>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="username"
            label="Enter your Employee ID"
            name="username"
            autoComplete="username"
            autoFocus
            onChange={handleChange}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            onChange={handleChange}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
            onClick={handleClick}
          >
            Sign In
          </Button>
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
}
