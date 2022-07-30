import sys
sys.path.append("..")
import re
import json
import codecs
import requests
import os
import config

def get_comment(url:str) -> list[dict]:
    """
    get all comments list from URL then save file and return in json type 

    Args:
        url (str): shopee product url exmple https://shopee.co.th/Notebook-Lenovo-Legion-Y500_82JU007LTA_15ACH6H-(BL)-Ryzen-5-5600H-16GB-512GB-NVMe-no-DVD-RTX-3060-(6GB)-15.6-Win10-3Y-i.22495699.9876744203?sp_atk=fd9b42b6-bb13-4a60-9701-e03bdd328dba&xptdk=fd9b42b6-bb13-4a60-9701-e03bdd328dba

    Returns:
        list[dict]: list of comments in python dict type ({"user": user, "star": star, "comment": comment})
    """

    r = re.search(r'i\.(\d+)\.(\d+)', url)
    shop_id, item_id = r[1], r[2]
    ratings_url = 'https://shopee.co.id/api/v2/item/get_ratings?filter=0&flag=1&itemid={item_id}&limit=20&offset={offset}&shopid={shop_id}&type=0'
    offset = 0
    result = []
    while True:

        data = requests.get(ratings_url.format(shop_id=shop_id, item_id=item_id, offset=offset)).json()

        for i, rating in enumerate(data['data']['ratings'], 1):

            user = rating['author_username']
            star = rating['rating_star']
            comment = rating['comment']
            value = {"user": user, "star": star, "comment": comment}
            result.append(value)
        if i % 20:
            break
        offset += 20
    resultJson = json.dumps(result, ensure_ascii=False)

    if not os.path.exists(config.DATA_DIR):
        os.mkdir(config.DATA_DIR)

    with codecs.open(f'{config.DATA_DIR}/{shop_id}-{item_id}.json', 'w', encoding='utf-8') as f:    
        f.write(resultJson)

    return result  

