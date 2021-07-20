import os
import psutil

APP_SYSTEM = list()


def process_running(logger, name_process):
    try:
        for proc in psutil.process_iter(['name']):
            if proc.info["name"] == name_process:
                return True
        return False
    except:
        logger.error("Error en process_running")
        return None


def num_process_running(logger, name_process):
    try:
        num = 0
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info["name"] == name_process:
                num = num + 1
        return num
    except:
        logger.error("Error en num_process_running")
        return None


def delete_app_user(logger):
    try:
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.info["username"]:
                if proc.info["username"].find("usr_salas_autolog") > -1 and not proc.info["name"] in APP_SYSTEM:
                    os.system("taskkill /f /im " + proc.info["name"] + " /t")

    except:
        logger.error("Error en función delete_app_user ")


def app_system(logger):
    global APP_SYSTEM

    try:
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.info["username"]:
                if proc.info["username"].find("usr_salas_autolog") > -1:
                    APP_SYSTEM.append((proc.info["name"]))

    except:
        logger.error("Error en función AppSystem ")
