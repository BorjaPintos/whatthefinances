import json
from typing import Dict


class LoadConfiguration:

    @staticmethod
    def load_from_file_json(json_configuration_path: str) -> Dict:
        with open(json_configuration_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def load_from_json(json_configuration: str) -> Dict:
        return json.loads(json_configuration)
