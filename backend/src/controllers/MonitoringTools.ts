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
  python_func_device_info,
  sonicos4_folder,
  output_folder,
  device_info_folder,
  websocket_message_filter,
} from "../library/Globals";

const directory: string = path.resolve();

const monitoringTools = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {};

export default {
  monitoringTools,
};
