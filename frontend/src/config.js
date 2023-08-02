const live = false;
let baseUrlV1 = "http://localhost:1202";
if (live) {
  baseUrlV1 = "";
}
const versionV1 = "/api/sonic4/v1";
export const APIS = {
  login: `${baseUrlV1}${versionV1}/users/login`,
  upload_backup: `${baseUrlV1}${versionV1}/device/backuptoyml`,
  upload_excel: `${baseUrlV1}${versionV1}/device/exceltoyml`,
  device_info: `${baseUrlV1}${versionV1}/device/deviceinfo`,
  device_backup: `${baseUrlV1}${versionV1}/device/deviceconfig`,
  device_deploy: `${baseUrlV1}${versionV1}/device/deploy`,
  new_config_file: `${baseUrlV1}${versionV1}/device/newtemplate`,

  timeout: 15 * 60 * 1000,
};

const Config = {
  apis: { ...APIS },
};

export default Config;
