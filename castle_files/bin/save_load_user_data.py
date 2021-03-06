"""
В данном модуле располагаются функции для дампа и подъёма пользовательских данных на диск (с диска)
"""
import castle_files.work_materials.globals as file_globals
from castle_files.bin.quests import construction_jobs, quest_players, quest_lock

from castle_files.libs.api import CW3API
from castle_files.bin.guild_chats import sort_worldtop

import time
import pickle
import logging
import sys

log = logging.getLogger("Save load user data")


def load_data():
    """
    Функция, которая загружает все данные (которые хранятся на диске) с диска
    :return: None
    """
    try:
        f = open('castle_files/backup/user_data', 'rb')
        file_globals.dispatcher.user_data = pickle.load(f)
        f.close()
    except FileNotFoundError:
        logging.error("Data file not found")
    try:
        f = open('castle_files/backup/api_info', 'rb')
        CW3API.api_info = pickle.load(f)
        f.close()
    except FileNotFoundError:
        logging.error("Data file not found")
    try:
        f = open('castle_files/backup/worldtop', 'rb')
        t = pickle.load(f)
        sort_worldtop(t)
    except FileNotFoundError:
        logging.error("Data file not found")
    try:
        f = open('castle_files/backup/castle_chats', 'rb')
        t = pickle.load(f)
        for chat_id in t:
            file_globals.castle_chats.append(chat_id)
        f.close()
    except FileNotFoundError:
        logging.error("Data file not found")
    except Exception:
        logging.error(sys.exc_info()[0])
    print("Data picked up")


def save_data():
    """
    Функция, которая сохраняет данные на диск раз в N (30) секунд, и перед завершением работы бота.
    :return: None
    """
    need_exit = 0
    while need_exit == 0:
        for i in range(0, 5):
            time.sleep(5)
            if not file_globals.processing:
                need_exit = 1
                break
        # Before pickling
        log.debug("Writing data, do not shutdown bot...\r")
        if need_exit:
            log.warning("Writing data last time, do not shutdown bot...")
        try:
            f = open('castle_files/backup/user_data', 'wb+')
            pickle.dump(file_globals.dispatcher.user_data, f)
            f.close()
            f = open('castle_files/backup/api_info', 'wb+')
            pickle.dump(CW3API.api_info, f)
            f.close()
            dump = {}
            for k, v in list(construction_jobs.items()):
                """if v.get_time_left() < 0:
                    construction_jobs.pop(k)
                    continue"""
                dump.update({k: [file_globals.dispatcher.user_data.get(k).get("status"), v.stop_time, v.job.context]})
            if file_globals.began:
                f = open('castle_files/backup/construction_jobs', 'wb+')
                pickle.dump(dump, f)
                f.close()
            f = open('castle_files/backup/castle_chats', 'wb+')
            pickle.dump(file_globals.castle_chats, f)
            f = open('castle_files/backup/quest_players', 'wb+')
            with quest_lock:
                pickle.dump(quest_players, f)
            f.close()
            log.debug("Data write completed\b")
        except Exception:
            logging.error(sys.exc_info()[0])
