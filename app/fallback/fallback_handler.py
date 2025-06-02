import json
import logging

FALLBACK_PATH = "app/fallback/fallback_data.json"


def get_fallback_data(aba, schema_obj):
    try:
        with open(FALLBACK_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        key_path = [aba]
        if hasattr(schema_obj, "sub_aba"):
            key_path.append(str(schema_obj.sub_aba))
        key_path.append(str(schema_obj.ano))
        for key in key_path:
            data = data[key]
        return {"data": data}
    except Exception as e:
        logging.error(f"Erro ao buscar fallback: {e}")
        return {"data": []}
