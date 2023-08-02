import Joi, { ObjectSchema } from "joi";
import { NextFunction, Request, Response } from "express";
import { IUsers } from "../models/Users";
import { IDeviceInformation } from "../models/DeviceInformation";
import { IDeviceConfiguration } from "../models/DeviceConfiguration";
import { IExportBackupToYaml } from "../models/ExportBackupYaml";
import { logger } from "../library/General";

export const ValidateJoi = (schema: ObjectSchema) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      await schema.validateAsync(req.body);
      next();
    } catch (error) {
      logger.error(error);
      return res.status(422).json({ error });
    }
  };
};

export const Schemas = {
  registerUsers: {
    create: Joi.object<IUsers>({
      name: Joi.string().required(),
      password: Joi.string().required(),
    }),
  },
  login: {
    find: Joi.object<IUsers>({
      name: Joi.string().required(),
      password: Joi.string().required(),
    }),
  },
  deviceinfo: {
    info: Joi.object<IDeviceInformation>({
      host: Joi.string().required(),
      ipaddress: Joi.string().required(),
      user: Joi.string().required(),
      password: Joi.string().required(),
    }),
  },
  deviceconfig: {
    info: Joi.object<IDeviceConfiguration>({
      host: Joi.string().required(),
      ipaddress: Joi.string().required(),
      user: Joi.string().required(),
      password: Joi.string().required(),
    }),
  },
  backuptexttoyaml: {
    info: Joi.object<IExportBackupToYaml>({
      // file: Joi.object().required(),
      host: Joi.string(),
      ipaddress: Joi.string(),
      user: Joi.string(),
      password: Joi.string(),
    }),
  },
};
