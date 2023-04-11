import os
import requests
from flask import request
from typing import List, Any

def split_dict(dictionary, parts):
    n = len(dictionary)
    part_size = n // parts
    return [dict(list(dictionary.items())[i:i + part_size]) for i in range(0, n, part_size)]

def lookup(param):
    # Set API key and ID manually
    api_key = "51bc41f2ca1657d3ee7e76e0e360ba85"
    api_id = "910f2a02"

def stringify(list_name, string):
    list = request.args.getlist(list_name)
    arr = []
    for l in list:
        arr.append(string + l)
    stringified = "".join(arr)
    return list, stringified
        
    
def lookup(param):
    try:
        api_key = os.environ.get("API_KEY")
        api_id = os.environ.get("API_ID")
        response = requests.get(
            f"https://api.edamam.com/api/recipes/v2?type=public&app_id={api_id}&app_key={api_key}&q={param}")
        response.raise_for_status()
    except requests.RequestException:
        return None
    try:
        result = response.json()
        # count = result["count"]
        # next = result["_links"]["next"]["href"]
        hits_dict = result["hits"]
        recipes_list = []
        for index in hits_dict:
            link = index["_links"]["self"]["href"]  # Recipe's JSON link
            label = index["recipe"]["label"]
            image = index["recipe"]["image"]
            source = index["recipe"]["source"]
            url = index["recipe"]["url"]  # Source link
            dietLabels = list(index["recipe"]["dietLabels"])
            healthLabels = list(index["recipe"]["healthLabels"])
            ingredientLines = list(index["recipe"]["ingredientLines"])
            calories = index["recipe"]["calories"]
            totalTime = index["recipe"]["totalTime"]
            cuisineType = list(index["recipe"]["cuisineType"])
            dishType = list(index["recipe"]["dishType"])
            recipes_list.append(
                {
                    "link": link,
                    "label": label,
                    "image": image,
                    "source": source,
                    "url": url,
                    "dietLabels": dietLabels,
                    "healthLabels": healthLabels,
                    "ingredientLines": ingredientLines,
                    "calories": calories,
                    "totalTime": totalTime,
                    "cuisineType": cuisineType,
                    "dishType": dishType
                })
        return recipes_list  # , next, count
    except (KeyError, TypeError, ValueError):
        return None


def readable_list(seq: List[Any]) -> str:
    """
    Grammatically correct human readable string from list (with Oxford comma)
    https://stackoverflow.com/a/53981846/19845029
    """
    seq = [str(s) for s in seq]
    if len(seq) < 3:
        return ' and '.join(seq)
    return ', '.join(seq[:-1]) + ', and ' + seq[-1]

