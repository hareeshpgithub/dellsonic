import mongoose, { Document, Schema } from "mongoose";

export interface IDeployConfiguration {
  file: Object;
  host: string;
  ipaddress: string;
  user: string;
  password: boolean;
  log: string;
  backup_config: string;
}

export interface IDeployConfigurationModel
  extends IDeployConfiguration,
    Document {}

const DeployConfigurationSchema: Schema = new Schema(
  {
    file: { type: Object, required: true },
    hostname: { type: String, required: true },
    ip_address: { type: String, required: true },
    user: { type: String, required: true },
    password: { type: String, required: true },
    backup_config: { type: String, required: true },
  },
  {
    timestamps: true,
    versionKey: false,
  }
);

export default mongoose.model<IDeployConfigurationModel>(
  "DeployConfiguration",
  DeployConfigurationSchema
);
