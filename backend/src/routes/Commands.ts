import express, { Request, Response, NextFunction } from "express";
import { logger } from "../library/General";
import path from "path";
import mongoose from "mongoose";
import Users from "../models/Users";
import WebSocket from "ws";
import multer from "multer";
const fs = require("fs").promises;
import { createWriteStream } from "fs";

let router = express.Router();
let crypto = require("crypto");
let backup_original_name = "";
const spawn = require("child_process").spawn;
const wss = new WebSocket.Server({ port: 9092 });
const clients = new Set();
wss.on("connection", (ws: any) => {
  clients.add(ws);
  ws.on("close", () => {
    clients.delete(ws);
  });
});

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "./uploads/");
  },

  filename: function (req: any, file: any, cb: any) {
    backup_original_name = file.originalname.replace(".txt", "");
    let temp_filename = crypto.randomBytes(10).toString("hex");
    temp_filename += temp_filename + path.extname(file.originalname);
    cb(null, temp_filename);
  },
});

const ymlFilter = (req: any, file: any, cb: any) => {
  if (file.mimetype === "text/plain") {
    cb(null, true);
  } else {
    cb(new Error("Uploaded is not a Yaml File"), false);
  }
};

const excelFilter = (req: any, file: any, cb: any) => {
  if (
    file.mimetype === "application/vnd.ms-excel" ||
    file.mimetype ===
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
  ) {
    cb(null, true);
  } else {
    cb(new Error("Uploaded is not a Excel File"), false);
  }
};

const textFilter = (req: any, file: any, cb: any) => {
  if (file.mimetype === "text/plain") {
    cb(null, true);
  } else {
    cb(new Error("Uploaded is not a Text File"), false);
  }
};

const upload_backup_file = multer({
  storage: storage,
  fileFilter: textFilter,
});
const deploy_yaml_file = multer({
  storage: storage,
  fileFilter: ymlFilter,
});
const upload_excel_file = multer({ storage: storage, fileFilter: excelFilter });

router.post(
  "/deploy",
  deploy_yaml_file.single("file"),
  async (req: Request, res: Response, next: NextFunction) => {
    const { host, ip, user, password } = req.body;
    const directory: string = path.resolve();
    let input_file = req.file?.filename!;
    logger.info(input_file);
    const sonic_path = path.join(directory, "src", "automate");
    const command = "python3";
    const args = ["Automate.py", "deviceinfo", host, ip, user, password];
    const output = spawn(command, args, { cwd: sonic_path });

    output.stdout.on("data", (data: any) => {
      logger.info(`stdout: ${data}`);
      clients.forEach((client: any) => {
        logger.info("======>" + data);
        client.send(data);
      });
    });

    output.stderr.on("data", (data: any) => {
      logger.error(`stderr: ${data}`);
    });

    output.on("close", (code: any) => {
      logger.info(`child process exited with code ${code}`);
      if (code === 0) {
        return res.status(20).json({ detail: "Success" });
      } else {
        const options = {
          root: path.join(directory, "src", "sonicos4"),
        };
        return res.status(500).sendFile("log.txt", options, function (err) {
          if (err) {
            next(err);
          }
        });
      }
    });
  }
);

router.post(
  "/backuptoyml",
  upload_backup_file.single("file"),
  async (req: Request, res: Response, next: NextFunction) => {
    const directory: string = path.resolve();
    let input_file = req.file?.filename!;
    let output_file = req.file?.filename.replace(".txt", ".yml")!;
    const output = await spawn("python3", [
      path.join(directory, "src", "Parser", "BackupParser.py"),
      backup_original_name,
      path.join(directory, "uploads", input_file),
      path.join(directory, "uploads", output_file),
    ]);
    output.stdout.on("data", (data: any) => {
      logger.info(`stdout: ${data}`);
      clients.forEach((client: any) => {
        logger.info("======>" + data);
        client.send(data);
      });
    });

    output.stderr.on("data", (data: any) => {
      logger.error(`stderr: ${data}`);
    });

    output.on("close", (code: any) => {
      logger.info(`child process exited with code ${code}`);
      if (code === 0) {
        console.log(directory);
        console.log(output_file);
        const options = {
          root: path.join(directory, "uploads"),
        };
        console.log(options);

        res.sendFile(output_file, options, function (err) {
          if (err) {
            next(err);
          } else {
            logger.info("Sent: " + output_file);
          }
        });
      } else {
        // Pending
      }
    });
  }
);

router.post(
  "/deviceinfo",
  async (req: Request, res: Response, next: NextFunction) => {
    const { host, ip, user, password } = req.body;
    const directory: string = path.resolve();

    const sonic_path = path.join(directory, "src", "automate");
    const command = "python3";
    const args = ["Automate.py", "deviceinfo", host, ip, user, password];

    const output = spawn(command, args, { cwd: sonic_path });

    output.stdout.on("data", (data: any) => {
      const lines = data.toString().split("\n");
      const errorLines = lines.filter((line: any) => line.includes("fatal"));
      if (errorLines.length > 0) {
      }
    });
    output.stdout.on("data", (data: any) => {
      const lines = data.toString().split("\n");
      const taskLine = lines.find((line: any) => line.startsWith("TASK"));
      if (taskLine) {
        // Extract the text inside brackets
        const bracketsContent = taskLine.match(/\[(.*?)\]/)?.[1] || "";

        // Remove the text before the colon
        const colonIndex = bracketsContent.indexOf(":");
        const extractedText =
          colonIndex !== -1
            ? bracketsContent.substring(colonIndex + 1).trim()
            : "";

        clients.forEach((client: any) => {
          client.send(extractedText);
        });
      }
    });
    output.on("close", (code: any) => {
      if (code === 0) {
        const options = {
          root: path.join(directory, "src", "sonicos4", "deviceinfo"),
        };
        res.status(200).sendFile(host + ".txt", options, function (err) {
          if (err) {
            next(err);
          }
        });
      } else {
        const options = {
          root: path.join(directory, "src", "sonicos4"),
        };
        return res.status(500).sendFile("log.txt", options, function (err) {
          if (err) {
            next(err);
          }
        });
      }
    });
  }
);

router.post(
  "/devicebackup",
  async (req: Request, res: Response, next: NextFunction) => {
    const { host, ip, user, password } = req.body;
    const directory: string = path.resolve();

    const sonic_path = path.join(directory, "src", "automate");
    const command = "python3";
    const args = ["Automate.py", "devicebackup", host, ip, user, password];

    const output = spawn(command, args, { cwd: sonic_path });

    output.stdout.on("data", (data: any) => {
      const lines = data.toString().split("\n");
      const taskLine = lines.find((line: any) => line.startsWith("TASK"));
      if (taskLine) {
        // Extract the text inside brackets
        const bracketsContent = taskLine.match(/\[(.*?)\]/)?.[1] || "";

        // Remove the text before the colon
        const colonIndex = bracketsContent.indexOf(":");
        const extractedText =
          colonIndex !== -1
            ? bracketsContent.substring(colonIndex + 1).trim()
            : "";

        clients.forEach((client: any) => {
          client.send(extractedText);
        });
      }
    });
    output.on("close", (code: any) => {
      if (code === 0) {
        const options = {
          root: path.join(directory, "src", "sonicos4", "configs_backup"),
        };
        res.status(200).sendFile(host + ".txt", options, function (err) {
          if (err) {
            next(err);
          }
        });
      } else {
        const options = {
          root: path.join(directory, "src", "sonicos4"),
        };
        return res.status(500).sendFile("log.txt", options, function (err) {
          if (err) {
            next(err);
          }
        });
      }
    });
  }
);

export = router;
