// import express, { Request, Response, NextFunction } from "express";
import { Request, Response, NextFunction } from "express";
import { general, logger } from "../library/General";

import path from "path";

const NewConfig = async (req: Request, res: Response, next: NextFunction) => {
  const options = {
    root: path.join("uploads"),
  };
  // Set the content type explicitly before sending the file
  res.contentType(
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
  );

  return res.status(200).sendFile("New.xlsx", options, function (err) {
    if (err) {
      next(err);
    }
  });
};
export default {
  NewConfig,
};
