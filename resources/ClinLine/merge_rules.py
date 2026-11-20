import json
import os
import pickle
from pathlib import Path

# maybe? I wanna specifically not save or have those files anywhere on the server
# Server is also a maybe?
# TODO: make a software design document before ANYTHING
# TEMPORARY SO THAT MERGING WORKS
# TODO: REMOVE TEMPORARY CODE \/
# TODO: REMOVE TEMP FUNCTIONS


def load_pkl(file_path):
    with open(file_path, "rb") as f:
        data = pickle.load(f)
    return data


def load_json(file_path):
    with open(file_path, "rb") as f:
        data = json.load(f)
    return data


def translate_rules(origin_rules: dict, new_rules: dict):
    for rule_id, rule in new_rules.items():
        if not origin_rules.get(rule_id, None):
            origin_rules[rule_id] = rule

    with open("rules.pkl", "wb") as f:
        pickle.dump(origin_rules, f)


def translate_rules_dictionary(origin_dict: dict, new_dict: dict):
    for standard, rules in new_dict.items():
        base_standards_rules_dirty = origin_dict.get(standard, None)

        if base_standards_rules_dirty is None:
            origin_dict[standard] = rules
            continue

        base_standards_rules: set[str] = set(base_standards_rules_dirty)

        for rule in rules:
            base_standards_rules.add(rule)

        origin_dict[standard] = list(base_standards_rules)

    with open("rules_dictionary.pkl", "wb") as f:
        pickle.dump(origin_dict, f)


def pickle_validation_packages():
    validation_packages_directory = str(
        Path(__file__).parent.parent / "validation_packages"
    )

    for entry in os.scandir(validation_packages_directory):
        if entry.is_file():
            file_path = Path(entry.path)

            if file_path.suffix != ".json":
                continue

            with open(file_path, "r") as f:
                json_data = json.load(f)

            with open(
                validation_packages_directory + "/" + file_path.name + ".pkl", "wb"
            ) as f:
                pickle.dump(json_data, f)


def merge_packages(
    base_rules: str,
    base_dictionary: str,
    add_rules: str,
    add_dictionary: str,
):
    base_rules_pkl = load_pkl(base_rules)
    base_dictionary_pkl = load_pkl(base_dictionary)

    add_rules = load_json(add_rules)
    add_dictionary = load_json(add_dictionary)

    translate_rules(base_rules_pkl, add_rules)
    translate_rules_dictionary(base_dictionary_pkl, add_dictionary)


def main():
    base_rules = "../cache/rules.pkl"
    base_dictionary = "../cache/rules_dictionary.pkl"

    # clinline_rules = "ClinLine_extension_rules.json"
    # clinline_dictionary = "ClinLine_extension_rules_dictionairy.json"

    M11_rules = "M11_extensions.json"
    M11_dictionary = "M11_extensions_rules.json"

    merge_packages(
        base_rules, base_dictionary, add_rules=M11_rules, add_dictionary=M11_dictionary
    )

    pickle_validation_packages()


main()
