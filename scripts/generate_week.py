from __future__ import annotations

import datetime as dt
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
PLAN_JSON = DATA_DIR / "meal-plan.json"
DATA_JS = ROOT / "data.js"
DAY_NAMES = ["月", "火", "水", "木", "金"]
GROUPS = ["野菜", "肉・魚・大豆", "乾物・その他"]


def shop(veg=None, protein=None, other=None):
    return {"野菜": veg or [], "肉・魚・大豆": protein or [], "乾物・その他": other or []}


def menu(id, main, url, rice, soup, vegetable, work, before, after, protein, tags, shopping):
    return {
        "id": id,
        "main": main,
        "sourceName": "リュウジのバズレシピ",
        "sourceUrl": url,
        "rice": rice,
        "soup": soup,
        "vegetable": vegetable,
        "work": work,
        "before": before,
        "after": after,
        "protein": protein,
        "tags": tags,
        "shopping": shopping,
    }


URLS = {
    "pork_cabbage_steam": "https://bazurecipe.com/2023/04/30/%e3%82%ad%e3%83%a3%e3%83%99%e3%83%84%e3%81%a8%e8%b1%9a%e3%81%93%e3%81%be%e3%81%ae%e3%81%ab%e3%82%93%e3%81%ab%e3%81%8f%e9%85%92%e8%92%b8%e3%81%97/",
    "pork_cabbage_miso": "https://bazurecipe.com/2023/10/03/%e6%9c%ac%e5%bd%93%e3%81%ab%e7%be%8e%e5%91%b3%e3%81%97%e3%81%84%e8%b1%9a%e3%82%ad%e3%83%a3%e3%83%99%e3%83%84/",
    "chicken_eggplant_nanban": "https://bazurecipe.com/2024/07/07/%e9%b6%8f%e3%81%aa%e3%81%99%e5%8d%97%e8%9b%ae/",
    "stuffed_green_pepper": "https://bazurecipe.com/2025/06/02/%e7%b5%b6%e5%af%be%e5%89%9d%e3%81%8c%e3%82%8c%e3%81%aa%e3%81%84%e3%83%94%e3%83%bc%e3%83%9e%e3%83%b3%e3%81%ae%e8%82%89%e8%a9%b0%e3%82%81/",
    "chicken_tomato": "https://bazurecipe.com/2021/02/09/8526/",
    "mini_tomato_pasta": "https://bazurecipe.com/2024/05/02/%e3%81%82%e3%81%be%e3%82%8a%e3%81%ab%e3%82%82%e7%be%8e%e5%91%b3%e3%81%97%e3%81%84%e3%83%9f%e3%83%8b%e3%83%88%e3%83%9e%e3%83%88%e3%81%ae%e3%83%91%e3%82%b9%e3%82%bf/",
    "tomato_pasta": "https://bazurecipe.com/2023/04/09/%e8%99%9a%e7%84%a1%e3%83%88%e3%83%9e%e3%83%88%e3%83%91%e3%82%b9%e3%82%bf/",
    "tomato_garlic_pasta": "https://bazurecipe.com/2024/03/05/%e8%87%b3%e9%ab%98%e3%82%92%e8%b6%8a%e3%81%88%e3%81%9f%e3%83%88%e3%83%9e%e3%83%88%e3%81%a8%e3%81%ab%e3%82%93%e3%81%ab%e3%81%8f%e3%81%ae%e3%83%91%e3%82%b9%e3%82%bf/",
    "microwave_tomato_pasta": "https://bazurecipe.com/2025/06/19/%e8%99%9a%e7%84%a1%e3%83%ac%e3%83%b3%e3%82%b8%e3%83%88%e3%83%9e%e3%83%88%e3%82%bd%e3%83%bc%e3%82%b9%e3%83%91%e3%82%b9%e3%82%bf/",
    "cold_tomato_pasta": "https://bazurecipe.com/2025/10/08/%e3%83%88%e3%83%9e%e3%83%88%e7%bc%b6%e3%81%a7%e4%bd%9c%e3%82%8b%e5%86%b7%e8%a3%bd%e3%83%91%e3%82%b9%e3%82%bf/",
    "pork_green_pepper_tsukune": "https://bazurecipe.com/2024/08/01/%e3%83%94%e3%83%bc%e3%83%9e%e3%83%b3%e8%b1%9a%e3%81%93%e3%81%be%e3%81%a4%e3%81%8f%e3%81%ad/",
    "pork_green_pepper_stuffed": "https://bazurecipe.com/2024/01/08/%e3%83%94%e3%83%bc%e3%83%9e%e3%83%b3%e3%81%ae%e8%b1%9a%e3%81%93%e3%81%be%e8%a9%b0%e3%82%81/",
    "buta_ten": "https://bazurecipe.com/2023/12/28/%e8%b1%9a%e3%81%93%e3%81%be%e8%82%89%e3%81%a7%e4%bd%9c%e3%82%8b%e3%81%b6%e3%81%9f%e5%a4%a9/",
    "onion_pork_curry": "https://bazurecipe.com/2025/09/28/%e7%8e%89%e3%81%ad%e3%81%8e%e3%81%a8%e8%b1%9a%e3%81%93%e3%81%be%e3%81%ae%e3%82%ab%e3%83%ac%e3%83%bc/",
    "chicken_breast_steak": "https://bazurecipe.com/2026/02/01/%e7%a9%b6%e6%a5%b5%e3%81%ae%e9%b6%8f%e3%82%80%e3%81%ad%e3%82%b9%e3%83%86%e3%83%bc%e3%82%ad/",
    "chicken_breast_cabbage": "https://bazurecipe.com/2025/05/23/%e9%b6%8f%e3%82%80%e3%81%ad%e8%82%89%e3%81%a8%e3%82%ad%e3%83%a3%e3%83%99%e3%83%84%e3%81%ae%e5%a1%a9%e3%81%91%e3%81%84%e3%81%a1%e3%82%83%e3%82%93/",
    "hikiniku_nira_tofu": "https://bazurecipe.com/2020/05/18/%e3%81%b2%e3%81%8d%e8%82%89%e3%83%8b%e3%83%a9%e8%b1%86%e8%85%90/",
    "ginger_hikiniku_tofu": "https://bazurecipe.com/2020/05/02/%e7%88%86%e9%80%9f%e3%82%b7%e3%83%a7%e3%82%a6%e3%82%ac%e3%81%b2%e3%81%8d%e8%82%89%e8%b1%86%e8%85%90/",
    "atsuage_pork_roll": "https://bazurecipe.com/2024/03/24/%e5%8e%9a%e6%8f%9a%e3%81%92%e3%81%ae%e3%83%8b%e3%83%a9%e3%83%81%e3%83%bc%e3%82%ba%e8%b1%9a%e5%b7%bb%e3%81%8d/",
    "atsuage_ginger": "https://bazurecipe.com/2020/05/16/%e5%8e%9a%e6%8f%9a%e3%81%92%e3%81%ae%e3%82%b8%e3%83%b3%e3%82%b8%e3%83%a3%e3%83%bc%e3%82%b9%e3%83%86%e3%83%bc%e3%82%ad/",
    "moyashi_egg_namul": "https://bazurecipe.com/2025/06/12/%e3%82%82%e3%82%84%e3%81%97%e3%81%a8%e5%8d%b5%e3%81%ae%e3%83%8a%e3%83%a0%e3%83%ab/",
    "saba_salad": "https://bazurecipe.com/2025/06/21/%e3%81%95%e3%81%b0%e3%82%b5%e3%83%a9%e3%83%80/",
    "kyomu_abura_udon": "https://bazurecipe.com/2025/06/25/%e8%99%9a%e7%84%a1%e6%b2%b9%e3%81%86%e3%81%a9%e3%82%93/",
    "kyomu_kayu": "https://bazurecipe.com/2025/05/19/%e8%99%9a%e7%84%a1%e7%b2%a5/",
}


MENUS = {
    "normal": [
        menu("pork_cabbage_steam", "キャベツと豚こまのにんにく酒蒸し", URLS["pork_cabbage_steam"], "白ごはん", "豆腐・わかめの味噌汁", "きゅうりとミニトマトのごま酢サラダ", "下準備10分 + 仕上げ15分", "キャベツを切る。豚こまに下味をつける。", "主菜を蒸す。味噌汁とサラダを仕上げる。", "pork", ["protein", "vegetable"], shop([["キャベツ", "約375g", "キャベツと豚こまのにんにく酒蒸し"], ["きゅうり", "1本", "ごま酢サラダ"], ["ミニトマト", "1/2パック", "ごま酢サラダ"]], [["豚こま肉", "300g", "キャベツと豚こまのにんにく酒蒸し"], ["豆腐", "1/2丁", "味噌汁"]], [["乾燥わかめ", "適量", "味噌汁"]])),
        menu("chicken_eggplant_nanban", "鶏なす南蛮", URLS["chicken_eggplant_nanban"], "白ごはん", "新玉ねぎ・油揚げの味噌汁", "レタスとにんじんの塩昆布サラダ", "下準備12分 + 仕上げ15分", "なす乱切り、鶏もも一口大。南蛮だれを合わせる。", "鶏となすを炒めてたれを絡める。味噌汁とサラダを仕上げる。", "chicken", ["protein", "vegetable", "make_ahead"], shop([["なす", "3本", "鶏なす南蛮"], ["玉ねぎ", "1個", "鶏なす南蛮・味噌汁"], ["レタス", "1/2玉", "塩昆布サラダ"], ["にんじん", "1/2本", "塩昆布サラダ"]], [["鶏もも肉", "330g", "鶏なす南蛮"], ["油揚げ", "1枚", "味噌汁"]], [["塩昆布", "適量", "塩昆布サラダ"]])),
        menu("stuffed_green_pepper", "絶対剥がれないピーマンの肉詰め", URLS["stuffed_green_pepper"], "白ごはん", "キャベツ・えのきの味噌汁", "トマトと大葉の冷やしサラダ", "下準備15分 + 仕上げ10分", "ピーマン半割り。肉だねを混ぜて詰める。", "肉詰めを焼く。味噌汁とサラダを盛る。", "beef_pork", ["iron", "vegetable"], shop([["ピーマン", "8個", "ピーマンの肉詰め"], ["キャベツ", "1/8玉", "味噌汁"], ["トマト", "2個", "冷やしサラダ"], ["大葉", "1束", "冷やしサラダ"]], [["合い挽き肉", "375g", "ピーマンの肉詰め"]], [["えのき", "1袋", "味噌汁"]])),
        menu("pork_cabbage_miso", "本当に美味しい豚キャベツ", URLS["pork_cabbage_miso"], "白ごはん", "大根・にんじん・油揚げの味噌汁", "豆腐と水菜のサラダ", "下準備8分 + 仕上げ12分", "豚こま解凍。キャベツを切る。たれを合わせる。", "肉を炒めてキャベツを合わせる。味噌汁とサラダを仕上げる。", "pork", ["protein", "soy", "vegetable"], shop([["キャベツ", "約350g", "豚キャベツ"], ["大根", "1/4本", "味噌汁"], ["にんじん", "1/2本", "味噌汁"], ["水菜", "1袋", "豆腐サラダ"]], [["豚こま肉", "300g", "豚キャベツ"], ["豆腐", "1丁", "豆腐サラダ"], ["油揚げ", "1枚", "味噌汁"]])),
        menu("chicken_tomato", "至高のチキントマト煮", URLS["chicken_tomato"], "白ごはん", "玉ねぎと卵のスープ", "ブロッコリーサラダ", "下準備12分 + 仕上げ18分", "鶏肉、なす、玉ねぎを切る。", "鶏肉となすを焼いてトマト缶で煮る。", "chicken", ["protein", "vegetable"], shop([["なす", "3本", "チキントマト煮"], ["玉ねぎ", "1個", "チキントマト煮・スープ"], ["ブロッコリー", "1株", "サラダ"]], [["鶏もも肉", "350g", "チキントマト煮"], ["卵", "2個", "スープ"]], [["トマト缶", "1缶", "チキントマト煮"]])),
        menu("pork_green_pepper_tsukune", "ピーマン豚こまつくね", URLS["pork_green_pepper_tsukune"], "白ごはん", "豆腐・小ねぎの味噌汁", "トマトときゅうりのサラダ", "下準備12分 + 仕上げ13分", "ピーマンを切る。豚こまをまとめる。", "つくねを焼く。味噌汁とサラダを仕上げる。", "pork", ["protein", "vegetable"], shop([["ピーマン", "6個", "ピーマン豚こまつくね"], ["トマト", "2個", "サラダ"], ["きゅうり", "1本", "サラダ"], ["小ねぎ", "適量", "味噌汁"]], [["豚こま肉", "350g", "ピーマン豚こまつくね"], ["豆腐", "1/2丁", "味噌汁"]])),
        menu("pork_green_pepper_stuffed", "ピーマンの豚こま詰め", URLS["pork_green_pepper_stuffed"], "白ごはん", "わかめ・卵の味噌汁", "水菜と豆腐のサラダ", "下準備12分 + 仕上げ12分", "ピーマンを切る。豚こまを詰める。", "フライパンで焼く。味噌汁とサラダを仕上げる。", "pork", ["protein", "vegetable"], shop([["ピーマン", "6個", "ピーマンの豚こま詰め"], ["水菜", "1袋", "サラダ"]], [["豚こま肉", "350g", "ピーマンの豚こま詰め"], ["卵", "2個", "味噌汁"], ["豆腐", "1丁", "サラダ"]], [["乾燥わかめ", "適量", "味噌汁"]])),
        menu("chicken_breast_steak", "究極の鶏むねステーキ", URLS["chicken_breast_steak"], "白ごはん", "大根・小ねぎの味噌汁", "ブロッコリーとトマトのサラダ", "下準備10分 + 仕上げ15分", "鶏むねに下味をつける。野菜を洗う。", "鶏むねを焼く。味噌汁とサラダを仕上げる。", "chicken", ["protein", "quick"], shop([["大根", "1/4本", "味噌汁"], ["小ねぎ", "適量", "味噌汁"], ["ブロッコリー", "1株", "サラダ"], ["トマト", "2個", "サラダ"]], [["鶏むね肉", "2枚", "鶏むねステーキ"]])),
        menu("chicken_breast_cabbage", "鶏むね肉とキャベツの塩けいちゃん", URLS["chicken_breast_cabbage"], "白ごはん", "豆腐・わかめの味噌汁", "きゅうりとミニトマト", "下準備10分 + 仕上げ15分", "鶏むねとキャベツを切る。", "炒めて仕上げる。味噌汁と野菜を出す。", "chicken", ["protein", "vegetable"], shop([["キャベツ", "1/2玉", "塩けいちゃん"], ["きゅうり", "1本", "野菜"], ["ミニトマト", "1パック", "野菜"]], [["鶏むね肉", "2枚", "塩けいちゃん"], ["豆腐", "1/2丁", "味噌汁"]], [["乾燥わかめ", "適量", "味噌汁"]])),
        menu("hikiniku_nira_tofu", "ひき肉ニラ豆腐", URLS["hikiniku_nira_tofu"], "白ごはん", "もやし・卵の味噌汁", "トマトと大葉のサラダ", "下準備8分 + 仕上げ12分", "ニラと豆腐を切る。", "ひき肉と豆腐を炒め煮にする。", "pork", ["soy", "iron", "quick"], shop([["ニラ", "1束", "ひき肉ニラ豆腐"], ["もやし", "1袋", "味噌汁"], ["トマト", "2個", "サラダ"], ["大葉", "1束", "サラダ"]], [["豚ひき肉", "250g", "ひき肉ニラ豆腐"], ["豆腐", "2丁", "ひき肉ニラ豆腐"], ["卵", "2個", "味噌汁"]])),
        menu("atsuage_pork_roll", "厚揚げのニラチーズ豚巻き", URLS["atsuage_pork_roll"], "白ごはん", "キャベツ・油揚げの味噌汁", "水菜サラダ", "下準備12分 + 仕上げ13分", "厚揚げとニラを切り、豚肉で巻く。", "巻いたものを焼く。味噌汁とサラダを仕上げる。", "pork_soy", ["soy", "calcium"], shop([["ニラ", "1束", "厚揚げ豚巻き"], ["キャベツ", "1/8玉", "味噌汁"], ["水菜", "1袋", "サラダ"]], [["厚揚げ", "2枚", "厚揚げ豚巻き"], ["豚バラ肉", "300g", "厚揚げ豚巻き"], ["チーズ", "適量", "厚揚げ豚巻き"], ["油揚げ", "1枚", "味噌汁"]])),
    ],
    "tired": [
        menu("tomato_pasta", "虚無トマトパスタ", URLS["tomato_pasta"], "なし", "即席味噌汁", "袋サラダ + 豆腐", "下準備3分 + 仕上げ12分", "トマト缶とパスタを出す。", "ワンパンでパスタを仕上げる。サラダに豆腐をのせる。", "light", ["quick", "limit"], shop([["袋サラダ", "1袋", "サラダ"]], [["豆腐", "1丁", "サラダ"]], [["パスタ", "300g", "虚無トマトパスタ"], ["トマト缶", "1缶", "虚無トマトパスタ"], ["即席味噌汁", "1食", "汁物"]])),
        menu("mini_tomato_pasta", "ミニトマトのパスタ", URLS["mini_tomato_pasta"], "なし", "即席味噌汁", "カット野菜サラダ", "下準備5分 + 仕上げ12分", "ミニトマトを洗う。にんにくを出す。", "ワンパンでパスタを仕上げる。サラダを添える。", "light", ["quick", "vegetable"], shop([["ミニトマト", "1パック", "ミニトマトのパスタ"], ["カット野菜", "1袋", "サラダ"]], [], [["パスタ", "300g", "ミニトマトのパスタ"], ["即席味噌汁", "1食", "汁物"]])),
        menu("buta_ten", "豚こま肉で作るぶた天", URLS["buta_ten"], "白ごはん", "豆腐・わかめの味噌汁", "袋サラダ", "下準備8分 + 仕上げ15分", "豚こまに下味。衣を作る。", "揚げ焼きする。味噌汁と袋サラダを用意。", "pork", ["protein"], shop([["袋サラダ", "1袋", "サラダ"]], [["豚こま肉", "350g", "ぶた天"], ["豆腐", "1/2丁", "味噌汁"]], [["乾燥わかめ", "適量", "味噌汁"]])),
        menu("onion_pork_curry", "玉ねぎと豚こまのカレー", URLS["onion_pork_curry"], "白ごはん", "即席味噌汁", "ミニトマト", "下準備7分 + 仕上げ15分", "玉ねぎを切る。豚こまを出す。", "カレーを作る。ミニトマトを添える。", "pork", ["protein", "quick"], shop([["玉ねぎ", "2個", "カレー"], ["ミニトマト", "1パック", "野菜"]], [["豚こま肉", "300g", "カレー"]], [["カレールー", "適量", "カレー"], ["即席味噌汁", "1食", "汁物"]])),
        menu("microwave_tomato_pasta", "虚無レンジトマトソースパスタ", URLS["microwave_tomato_pasta"], "なし", "即席味噌汁", "冷凍ブロッコリー", "下準備2分 + 仕上げ10分", "耐熱容器に材料を入れる。", "レンジ加熱。ブロッコリーを温める。", "light", ["quick", "limit"], shop([["冷凍ブロッコリー", "1袋", "野菜"]], [], [["パスタ", "300g", "レンジトマトパスタ"], ["トマト缶", "1缶", "レンジトマトパスタ"], ["即席味噌汁", "1食", "汁物"]])),
        menu("cold_tomato_pasta", "トマト缶で作る冷製パスタ", URLS["cold_tomato_pasta"], "なし", "即席味噌汁", "豆腐と水菜のサラダ", "下準備5分 + 仕上げ10分", "パスタを茹でる準備。トマト缶を冷やす。", "パスタを冷やして和える。サラダを出す。", "light", ["quick"], shop([["水菜", "1袋", "サラダ"]], [["豆腐", "1丁", "サラダ"]], [["パスタ", "300g", "冷製パスタ"], ["トマト缶", "1缶", "冷製パスタ"], ["即席味噌汁", "1食", "汁物"]])),
        menu("ginger_hikiniku_tofu", "爆速ショウガひき肉豆腐", URLS["ginger_hikiniku_tofu"], "白ごはん", "即席味噌汁", "袋サラダ", "下準備5分 + 仕上げ8分", "豆腐を切り、しょうがを出す。", "ひき肉と豆腐を炒める。サラダを出す。", "pork_soy", ["soy", "quick"], shop([["袋サラダ", "1袋", "サラダ"]], [["豚ひき肉", "250g", "主菜"], ["豆腐", "2丁", "主菜"]], [["即席味噌汁", "1食", "汁物"]])),
        menu("atsuage_ginger", "厚揚げのジンジャーステーキ", URLS["atsuage_ginger"], "白ごはん", "即席味噌汁", "カット野菜", "下準備3分 + 仕上げ10分", "厚揚げを切る。", "厚揚げを焼く。カット野菜を出す。", "soy", ["soy", "quick"], shop([["カット野菜", "1袋", "野菜"]], [["厚揚げ", "2枚", "主菜"]], [["即席味噌汁", "1食", "汁物"]])),
        menu("saba_salad", "さばサラダ", URLS["saba_salad"], "白ごはん", "即席味噌汁", "さばサラダを野菜料理兼用", "下準備3分 + 仕上げ5分", "野菜を出す。さば缶を開ける。", "盛り付ける。ごはんと味噌汁を用意。", "fish", ["fish", "quick"], shop([["袋サラダ", "1袋", "さばサラダ"]], [["さば缶", "2缶", "さばサラダ"]], [["即席味噌汁", "1食", "汁物"]])),
        menu("moyashi_egg_namul", "もやしと卵のナムル", URLS["moyashi_egg_namul"], "白ごはん", "即席味噌汁", "トマトと豆腐", "下準備3分 + 仕上げ8分", "もやしを洗う。卵を出す。", "もやしと卵を調理し、豆腐とトマトを添える。", "egg", ["quick"], shop([["もやし", "2袋", "もやしと卵のナムル"], ["トマト", "2個", "野菜"]], [["卵", "3個", "もやしと卵のナムル"], ["豆腐", "1丁", "野菜"]], [["即席味噌汁", "1食", "汁物"]])),
    ],
    "limit": [
        menu("tomato_pasta", "虚無トマトパスタ", URLS["tomato_pasta"], "なし", "即席味噌汁", "袋サラダ", "下準備0分 + 仕上げ12分", "なし。", "ワンパンで作る。袋サラダを出す。", "light", ["quick", "limit"], shop([["袋サラダ", "1袋", "サラダ"]], [], [["パスタ", "300g", "虚無トマトパスタ"], ["トマト缶", "1缶", "虚無トマトパスタ"], ["即席味噌汁", "1食", "汁物"]])),
        menu("microwave_tomato_pasta", "虚無レンジトマトソースパスタ", URLS["microwave_tomato_pasta"], "なし", "即席味噌汁", "冷奴", "下準備0分 + 仕上げ10分", "なし。", "レンジで作る。豆腐を出す。", "light", ["quick", "limit"], shop([], [["豆腐", "1丁", "冷奴"]], [["パスタ", "300g", "レンジトマトパスタ"], ["トマト缶", "1缶", "レンジトマトパスタ"], ["即席味噌汁", "1食", "汁物"]])),
        menu("mini_tomato_pasta", "ミニトマトのパスタ", URLS["mini_tomato_pasta"], "なし", "即席味噌汁", "カット野菜", "下準備3分 + 仕上げ10分", "ミニトマトを洗う。", "ワンパンで作る。カット野菜を出す。", "light", ["quick", "limit"], shop([["ミニトマト", "1パック", "ミニトマトのパスタ"], ["カット野菜", "1袋", "野菜"]], [], [["パスタ", "300g", "ミニトマトのパスタ"], ["即席味噌汁", "1食", "汁物"]])),
        menu("onion_pork_curry", "玉ねぎと豚こまのカレー", URLS["onion_pork_curry"], "パックごはん可", "即席味噌汁", "袋サラダ", "下準備5分 + 仕上げ15分", "玉ねぎを切る。", "カレーを作る。パックごはんでもOK。", "pork", ["quick"], shop([["玉ねぎ", "2個", "カレー"], ["袋サラダ", "1袋", "サラダ"]], [["豚こま肉", "300g", "カレー"]], [["カレールー", "適量", "カレー"], ["パックごはん", "必要分", "主食"], ["即席味噌汁", "1食", "汁物"]])),
        menu("pork_cabbage_miso", "本当に美味しい豚キャベツ", URLS["pork_cabbage_miso"], "パックごはん可", "即席味噌汁", "カット野菜", "下準備5分 + 仕上げ12分", "キャベツを切る。", "肉とキャベツを炒める。即席味噌汁を用意。", "pork", ["protein"], shop([["キャベツ", "約350g", "豚キャベツ"], ["カット野菜", "1袋", "野菜"]], [["豚こま肉", "300g", "豚キャベツ"]], [["即席味噌汁", "1食", "汁物"], ["パックごはん", "必要分", "主食"]])),
        menu("kyomu_abura_udon", "虚無油うどん", URLS["kyomu_abura_udon"], "なし", "即席味噌汁", "冷凍ほうれん草", "下準備0分 + 仕上げ7分", "なし。", "うどんを作り、冷凍ほうれん草を足す。", "light", ["quick", "limit"], shop([["冷凍ほうれん草", "1袋", "野菜"]], [], [["冷凍うどん", "3玉", "虚無油うどん"], ["即席味噌汁", "1食", "汁物"]])),
        menu("kyomu_kayu", "虚無粥", URLS["kyomu_kayu"], "粥", "粥を汁物兼用", "豆腐とミニトマト", "下準備0分 + 仕上げ8分", "なし。", "粥を作る。豆腐とミニトマトを出す。", "light", ["quick", "limit"], shop([["ミニトマト", "1パック", "野菜"]], [["豆腐", "1丁", "野菜"]], [["米またはパックごはん", "必要分", "虚無粥"]])),
        menu("saba_salad", "さばサラダ", URLS["saba_salad"], "パックごはん", "即席味噌汁", "さばサラダを野菜料理兼用", "下準備0分 + 仕上げ5分", "なし。", "さば缶と袋サラダを盛る。", "fish", ["fish", "quick", "limit"], shop([["袋サラダ", "1袋", "さばサラダ"]], [["さば缶", "2缶", "さばサラダ"]], [["パックごはん", "必要分", "主食"], ["即席味噌汁", "1食", "汁物"]])),
    ],
}


def plan_monday(today: dt.date) -> dt.date:
    if today.weekday() <= 4:
        return today - dt.timedelta(days=today.weekday())
    return today + dt.timedelta(days=7 - today.weekday())


def analyze_previous(previous: dict | None) -> dict:
    if not previous:
        return {"summary": "初回生成のため前週データなし。", "boost": ["fish", "soy", "calcium"], "previous_ids": {}}
    plans = previous.get("plans", {})
    normal_dinners = previous.get("dinners") or plans.get("normal", {}).get("dinners", [])
    tags = Counter(tag for dinner in normal_dinners for tag in dinner.get("tags", []))
    proteins = Counter(dinner.get("protein", "") for dinner in normal_dinners)
    boost = []
    if tags["fish"] < 1:
        boost.append("fish")
    if tags["soy"] < 1:
        boost.append("soy")
    if tags["calcium"] < 2:
        boost.append("calcium")
    if proteins["pork"] >= 3:
        boost.append("not_pork")
    previous_ids = {"normal": {dinner.get("id") for dinner in normal_dinners}}
    return {"summary": "前週バランスを内部分析済み。", "boost": boost, "previous_ids": previous_ids}


def choose_menus(mode: str, start: dt.date, analysis: dict) -> list[dict]:
    candidates = MENUS[mode][:]
    shift = ((start.toordinal() // 7) + {"normal": 0, "tired": 3, "limit": 5}[mode]) % len(candidates)
    candidates = candidates[shift:] + candidates[:shift]
    previous_ids = analysis["previous_ids"].get(mode, set())
    fresh_candidates = [item for item in candidates if item["id"] not in previous_ids]
    if len(fresh_candidates) >= 5:
        candidates = fresh_candidates
    scored = []
    for order, item in enumerate(candidates):
        score = sum(5 for tag in item["tags"] if tag in analysis["boost"])
        if "not_pork" in analysis["boost"] and item["protein"] == "pork":
            score -= 4
        if item["id"] in previous_ids:
            score -= 100
        scored.append((score, -order, item))
    return [item for _, _, item in sorted(scored, key=lambda row: (row[0], row[1]), reverse=True)[:5]]


def build_shopping(dinners: list[dict]) -> dict:
    result = {"月曜": {group: [] for group in GROUPS}, "水曜": {group: [] for group in GROUPS}}
    for index, dinner in enumerate(dinners):
        buy_day = "月曜" if index <= 2 else "水曜"
        for group, items in dinner["shopping"].items():
            for name, amount, use in items:
                use_label = f"{DAY_NAMES[index]}夕・{dinner['main']}: {use}"
                existing = next((row for row in result[buy_day][group] if row[0] == name), None)
                if existing:
                    if amount not in existing[1].split(" + "):
                        existing[1] += f" + {amount}"
                    existing[2] += f" / {use_label}"
                else:
                    result[buy_day][group].append([name, amount, use_label])
    return result


def build_mode(mode: str, start: dt.date, analysis: dict) -> dict:
    menus = choose_menus(mode, start, analysis)
    dinners = []
    for index, item in enumerate(menus):
        date = start + dt.timedelta(days=index)
        dinner = {key: value for key, value in item.items() if key != "shopping"}
        dinner.update({"day": DAY_NAMES[index], "date": f"{date.month}/{date.day}"})
        dinners.append(dinner)
    return {"dinners": dinners, "shopping": build_shopping(menus)}


def build_plan(today: dt.date) -> dict:
    previous = json.loads(PLAN_JSON.read_text(encoding="utf-8")) if PLAN_JSON.exists() else None
    analysis = analyze_previous(previous)
    start = plan_monday(today)
    return {
        "generatedAt": today.isoformat(),
        "weekStart": start.isoformat(),
        "weekEnd": (start + dt.timedelta(days=4)).isoformat(),
        "analysis": analysis["summary"],
        **build_mode("normal", start, analysis),
    }


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    plan = build_plan(dt.date.today())
    PLAN_JSON.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    DATA_JS.write_text("window.MEAL_PLAN_DATA = " + json.dumps(plan, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
    print(f"Generated {PLAN_JSON}")
    print(f"Generated {DATA_JS}")


if __name__ == "__main__":
    main()
