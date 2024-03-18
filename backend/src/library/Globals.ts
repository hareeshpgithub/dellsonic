import WebSocket from "ws";
export const clients: Set<WebSocket> = new Set();
export const command = "python3";
export const python_script = "dell.py";
export const parser_script = "parser.py";
export const excel_script = "excel.pyc";
export const python_func_device_backup = "devicebackup";
export const python_func_device_info = "deviceinfo";
export const python_func_images_list = "imageslist";
export const python_func_set_image = "setimage";
export const python_func_deploy_image = "deployimage";
export const python_func_remote_command = "remotecommand";
export const python_func_deploy_configuration = "deploy";
export const upload_folder = "uploads";
export const source_folder = "src";
export const sonicos4_folder = "sonicos4";
export const python_automation_folder = "dell";
export const output_folder = "output";
export const device_info_folder = "info";
export const device_config_folder = "backup";
export const websocket_message_filter = "TASK";
export const log_file = "log.txt";
