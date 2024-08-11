from .utils import clean_text, date_calculator
from .es_query import query_es

def retrieve_jds(rank_id_list):    
    query = {
        "query": {
            "ids": {
                "values": rank_id_list
            }
        }
    }
    
    es_jd_list = query_es(query)
    return es_jd_list