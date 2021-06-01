import os
import subprocess

import psutil

APP_SYSTEM = list()
LOGGER = None


def process_running(name_process):
    try:
        found = False
        for proc in psutil.process_iter():
            if proc.name() == name_process:
                found = True
        return found
    except:
        LOGGER.error("Error en ProcessRunning")


def num_process_running(name_process):
    try:
        num = 0
        for proc in psutil.process_iter():
            if proc.name() == name_process:
                num = num + 1
        return num
    except:
        LOGGER.error("Error en numProcessRunning")


def delete_app_user():
    global LOGGER

    try:
        command_taskApp = 'tasklist /fi "username eq usr_salas_autolog" /FO LIST'
        app_tasklist = subprocess.Popen(command_taskApp, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                        stderr=subprocess.PIPE, shell=True)
        (stdout, stderr) = app_tasklist.communicate()
        replace_string = stdout.replace(b' ', b'')
        replace_s1 = replace_string.replace(b'\r\n\r\n', b'\r\n')
        replace_s2 = replace_s1.replace(b'\r\n', b'|')
        replace_s3 = replace_s2.split(b'|')
        for val in replace_s3:
            Appsys = False
            if b'Nombredeimagen:' in val:
                value = val.split(b':')
                for programs in APP_SYSTEM:
                    if value[1] == programs:
                        Appsys = True
                if not Appsys:
                    command_kill = r'''taskkill /f /im  {}'''.format(str(value[1], 'utf-8'))
                    os.system(command_kill)
        pass

    except:
        LOGGER.error("Error en deleteAppUser")


def app_system(logger):
    global LOGGER
    LOGGER = logger

    try:
        command_taskApp = 'tasklist /fi "username eq usr_salas_autolog" /FO LIST'
        app_tasks = subprocess.Popen(command_taskApp, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                       stderr=subprocess.PIPE, shell=True)
        (stdout, stderr) = app_tasks.communicate()
        replace_string = stdout.replace(b' ', b'')
        replace_s1 = replace_string.replace(b'\r\n\r\n', b'\r\n')
        replace_s2 = replace_s1.replace(b'\r\n', b'|')
        replace_s3 = replace_s2.split(b'|')
        # print(reemplaceS3)
        for value in replace_s3:
            if b'Nombredeimagen:' in value:
                value_s = value.split(b':')
                APP_SYSTEM.append(value_s[1])
        pass

    except:
        logger.error("Error en función AppSystem ")
