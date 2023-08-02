import express from "express";
import { Schemas, ValidateJoi } from "../middleware/Joi";
import users from "../controllers/Users";
import deviceinfo from "../controllers/DeviceInformation";
import deviceconfig from "../controllers/DeviceConfiguration";
import backuptoyml from "../controllers/ExportBackupYaml";
import exceltoyml from "../controllers/ExportExcelYaml";
import deploy from "../controllers/DeployConfiguration";
import newtemplate from "../controllers/NewConfigurationExcel";

const router = express.Router();

router.post(
  "/register",
  ValidateJoi(Schemas.registerUsers.create),
  users.registerUser
);
router.post("/login", ValidateJoi(Schemas.login.find), users.login);
router.post(
  "/deviceinfo",
  ValidateJoi(Schemas.deviceinfo.info),
  deviceinfo.deviceInfo
);
router.post(
  "/deviceconfig",
  ValidateJoi(Schemas.deviceinfo.info),
  deviceconfig.deviceConfig
);
router.post(
  "/backuptoyml",
  ValidateJoi(Schemas.backuptexttoyaml.info),
  backuptoyml
);
router.post(
  "/newtemplate",
  ValidateJoi(Schemas.backuptexttoyaml.info),
  newtemplate.NewConfig
);

router.post(
  "/exceltoyml",
  ValidateJoi(Schemas.backuptexttoyaml.info),
  exceltoyml
);

router.post("/deploy", ValidateJoi(Schemas.backuptexttoyaml.info), deploy);
export = router;
