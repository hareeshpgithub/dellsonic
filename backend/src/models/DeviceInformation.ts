import mongoose, { Document, Schema } from "mongoose";

export interface IDeviceInformation {
  host: string;
  ipaddress: string;
  user: string;
  password: boolean;
  log: string;
  device_info: string;
}

export interface IDeviceInformationModel extends IDeviceInformation, Document {}

const DeviceInformationSchema: Schema = new Schema(
  {
    hostname: { type: String, required: true },
    ip_address: { type: String, required: true },
    user: { type: String, required: true },
    password: { type: String, required: true },
    device_info: { type: String, required: true },
  },
  {
    timestamps: true,
    versionKey: false,
  }
);

export default mongoose.model<IDeviceInformationModel>(
  "DeviceInfo",
  DeviceInformationSchema
);
