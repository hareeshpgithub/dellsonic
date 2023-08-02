import { NextFunction, Request, Response } from "express";
import mongoose from "mongoose";
import { general, logger } from "../library/General";
import Users from "../models/Users";
import bcrypt from "bcryptjs";

const HASH_ROUNDS = 10;

const registerUser = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const { name, password } = req.body;
  const user = new Users({
    _id: new mongoose.Types.ObjectId(),
    name: name,
    password: password,
    active: true,
  });

  const salt = await bcrypt.genSalt(HASH_ROUNDS);
  user.password = await bcrypt.hash(user.password, salt);

  try {
    await user.save();
    return res.status(201).json({ detail: user });
  } catch (error) {
    return res.status(500).json({ detail: error });
  }
};

const login = async (req: Request, res: Response, next: NextFunction) => {
  const { name, password } = req.body;
  let user_name = name.toLowerCase();
  let user_password = password;
  const find_query = {
    name: user_name,
  };
  try {
    const user = await Users.findOne(find_query);
    if (user) {
      let check = await bcrypt.compare(user_password, user.password);
      if (check) {
        return res.status(200).json({ detail: "Logged in" });
      } else {
        return res.status(401).json({ detail: "Invalid Password" });
      }
    } else {
      return res.status(401).json({ detail: "Invalid User Name" });
    }
  } catch (error) {
    return res.status(401).json({ detail: error });
  }
};

export default {
  registerUser,
  login,
};
