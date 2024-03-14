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
  python_func_device_info,
  python_func_set_image,
  sonicos4_folder,
  output_folder,
  device_info_folder,
  websocket_message_filter,
  python_func_images_list,
  python_func_deploy_image,
} from "../library/Globals";

const directory: string = path.resolve();

const ImagesList = async (req: Request, res: Response, next: NextFunction) => {
  logger.debug("Inside Device Info");
  const { host, ip, user, password } = req.body;

  const sonic_path = path.join(
    directory,
    source_folder,
    python_automation_folder
  );
  const args = [
    python_script,
    python_func_images_list,
    host,
    ip,
    user,
    password,
  ];
  logger.debug(sonic_path);
  logger.debug(args);
  const output = spawn(command, args, { cwd: sonic_path });

  output.stderr.on("data", (data: any) => {
    logger.error(data.toString());
  });

  output.stdout.on("data", (data: any) => {
    let lines = data.toString().split("\n");
    logger.error(data.toString());
    let taskLine = lines.find((line: any) =>
      line.startsWith(websocket_message_filter)
    );
    if (taskLine) {
      const bracketsContent = taskLine.match(/\[(.*?)\]/)?.[1] || "";
      const colonIndex = bracketsContent.indexOf(":");
      const extractedText =
        colonIndex !== -1
          ? bracketsContent.substring(colonIndex + 1).trim()
          : "";
      const extractedTextMessage = JSON.stringify({
        message: extractedText,
      });
      clients.forEach((client) => {
        client.send(extractedTextMessage);
      });
    }
    const extractedDebugMessage = JSON.stringify({
      debug: lines,
    });
    clients.forEach((client) => {
      client.send(extractedDebugMessage);
    });
  });

  output.on("close", (code: any) => {
    if (code === 0) {
      const options = {
        root: path.join(
          directory,
          source_folder,
          sonicos4_folder,
          output_folder
          // device_info_folder
        ),
      };
      res
        .status(200)
        .sendFile(host + ".aarohi.image.info.txt", options, function (err) {
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
          output_folder,
          device_info_folder
        ),
      };
      return res
        .status(500)
        .sendFile(host + "-logs.txt", options, function (err) {
          if (err) {
            next(err);
          }
        });
    }
  });
};

const SetImage = async (req: Request, res: Response, next: NextFunction) => {
  logger.debug("Inside Device Info");
  const { host, ip, user, password, image } = req.body;

  const sonic_path = path.join(
    directory,
    source_folder,
    python_automation_folder
  );
  const args = [
    python_script,
    python_func_set_image,
    host,
    ip,
    user,
    password,
    image,
  ];
  logger.debug(sonic_path);
  logger.debug(args);
  const output = spawn(command, args, { cwd: sonic_path });

  output.stderr.on("data", (data: any) => {
    logger.error(data.toString());
  });

  output.stdout.on("data", (data: any) => {
    let lines = data.toString().split("\n");
    logger.error(data.toString());
    let taskLine = lines.find((line: any) =>
      line.startsWith(websocket_message_filter)
    );
    if (taskLine) {
      const bracketsContent = taskLine.match(/\[(.*?)\]/)?.[1] || "";
      const colonIndex = bracketsContent.indexOf(":");
      const extractedText =
        colonIndex !== -1
          ? bracketsContent.substring(colonIndex + 1).trim()
          : "";
      const extractedTextMessage = JSON.stringify({
        message: extractedText,
      });
      clients.forEach((client) => {
        client.send(extractedTextMessage);
      });
    }
    const extractedDebugMessage = JSON.stringify({
      debug: lines,
    });
    clients.forEach((client) => {
      client.send(extractedDebugMessage);
    });
  });

  output.on("close", (code: any) => {
    if (code === 0) {
      const options = {
        root: path.join(
          directory,
          source_folder,
          sonicos4_folder,
          output_folder
          // device_info_folder
        ),
      };
      res
        .status(200)
        .sendFile(host + ".aarohi.image.info.txt", options, function (err) {
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
          output_folder,
          device_info_folder
        ),
      };
      return res
        .status(500)
        .sendFile(host + "-logs.txt", options, function (err) {
          if (err) {
            next(err);
          }
        });
    }
  });
};

const DeployImage = async (req: Request, res: Response, next: NextFunction) => {
  logger.debug("Inside Device Info");
  const { host, ip, user, password, image } = req.body;

  const sonic_path = path.join(
    directory,
    source_folder,
    python_automation_folder
  );
  const args = [
    python_script,
    python_func_deploy_image,
    host,
    ip,
    user,
    password,
    image,
  ];
  logger.debug(sonic_path);
  logger.debug(args);
  const output = spawn(command, args, { cwd: sonic_path });

  output.stderr.on("data", (data: any) => {
    logger.error(data.toString());
  });

  output.stdout.on("data", (data: any) => {
    let lines = data.toString().split("\n");
    logger.error(data.toString());
    let taskLine = lines.find((line: any) =>
      line.startsWith(websocket_message_filter)
    );
    if (taskLine) {
      const bracketsContent = taskLine.match(/\[(.*?)\]/)?.[1] || "";
      const colonIndex = bracketsContent.indexOf(":");
      const extractedText =
        colonIndex !== -1
          ? bracketsContent.substring(colonIndex + 1).trim()
          : "";
      const extractedTextMessage = JSON.stringify({
        message: extractedText,
      });
      clients.forEach((client) => {
        client.send(extractedTextMessage);
      });
    }
    const extractedDebugMessage = JSON.stringify({
      debug: lines,
    });
    clients.forEach((client) => {
      client.send(extractedDebugMessage);
    });
  });

  output.on("close", (code: any) => {
    if (code === 0) {
      const options = {
        root: path.join(
          directory,
          source_folder,
          sonicos4_folder,
          output_folder
          // device_info_folder
        ),
      };
      res
        .status(200)
        .sendFile(host + ".aarohi.image.info.txt", options, function (err) {
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
          output_folder,
          device_info_folder
        ),
      };
      return res
        .status(500)
        .sendFile(host + "-logs.txt", options, function (err) {
          if (err) {
            next(err);
          }
        });
    }
  });
};

const ShowStatus = async (req: Request, res: Response, next: NextFunction) => {
  logger.debug("Inside Device Info");
  const { host, ip, user, password } = req.body;

  const sonic_path = path.join(
    directory,
    source_folder,
    python_automation_folder
  );
  const args = [python_script, "showstatus", host, ip, user, password];
  logger.debug(sonic_path);
  logger.debug(args);
  const output = spawn(command, args, { cwd: sonic_path });

  output.stderr.on("data", (data: any) => {
    logger.error(data.toString());
  });

  output.stdout.on("data", (data: any) => {
    let lines = data.toString().split("\n");
    logger.error(data.toString());
    let taskLine = lines.find((line: any) =>
      line.startsWith(websocket_message_filter)
    );
    if (taskLine) {
      const bracketsContent = taskLine.match(/\[(.*?)\]/)?.[1] || "";
      const colonIndex = bracketsContent.indexOf(":");
      const extractedText =
        colonIndex !== -1
          ? bracketsContent.substring(colonIndex + 1).trim()
          : "";
      const extractedTextMessage = JSON.stringify({
        message: extractedText,
      });
      clients.forEach((client) => {
        client.send(extractedTextMessage);
      });
    }
    const extractedDebugMessage = JSON.stringify({
      debug: lines,
    });
    clients.forEach((client) => {
      client.send(extractedDebugMessage);
    });
  });

  output.on("close", (code: any) => {
    if (code === 0) {
      const options = {
        root: path.join(
          directory,
          source_folder,
          sonicos4_folder,
          output_folder
          // device_info_folder
        ),
      };
      res
        .status(200)
        .sendFile(host + ".aarohi.image.info.txt", options, function (err) {
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
          output_folder,
          device_info_folder
        ),
      };
      return res
        .status(500)
        .sendFile(host + "-logs.txt", options, function (err) {
          if (err) {
            next(err);
          }
        });
    }
  });
};

export default {
  ImagesList,
  SetImage,
  DeployImage,
  ShowStatus,
};
