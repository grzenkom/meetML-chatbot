import pandas as pd
import os

KNOWLEDGE_BASE_PATH = os.path.dirname(__file__)
KNOWLEDGE_BASE_FILE = os.path.join(KNOWLEDGE_BASE_PATH, "periodic-table-extract.csv")


def get_kb_value(element, column_name):
    kb = pd.read_csv(KNOWLEDGE_BASE_FILE, dtype=object)
    return str(kb[kb["Element"].str.lower() == element.lower()][column_name].tolist()[0])

if __name__ == "__main__":
    print(get_kb_value("carbon", "Group"))
