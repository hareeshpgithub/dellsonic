import mongoose, { Document, Schema } from "mongoose";

export interface IDeviceConfiguration {
  host: string;
  ipaddress: string;
  user: string;
  password: boolean;
  log: string;
  device_config: string;
}

export interface IDeviceConfigurationModel
  extends IDeviceConfiguration,
    Document {}

const DeviceConfigurationSchema: Schema = new Schema(
  {
    hostname: { type: String, required: true },
    ip_address: { type: String, required: true },
    user: { type: String, required: true },
    password: { type: String, required: true },
    device_config: { type: String, required: true },
  },
  {
    timestamps: true,
    versionKey: false,
  }
);

export default mongoose.model<IDeviceConfigurationModel>(
  "DeviceConfig",
  DeviceConfigurationSchema
);
