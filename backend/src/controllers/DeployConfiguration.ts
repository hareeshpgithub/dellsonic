import express, { Request, Response, NextFunction } from "express";
import { general, logger } from "../library/General";
import path from "path";
const spawn = require("child_process").spawn;

import {
  clients,
  command,
  source_folder,
  python_automation_folder,
  python_script,
  python_func_device_backup,
  sonicos4_folder,
  output_folder,
  device_config_folder,
  websocket_message_filter,
  python_func_deploy_configuration,
} from "../library/Globals";

let crypto = require("crypto");
let router = express.Router();
import multer from "multer";

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "./uploads/");
  },

  filename: function (req: any, file: any, cb: any) {
    let temp_filename = crypto.randomBytes(10).toString("hex");
    temp_filename += temp_filename + path.extname(file.originalname);
    cb(null, temp_filename);
  },
});

const ymlFilter = (req: any, file: any, cb: any) => {
  if (file.mimetype === "application/x-yaml") {
    cb(null, true);
  } else {
    cb(new Error("Uploaded is not a Yaml File"), false);
  }
};

const deploy_yaml_file = multer({
  storage: storage,
  fileFilter: ymlFilter,
});

router.post(
  "/deploy",
  deploy_yaml_file.single("file"),
  async (req: Request, res: Response, next: NextFunction) => {
    const { host, ip, user, password } = req.body;
    const directory: string = path.resolve();
    let input_file = req.file?.filename!;
    logger.info(input_file);
    logger.info("Deploy Configuration");
    const sonic_path = path.join(
      directory,
      source_folder,
      python_automation_folder
    );
    const command = "python3";
    const args = [
      python_script,
      python_func_deploy_configuration,
      "user",
      host,
      ip,
      user,
      password,
      input_file,
    ];
    logger.info(JSON.stringify(args));

    const output = spawn(command, args, { cwd: sonic_path });

    output.stdout.on("data", (data: any) => {
      let lines = data.toString().split("\n");

      let taskLine = lines.find((line: any) =>
        line.startsWith(websocket_message_filter)
      );
      if (taskLine) {
        logger.info(taskLine);
        const bracketsContent = taskLine.match(/\[(.*?)\]/)?.[1] || "";
        const colonIndex = bracketsContent.indexOf(":");
        const extractedText =
          colonIndex !== -1
            ? bracketsContent.substring(colonIndex + 1).trim()
            : "";
        const extractedTextMessage = JSON.stringify({
          message: extractedText,
        });
        logger.error("Clients List: " + clients);
        clients.forEach((client) => {
          client.send(extractedTextMessage);
          logger.debug("sending: " + extractedTextMessage);
        });
      }
      const extractedDebugMessage = JSON.stringify({
        debug: lines,
      });
      clients.forEach((client) => {
        client.send(extractedDebugMessage);
      });
    });

    output.stderr.on("data", (data: any) => {
      logger.error(`stderr: ${data}`);
    });

    output.on("close", (code: any) => {
      logger.info(`child process exited with code ${code}`);
      if (code === 0) {
        const options = {
          root: path.join(
            directory,
            source_folder,
            sonicos4_folder,
            output_folder
          ),
        };
        res
          .status(200)
          .sendFile(
            host + ".aarohi.device.backup.txt",
            options,
            function (err) {
              if (err) {
                next(err);
              }
            }
          );
      } else {
        const options = {
          root: path.join(
            directory,
            source_folder,
            sonicos4_folder,
            output_folder
          ),
        };
        return res.status(500).sendFile("error.log", options, function (err) {
          if (err) {
            next(err);
          }
        });
      }
    });
  }
);

export = router;
