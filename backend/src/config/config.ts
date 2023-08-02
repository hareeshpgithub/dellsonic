import dotenv from "dotenv";

dotenv.config();

const MONGO_USERNAME = process.env.MONGO_USERNAME || "aarohi-admin";
const MONGO_PASSWORD = process.env.MONGO_PASSWORD || "aarohi@12345";

const SERVER_PORT = process.env.PORT ? Number(process.env.PORT) : 1202;
const WEBSOCKET_SERVER_PORT = process.env.WEBSOCKET_PORT
  ? Number(process.env.WEBSOCKET_PORT)
  : 1204;

export const config = {
  mongo: {
    url: "mongodb://127.0.0.1:27017/aarohi",
  },
  server: {
    port: SERVER_PORT,
    websocket_port: WEBSOCKET_SERVER_PORT,
  },
};
