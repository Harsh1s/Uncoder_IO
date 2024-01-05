"""
Uncoder IO Community Edition License
-----------------------------------------------------------------
Copyright (c) 2023 SOC Prime, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-----------------------------------------------------------------
"""

import re
from typing import Union

from app.translator.const import DEFAULT_VALUE_TYPE
from app.translator.platforms.chronicle.renders.chronicle import ChronicleFieldValue, ChronicleQueryRender
from app.translator.platforms.chronicle.const import DEFAULT_CHRONICLE_SECURITY_RULE, chronicle_rule_details
from app.translator.core.mapping import SourceMapping
from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.parser_output import MetaInfoContainer
from app.translator.tools.utils import concatenate_str, get_author_str

_AUTOGENERATED_TITLE = "Autogenerated Chronicle Security rule"
_AUTOGENERATED_DESCRIPTION = "Autogenerated Chronicle Security rule."


class ChronicleRuleFieldValue(ChronicleFieldValue):
    details: PlatformDetails = chronicle_rule_details

    def equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.equal_modifier(field=field, value=v) for v in value)})"
        return f'{self.apply_field(field)} = "{self.apply_value(value)}"'

    def less_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{self.apply_field(field)} < "{self.apply_value(value)}"'

    def less_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{self.apply_field(field)} <= "{self.apply_value(value)}"'

    def greater_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{self.apply_field(field)} > "{self.apply_value(value)}"'

    def greater_or_equal_modifier(self, field: str, value: Union[int, str]) -> str:
        return f'{self.apply_field(field)} >= "{self.apply_value(value)}"'

    def not_equal_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join([self.not_equal_modifier(field=field, value=v) for v in value])})"
        return f'{self.apply_field(field)} != "{self.apply_value(value)}"'

    def contains_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field=field, value=v) for v in value)})"
        return f're.regex({self.apply_field(field)}, `.*{self.apply_value(value)}.*`)'

    def endswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field=field, value=v) for v in value)})"
        return f're.regex({self.apply_field(field)}, `.*{self.apply_value(value)}`)'

    def startswith_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field=field, value=v) for v in value)})"
        return f're.regex({self.apply_field(field)}, `{self.apply_value(value)}.*`)'

    @staticmethod
    def apply_field(field):
        return f"$e.{field}"

    def regex_modifier(self, field: str, value: DEFAULT_VALUE_TYPE) -> str:
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        return f're.regex({self.apply_field(field)}, `{self.apply_asterics_value(value)}`)'


class ChronicleSecurityRuleRender(ChronicleQueryRender):
    details: PlatformDetails = chronicle_rule_details
    or_token = "or"
    field_value_map = ChronicleRuleFieldValue(or_token=or_token)

    @staticmethod
    def prepare_title(title: str) -> str:
        if not title:
            return title
        new_title = re.sub(re.compile('[()*‘’:;+!,\\[\\].?`"-/]'), "", title.lower())
        new_title = re.sub(re.compile("\\s"), "_", new_title.lower())
        index = 0
        for i, title_char in enumerate(new_title):
            if not title_char.isdigit():
                index = i
                break
        new_title = new_title[index:]
        new_title = new_title.strip("_")
        return new_title

    def finalize_query(self, prefix: str, query: str, functions: str, meta_info: MetaInfoContainer = None,
                       source_mapping: SourceMapping = None, not_supported_functions: list = None) -> str:
        query = super().finalize_query(prefix=prefix, query=query, functions=functions)
        rule = DEFAULT_CHRONICLE_SECURITY_RULE.replace("<query_placeholder>", query)
        rule = rule.replace("<title_place_holder>", self.prepare_title(meta_info.title) or _AUTOGENERATED_TITLE)
        description = meta_info.description or _AUTOGENERATED_DESCRIPTION
        description = concatenate_str(description, get_author_str(meta_info.author))
        rule = rule.replace("<description_place_holder>", description)
        rule = rule.replace("<licence_place_holder>", meta_info.license)
        rule = rule.replace("<rule_id_place_holder>", meta_info.id)
        rule = rule.replace("<severity_place_holder>", meta_info.severity)
        rule = rule.replace("<status_place_holder>", meta_info.status)
        rule = rule.replace("<falsepositives_place_holder>", ', '.join(meta_info.false_positives))
        rule = rule.replace("<tags_place_holder>", ", ".join(meta_info.tags))
        rule = rule.replace("<created_place_holder>", str(meta_info.date))
        return rule
