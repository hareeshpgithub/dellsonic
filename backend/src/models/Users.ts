import mongoose, { Document, Schema } from "mongoose";

export interface IUsers {
  Company: string;
  name: string;
  password: string;
  active: boolean;
}

export interface IUsersModel extends IUsers, Document {}

const UsersSchema: Schema = new Schema(
  {
    name: { type: String, required: true, index: { unique: true } },
    password: { type: String, required: true },
    active: { type: Boolean, required: true },
  },
  {
    timestamps: true,
    versionKey: false,
  }
);

export default mongoose.model<IUsersModel>("Users", UsersSchema);
