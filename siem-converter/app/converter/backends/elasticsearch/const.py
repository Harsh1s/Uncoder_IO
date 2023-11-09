from app.converter.core.models.platform_details import PlatformDetails

PLATFORM_DETAILS = {
    "group_id": "elk stack",
    "group_name": "Elastic Stack",
    "alt_platform_name": "ECS",
}

ELASTICSEARCH_LUCENE_QUERY_DETAILS = {
    "siem_type": "elastic-lucene-query",
    "name": "Elasticsearch Query",
    "platform_name": "Query (Lucene)",
    **PLATFORM_DETAILS
}

ELASTICSEARCH_RULE_DETAILS = {
    "siem_type": "elastic-lucene-rule",
    "name": "Elastic Rule",
    "platform_name": "Detection Rule (Lucene)",
    "first_choice": 0,
    **PLATFORM_DETAILS
}

KIBANA_DETAILS = {
    "siem_type": "elastic-kibana-rule",
    "name": "Elastic Kibana Saved Search",
    "platform_name": "Kibana SavedSearch (JSON)",
    "first_choice": 0,
    **PLATFORM_DETAILS
}

ELASTALERT_DETAILS = {
    "siem_type": "elastalert-lucene-rule",
    "name": "ElastAlert",
    "platform_name": "Alert (Lucene)",
    "group_name": "ElastAlert",
    "group_id": "elastalert"
}

XPACK_WATCHER_DETAILS = {
    "siem_type": "elastic-watcher-rule",
    "name": "Elastic Watcher",
    "platform_name": "Rule (Watcher)",
    "first_choice": 0,
    **PLATFORM_DETAILS
}

elasticsearch_lucene_query_details = PlatformDetails(**ELASTICSEARCH_LUCENE_QUERY_DETAILS)
elasticsearch_rule_details = PlatformDetails(**ELASTICSEARCH_RULE_DETAILS)
elastalert_details = PlatformDetails(**ELASTALERT_DETAILS)
kibana_rule_details = PlatformDetails(**KIBANA_DETAILS)
xpack_watcher_details = PlatformDetails(**XPACK_WATCHER_DETAILS)

ELASTICSEARCH_DETECTION_RULE = {
    "description": "Autogenerated ElasticSearch Detection Rule.",
    "author": [],
    "enabled": True,
    "false_positives": [],
    "filters": [],
    "from": "now-360s",
    "immutable": False,
    "index": [],
    "interval": "5m",
    "rule_id": "",
    "language": "lucene",
    "output_index": ".siem-signals-default",
    "max_signals": 100,
    "risk_score": 65,
    "name": "",
    "query": "",
    "meta": {
        "from": "1m"
    },
    "severity": "high",
    "tags": [],
    "to": "now",
    "type": "query",
    "threat": [],
    "version": 1,
    "references": [],
    "license": ""
}

ELASTICSEARCH_ALERT = """alert:
- debug
description: <description_place_holder>
filter:
- query_string:
    query: <query_placeholder>
index: winlogbeat-*
name: <title_place_holder>
priority: <priority_place_holder>
realert:
  minutes: 0
type: any
"""

KIBANA_RULE = {
  "_id": "dcd74b95-3f36-4ed9-9598-0490951643aa-Malicious-PowerView-PowerShell-Commandlets",
  "_type": "search",
  "_source": {
    "title": "Autogenerated Kibana rule",
    "description": "Autogenerated Kibana rule.",
    "hits": 0,
    "columns": [],
    "sort": [
      "@timestamp",
      "desc"
    ],
    "version": 1,
    "kibanaSavedObjectMeta": {
      "searchSourceJSON": ""
    }
  }
}


KIBANA_SEARCH_SOURCE_JSON = {
    "index": "winlogbeat-*",
    "filter": [],
    "highlight": {
        "pre_tags": [
            "@kibana-highlighted-field@"
        ],
        "post_tags": [
            "@/kibana-highlighted-field@"
        ],
        "fields": {
            "*": {}
        },
        "require_field_match": False,
        "fragment_size": 2147483647
    },
    "query": {
        "query_string": {
            "query": "",
            "analyze_wildcard": True
        }
    }
}


XPACK_WATCHER_RULE = {
    "metadata": {
        "title": "",
        "description": "",
        "tags": [],
        "query": ""
    },
    "trigger": {
        "schedule": {
            "interval": "30m"
        }
    },
    "input": {
        "search": {
            "request": {
                "body": {
                    "size": 0,
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "query_string": {
                                        "query": "",
                                        "analyze_wildcard": True
                                    }
                                }
                            ],
                            "filter": {
                                "range": {
                                    "@timestamp": {
                                        "gte": "now-30m/m"
                                    }
                                }
                            }
                        }
                    }
                },
                "indices": []  # put indices from mapping
            }
        }
    },
    "condition": {
        "compare": {
            "ctx.payload.hits.total": {
                "not_eq": 0
            }
        }
    },
    "actions": {
        "send_email": {
            "throttle_period": "15m",
            "email": {
                "profile": "standard",
                "from": "root@localhost",
                "to": "root@localhost",
                "subject": "",
                "body": "Hits:\n{{#ctx.payload.hits.hits}}{{_source}}\n================================================================================\n{{/ctx.payload.hits.hits}}",
                "attachments": {
                    "data.json": {
                        "data": {
                            "format": "json"
                        }
                    }
                }
            }
        }
    }
}
