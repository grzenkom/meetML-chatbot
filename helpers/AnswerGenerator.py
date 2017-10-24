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
    "abundance": {"column_name": "Abundance_in_Earths_crust", "unit": "mg/kg"},
}

ANSWER_TEMPLATE = "The {0} of {1} is {2}{3}."
ABUNDANCE_ANSWER_TEMPLATE = "{1} is {4} ({2}{3})."
ABUNDANCE_THRESHOLD = 0.1


def abundance_value_mapping(action, value, element):
    if action == "ask_abundance":
        if float(value) >= ABUNDANCE_THRESHOLD:
            return "quite common", ABUNDANCE_ANSWER_TEMPLATE, element.title()
        else:
            return "rare", ABUNDANCE_ANSWER_TEMPLATE, element.title()
    return str(), ANSWER_TEMPLATE, element


def prepare_answer(intent_name, entities):
    element = entities.get("element").lower()
    property = entities.get("property")
    periodic_table_order = entities.get("periodic_table_order")

    if property:
        column_mapping_key = property
    elif periodic_table_order:
        column_mapping_key = periodic_table_order
    else:
        column_mapping_key = convert_action_to_key(intent_name)

    column_name = COLUMN_MAPPING.get(column_mapping_key).get("column_name")

    unit = COLUMN_MAPPING.get(column_mapping_key).get("unit")
    if unit:
        unit = " " + unit

    value = KnowledgeBaseReader.get_kb_value(element, column_name)
    abundance_value, answer_template, element_in_answer = abundance_value_mapping(intent_name, value, element)

    return answer_template.format(column_mapping_key, element_in_answer, value, unit, abundance_value)


def convert_action_to_key(action):
    return action.replace("ask_", "").replace("_", " ")

if __name__ == "__main__":
    TEST_CASES = [
        {"action": "ask_property", "parameters": {"element": "carbon", "property": "density"}},
        {"action": "ask_abundance", "parameters": {"element": "silver"}},
        {"action": "ask_periodic_table", "parameters": {"element": "iron", "periodic_table_order": "atomic number"}},
        {"action": "ask_origin_of_name", "parameters": {"element": "scandium"}},
    ]

    for tc in TEST_CASES:
        print(prepare_answer(tc["action"], tc["parameters"]))
