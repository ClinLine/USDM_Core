import json
import pickle

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


def main():
    base_rules_pkl = load_pkl("../cache/rules.pkl")
    base_dictionary_pkl = load_pkl("../cache/rules_dictionary.pkl")

    clinline_rules = load_json("ClinLine_extension_rules.json")
    clinline_dictionary = load_json("ClinLine_extension_rules_dictionairy.json")

    translate_rules(base_rules_pkl, clinline_rules)
    translate_rules_dictionary(base_dictionary_pkl, clinline_dictionary)


main()
