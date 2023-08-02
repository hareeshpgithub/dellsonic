import { NextFunction, Request, Response } from "express";
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
} from "../library/Globals";

const directory: string = path.resolve();

const deviceConfig = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const { host, ipaddress, user, password } = req.body;

  const sonic_path = path.join(
    directory,
    source_folder,
    python_automation_folder
  );
  const args = [
    python_script,
    python_func_device_backup,
    "user",
    host,
    ipaddress,
    user,
    password,
  ];
  console.log(args);
  const output = spawn(command, args, { cwd: sonic_path });

  output.stdout.on("data", (data: any) => {
    const lines = data.toString().split("\n");

    const taskLine = lines.find((line: any) =>
      line.startsWith(websocket_message_filter)
    );
    if (taskLine) {
      const bracketsContent = taskLine.match(/\[(.*?)\]/)?.[1] || "";
      const colonIndex = bracketsContent.indexOf(":");
      const extractedText =
        colonIndex !== -1
          ? bracketsContent.substring(colonIndex + 1).trim()
          : "";
      logger.info(data.toString());
      clients.forEach((client) => {
        client.send(extractedText);
      });
    }
  });

  output.on("close", (code: any) => {
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
        .sendFile(host + ".aarohi.device.backup.txt", options, function (err) {
          if (err) {
            next(err);
          }
        });
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
};

export default {
  deviceConfig,
};
