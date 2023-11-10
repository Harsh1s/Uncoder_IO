from typing import List, Optional

from app.converter.core.mapping import BasePlatformMappings, LogSourceSignature, SourceMapping, DEFAULT_MAPPING_NAME


class LogScaleLogSourceSignature(LogSourceSignature):
    def __str__(self) -> str:
        return ""


class LogScaleMappings(BasePlatformMappings):
    def prepare_log_source_signature(self, mapping: dict) -> LogScaleLogSourceSignature:
        return

    def get_suitable_source_mappings(self, field_names: List[str]) -> List[SourceMapping]:
        suitable_source_mappings = []
        for source_mapping in self._source_mappings.values():
            if source_mapping.source_id == DEFAULT_MAPPING_NAME:
                continue

            if source_mapping.fields_mapping.is_suitable(field_names):
                suitable_source_mappings.append(source_mapping)

        if not suitable_source_mappings:
            suitable_source_mappings = [self._source_mappings[DEFAULT_MAPPING_NAME]]

        return suitable_source_mappings


logscale_mappings = LogScaleMappings(platform_dir="logscale")