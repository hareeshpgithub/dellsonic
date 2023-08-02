import express, { Request, Response, NextFunction } from "express";
import { general, logger } from "../library/General";

import path from "path";
import multer from "multer";

import {
  clients,
  command,
  source_folder,
  python_automation_folder,
  python_script,
  parser_script,
  python_func_device_info,
  sonicos4_folder,
  output_folder,
  device_info_folder,
  websocket_message_filter,
  upload_folder,
} from "../library/Globals";

const fs = require("fs").promises;
const spawn = require("child_process").spawn;

let router = express.Router();
let crypto = require("crypto");
let backup_original_name = "";

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

router.post(
  "/backuptoyml",
  upload_backup_file.single("file"),
  async (req: Request, res: Response, next: NextFunction) => {
    const directory: string = path.resolve();
    let upload_file_path = path.join(directory, upload_folder);
    let input_file = req.file?.filename!;
    let output_file = req.file?.filename.replace(".txt", ".yml")!;

    const sonic_path = path.join(
      directory,
      source_folder,
      python_automation_folder
    );

    const args = [
      parser_script,
      backup_original_name,
      path.join(upload_file_path, input_file),
      path.join(upload_file_path, output_file),
    ];

    const output = spawn(command, args, { cwd: sonic_path });

    output.stderr.on("data", (data: any) => {
      logger.error(`stderr: ${data}`);
    });

    output.on("close", (code: any) => {
      if (code === 0) {
        const options = {
          root: path.join(directory, upload_folder),
        };

        res.sendFile(output_file, options, function (err) {
          if (err) {
            next(err);
          }
        });
      } else {
        const options = {
          root: path.join(directory, source_folder, sonicos4_folder),
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
