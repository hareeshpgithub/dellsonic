import express from "express";
import http from "http";
import mongoose from "mongoose";
import { config } from "./config/config";
import { logger } from "./library/General";
import allRoutes from "./routes/Common";
import WebSocket from "ws";
import { clients } from "./library/Globals";

const router = express();

/** Connect to Mongo */
mongoose
  .set("strictQuery", false)
  .connect(config.mongo.url, { retryWrites: true, w: "majority" })
  .then(() => {
    logger.info("Mongo connected successfully.");
    StartServer();
  })
  .catch((error) => logger.error(error));

/** Only Start Server if Mongoose Connects */
const StartServer = () => {
  /** StartWebsocket */
  const wss = new WebSocket.Server({ port: config.server.websocket_port });
  wss.on("connection", (ws: any) => {
    clients.add(ws);
    ws.on("close", () => {
      clients.delete(ws);
    });
  });
  /** Log the request */
  router.use((req, res, next) => {
    /** Log the req */
    logger.info(
      `Incoming - METHOD: [${req.method}] - URL: [${req.url}] - IP: [${req.socket.remoteAddress}]`
    );

    res.on("finish", () => {
      /** Log the res */
      logger.info(
        `Result - METHOD: [${req.method}] - URL: [${req.url}] - IP: [${req.socket.remoteAddress}] - STATUS: [${res.statusCode}]`
      );
    });

    next();
  });

  router.use(express.urlencoded({ extended: true }));
  router.use(express.json());

  /** Rules of our API */
  router.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header(
      "Access-Control-Allow-Headers",
      "Origin, X-Requested-With, Content-Type, Accept, Authorization"
    );

    if (req.method == "OPTIONS") {
      res.header(
        "Access-Control-Allow-Methods",
        "PUT, POST, PATCH, DELETE, GET"
      );
      return res.status(200).json({});
    }

    next();
  });

  /** Routes */
  router.use("/api/sonic4/v1/users", allRoutes);
  router.use("/api/sonic4/v1/device", allRoutes);

  /** Health check */
  router.get("/ping", (req, res, next) =>
    res.status(200).json({ result: "pong" })
  );

  router.post("/ping", (req, res, next) =>
    res.status(200).json({ result: "pong" })
  );

  /** Error handling */
  router.use((req, res, next) => {
    const error = new Error("API Not Found");
    logger.error(error);
    res.status(404).json({
      message: error.message,
    });
  });

  http
    .createServer(router)
    .listen(config.server.port, () =>
      logger.info(`Server is running on port ${config.server.port}`)
    );
};
