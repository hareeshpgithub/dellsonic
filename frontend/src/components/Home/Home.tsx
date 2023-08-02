import React, { useEffect, useState } from "react";
import { styled, useTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import MuiAppBar, { AppBarProps as MuiAppBarProps } from "@mui/material/AppBar";
import {
  ListItemText,
  ListItemIcon,
  ListItemButton,
  Box,
  Button,
  Drawer,
  Toolbar,
  List,
  Typography,
  Divider,
  IconButton,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from "@mui/material";
import {
  Menu,
  ChevronLeft,
  ChevronRight,
  LogoutOutlined,
  HomeOutlined,
  LockResetOutlined,
  ReadMoreOutlined,
  SettingsInputComponentOutlined,
  DisplaySettingsOutlined,
  BackupTableOutlined,
  StorageOutlined,
} from "@mui/icons-material";
import { useNavigate } from "react-router-dom";
import Welcome from "./Welcome";
import BackupYml from "./BackupUpload";
import ExcelYml from "./ExcelUpload";
import DeviceInfo from "./DeviceInfo";
import DeviceBackup from "./DeviceBackup";
import NewConfiguration from "./NewConfiguration";
import Deploy from "./Deploy";
import Footer from "./Footer";

const drawerWidth = 240;

const Main = styled("main", { shouldForwardProp: (prop) => prop !== "open" })<{
  open?: boolean;
}>(({ theme, open }) => ({
  flexGrow: 1,
  padding: theme.spacing(3),
  transition: theme.transitions.create("margin", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  marginLeft: `-${drawerWidth}px`,
  ...(open && {
    transition: theme.transitions.create("margin", {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
    marginLeft: 0,
  }),
}));

interface AppBarProps extends MuiAppBarProps {
  open?: boolean;
}

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== "open",
})<AppBarProps>(({ theme, open }) => ({
  transition: theme.transitions.create(["margin", "width"], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: `${drawerWidth}px`,
    transition: theme.transitions.create(["margin", "width"], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: "flex-end",
}));

export default function Home() {
  const theme = useTheme();
  const [pageHistory, setPageHistory] = useState(["home"]);
  const [open, setOpen] = useState(false);
  const [openConfirm, setOpenConfirm] = useState(false);

  const navigate = useNavigate();

  const userCompany = "Dell Sonic Automation";

  // Error Dialog
  const [openError, setOpenError] = useState(false);
  const [errorHeader, setErrorHeader] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const [state, setState] = useState({
    time: 0,
  });

  const closeError = () => {
    setOpenError(false);
    setErrorHeader("");
    setErrorMessage("");
    logOut();
  };

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const logOut = () => {
    localStorage.clear();
    navigate("/signin");
  };

  const currentPage = () => {
    return pageHistory[pageHistory.length - 1];
  };

  const handleClose = (event: any, reason: any) => {
    if (reason && reason === "backdropClick") return;
    setOpenConfirm(false);
  };

  const navigateToPage = (pageName: any) => {
    setState({ time: Date.now() });
    let newHistory = [...pageHistory];

    if (newHistory[newHistory.length - 1] !== pageName) {
      newHistory.push(pageName);
      setPageHistory([...newHistory]);
      handleDrawerClose();
    }
  };

  useEffect(() => {}, [state.time, userCompany]);

  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <AppBar position="fixed" open={open}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            sx={{ mr: 2, ...(open && { display: "none" }) }}
          >
            <Menu />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            {userCompany}
          </Typography>
        </Toolbar>
      </AppBar>

      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          "& .MuiDrawer-paper": {
            width: drawerWidth,
            boxSizing: "border-box",
          },
        }}
        variant="persistent"
        anchor="left"
        open={open}
      >
        <DrawerHeader>
          <IconButton onClick={handleDrawerClose}>
            {theme.direction === "ltr" ? <ChevronLeft /> : <ChevronRight />}
          </IconButton>
        </DrawerHeader>
        <Divider />
        <List>
          {/* Home Button */}
          {/* <ListItemButton onClick={() => navigateToPage("home")}>
            <ListItemIcon>
              <HomeOutlined />
            </ListItemIcon>
            <ListItemText primary="Home" />
          </ListItemButton> */}
          {/* End */}

          <Divider />
          {/* Export Text Button */}
          <ListItemButton onClick={() => navigateToPage("new_configuration")}>
            <ListItemIcon>
              <ReadMoreOutlined />
            </ListItemIcon>
            <ListItemText primary="New Configuration" />
          </ListItemButton>
          {/* End */}
          {/* Export Text Button */}
          {/* <ListItemButton onClick={() => navigateToPage("backup_to_yaml")}>
            <ListItemIcon>
              <ReadMoreOutlined />
            </ListItemIcon>
            <ListItemText primary="Backup to Yml" />
          </ListItemButton> */}
          {/* End */}
          {/* Export Excel Button */}
          {/* <ListItemButton onClick={() => navigateToPage("excel_to_yaml")}>
            <ListItemIcon>
              <ReadMoreOutlined />
            </ListItemIcon>
            <ListItemText primary="Excel to Yml" />
          </ListItemButton> */}
          {/* End */}
          {/* Export Excel Button */}
          {/* <ListItemButton onClick={() => navigateToPage("wizard_to_yaml")}>
            <ListItemIcon>
              <SettingsInputComponentOutlined />
            </ListItemIcon>
            <ListItemText primary="Wizard" />
          </ListItemButton> */}
          {/* End */}
          <Divider />
          {/* EDEvice Information Button */}
          {/* <ListItemButton onClick={() => navigateToPage("get_device_info")}>
            <ListItemIcon>
              <DisplaySettingsOutlined />
            </ListItemIcon>
            <ListItemText primary="Device Information" />
          </ListItemButton> */}
          {/* End */}
          {/* Device Backup Button */}
          <ListItemButton onClick={() => navigateToPage("get_device_backup")}>
            <ListItemIcon>
              <BackupTableOutlined />
            </ListItemIcon>
            <ListItemText primary="Device Backup" />
          </ListItemButton>
          {/* End */}
          {/* Device Deploy Button */}
          <ListItemButton
            onClick={() => navigateToPage("deploy_configuration")}
          >
            <ListItemIcon>
              <StorageOutlined />
            </ListItemIcon>
            <ListItemText primary="Deploy Inventory" />
          </ListItemButton>
          {/* End */}
          <Divider />
          {/* <ListItemButton>
            <ListItemIcon>
              <LockResetOutlined />
            </ListItemIcon>
            <ListItemText
              primary="Change Password"
              onClick={() => navigateToPage("change password")}
            />
          </ListItemButton> */}
          <ListItemButton>
            <ListItemIcon>
              <LogoutOutlined />
            </ListItemIcon>
            <ListItemText primary="Log Out" onClick={() => logOut()} />
          </ListItemButton>
        </List>
      </Drawer>

      <Main open={open}>
        <DrawerHeader />
        {currentPage() === "home" && (
          <Welcome
            location={{
              state: state,
            }}
          />
        )}
        {currentPage() === "backup_to_yaml" && (
          <BackupYml
            location={{
              state: state,
            }}
          />
        )}
        {currentPage() === "excel_to_yaml" && (
          <ExcelYml
            location={{
              state: state,
            }}
          />
        )}
        {currentPage() === "get_device_info" && (
          <DeviceInfo
            location={{
              state: state,
            }}
          />
        )}
        {currentPage() === "get_device_backup" && (
          <DeviceBackup
            location={{
              state: state,
            }}
          />
        )}
        {currentPage() === "deploy_configuration" && (
          <Deploy
            location={{
              state: state,
            }}
          />
        )}
        {currentPage() === "new_configuration" && (
          <NewConfiguration
            location={{
              state: state,
            }}
          />
        )}
      </Main>
      <Dialog
        open={openConfirm}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          {"Please Confirm Details:"}
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            <Typography>
              Note: This Mobile Device will be used for Attendance
            </Typography>
            <Typography color="common.red">
              Important: This Cannot be reverted
            </Typography>
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={logOut}>Disagree</Button>
        </DialogActions>
      </Dialog>
      <Dialog
        open={openError}
        onClose={closeError}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title" color="common.red">
          {errorHeader}
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            {errorMessage}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={closeError}>Ok</Button>
        </DialogActions>
      </Dialog>
      <Footer />
    </Box>
  );
}
