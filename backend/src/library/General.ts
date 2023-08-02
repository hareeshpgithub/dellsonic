import chalk from "chalk";

export class general {
  public static getWeekDay = (unixTime: any) => {
    let i = 0;
    let data = { list: [{ dt: unixTime }] };

    let days = [
      "Sunday",
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
    ];
    let dayNum = new Date(data.list[i].dt * 1000).getDay();
    let result = days[dayNum];
    return result;
  };

  public static formatUnixTime = (unixTime: any) => {
    let a = new Date(unixTime * 1000);
    let months = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ];
    let year = a.getFullYear();
    let month = months[a.getMonth()];
    let date = ("0" + a.getDate()).slice(-2);
    let hour = ("0" + a.getHours()).slice(-2);
    let min = ("0" + a.getMinutes()).slice(-2);
    let time = date + " " + month + " " + year + " " + hour + ":" + min;
    return time;
  };

  public static formatUnixTimeDateOnly = (unixTime: any) => {
    let a = new Date(unixTime * 1000);
    let months = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ];
    let year = a.getFullYear();
    let month = months[a.getMonth()];
    let date = ("0" + a.getDate()).slice(-2);
    let time = date + " " + month + " " + year;
    return time;
  };
  public static titleCase = (str: any) => {
    let splitStr = str.toLowerCase().split(" ");
    for (let i = 0; i < splitStr.length; i++) {
      splitStr[i] =
        splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);
    }
    return splitStr.join(" ").trim();
  };

  public static getUnixTimeStamp = () => {
    return Math.floor(Date.now() / 1000);
  };

  public static decimalToFixed = (amount: any) => {
    return parseFloat(amount.toString()).toFixed(2);
  };

  public static mongoToNumber = (amount: any) => {
    return parseFloat(amount.toString());
  };

  public static workingTime = (dayStart: any, dayEnd: any) => {
    var seconds = Math.floor(dayEnd - dayStart);
    var minutes = Math.floor(seconds / 60);
    var hours = Math.floor(minutes / 60);
    var days = Math.floor(hours / 24);

    hours = hours - days * 24;
    minutes = minutes - days * 24 * 60 - hours * 60;
    seconds = seconds - days * 24 * 60 * 60 - hours * 60 * 60 - minutes * 60;
    return hours + ":" + minutes + ":" + seconds;
  };
}

export class logger {
  public static log = (args: any) => this.info(args);
  public static info = (args: any) =>
    console.log(
      chalk.green(`[${new Date().toString()}] [INFO]`),
      typeof args === "string" ? chalk.greenBright(args) : args
    );
  public static warning = (args: any) =>
    console.log(
      chalk.yellow(`[${new Date().toString()}] [WARN]`),
      typeof args === "string" ? chalk.yellowBright(args) : args
    );
  public static error = (args: any) =>
    console.log(
      chalk.red(`[${new Date().toString()}] [ERROR]`),
      typeof args === "string" ? chalk.redBright(args) : args
    );
  public static debug = (args: any) =>
    console.log(
      chalk.blue(`[${new Date().toString()}] [DEBUG]`),
      typeof args === "string" ? chalk.blueBright(args) : args
    );
}
