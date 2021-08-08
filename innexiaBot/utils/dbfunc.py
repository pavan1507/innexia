import codecs
import pickle

from innexiaBot.mongo import db
from typing import Dict, List, Union


coupledb = db.couple
captchadb = db.captcha
captcha_cachedb = db.captcha_cache

# Couple Chooser

async def _get_lovers(chat_id: int):
    lovers = coupledb.find_one({"chat_id": chat_id})
    if lovers:
        lovers = lovers["couple"]
    else:
        lovers = {}
    return lovers


async def get_couple(chat_id: int, date: str):
    lovers = await _get_lovers(chat_id)
    if date in lovers:
        return lovers[date]
    else:
        return False


async def save_couple(chat_id: int, date: str, couple: dict):
    lovers = await _get_lovers(chat_id)
    lovers[date] = couple
    await coupledb.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "couple": lovers
            }
        },
        upsert=True
    )

#Captcha

async def is_captcha_on(chat_id: int) -> bool:
    chat = await captchadb.find_one({"chat_id": chat_id})
    if not chat:
        return True
    return False


async def captcha_on(chat_id: int):
    is_captcha = await is_captcha_on(chat_id)
    if is_captcha:
        return
    return await captchadb.delete_one({"chat_id": chat_id})


async def captcha_off(chat_id: int):
    is_captcha = await is_captcha_on(chat_id)
    if not is_captcha:
        return
    return await captchadb.insert_one({"chat_id": chat_id})

""" CAPTCHA CACHE SYSTEM """


async def update_captcha_cache(captcha_dict):
    pickle = obj_to_str(captcha_dict)
    await captcha_cachedb.delete_one({"captcha": "cache"})
    if not pickle:
        return
    await captcha_cachedb.update_one(
        {"captcha": "cache"},
        {"$set": {"pickled": pickle}},
        upsert=True,
    )


async def get_captcha_cache():
    cache = await captcha_cachedb.find_one({"captcha": "cache"})
    if not cache:
        return []
    return str_to_obj(cache["pickled"])

