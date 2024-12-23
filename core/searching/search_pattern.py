def looking(search_phrase: str):
    body = search_phrase[:-1]

    query = {
      "bool": {
        "should": [
            {
               "regexp": {
                 "name": {
                   "value": f".*{body}.ми",
                   "boost": 3
                 }
               }
            },
            {
              "regexp": {
                "description": {
                "value": f".*{body}.ми"
                }
              }
            },
            {
              "multi_match": {
                "query": search_phrase,
                "type": "best_fields",
                "fields": ["name^3", "description"],
                "fuzziness": "auto",
                "prefix_length": 1,
                "operator": "or"
              }
            },
            {
              "multi_match": {
                "query": search_phrase,
                "type": "best_fields",
                "fields": ["name^3", "description"],
                "fuzziness": "auto",
                "prefix_length": 1,
                "operator": "and"
              }
            }
        ],
        "minimum_should_match": 1
      }
    }
    return query