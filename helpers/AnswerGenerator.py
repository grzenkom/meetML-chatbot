# -*- coding: utf-8 -*-
from knowledge_base import KnowledgeBaseReader

COLUMN_MAPPING = {
    "atomic weight": {"column_name": "Atomic_weight", "unit": "u"},
    "density": {"column_name": "Density", "unit": "g/cm³"},
    "melting point": {"column_name": "Melting_point", "unit": "K"},
    "boiling point": {"column_name": "Boiling_point", "unit": "K"},
    "specific heat capacity": {"column_name": "Specific_heat_capacity", "unit": "J/g · K"},
    "electronegativity": {"column_name": "Electronegativity", "unit": ""},
    "atomic number": {"column_name": "Atomic_number", "unit": ""},
    "period": {"column_name": "Period", "unit": ""},
    "group": {"column_name": "Group", "unit": ""},
    "origin of name": {"column_name": "Origin_of_name", "unit": ""},
    "abundance": {"column_name": "Abundance_in_Earths_crust", "unit": ""},
}

ANSWER_TEMPLATE = "The {0} of {1} is {2}{3}."
ABUNDANCE_THRESHOLD = 0.01


def abundance_value_mapping(action, value):
    if action == "ask_abundance":
        if float(value) >= ABUNDANCE_THRESHOLD:
            return "quite common"
        else:
            return "rare"
    return value


def prepare_answer(action, parameters):
    element = parameters.get("element").lower()
    property = parameters.get("property")
    periodic_table_order = parameters.get("periodic_table_order")

    if property:
        column_mapping_key = property
    elif periodic_table_order:
        column_mapping_key = periodic_table_order
    else:
        column_mapping_key = convert_action_to_key(action)

    column_name = COLUMN_MAPPING.get(column_mapping_key).get("column_name")
    unit = COLUMN_MAPPING.get(column_mapping_key).get("unit")
    if unit:
        unit = " " + unit
    value = KnowledgeBaseReader.get_kb_value(element, column_name)
    value = abundance_value_mapping(action, value)

    return ANSWER_TEMPLATE.format(column_mapping_key, element, value, unit)


def convert_action_to_key(action):
    return action.replace("ask_", "").replace("_", " ")

if __name__ == "__main__":
    TEST_CASES = [
        {"action": "ask_property", "parameters": {"element": "carbon", "property": "density"}},
        {"action": "ask_abundance", "parameters": {"element": "lithium"}},
        {"action": "ask_periodic_table", "parameters": {"element": "iron", "periodic_table_order": "atomic number"}},
        {"action": "ask_origin_of_name", "parameters": {"element": "scandium"}},
    ]

    for tc in TEST_CASES:
        print(prepare_answer(tc["action"], tc["parameters"]))
