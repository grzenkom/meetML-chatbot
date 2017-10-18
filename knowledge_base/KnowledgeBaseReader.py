import pandas as pd
import os

KNOWLEDGE_BASE_PATH = os.path.dirname(__file__)
KNOWLEDGE_BASE_FILE = os.path.join(KNOWLEDGE_BASE_PATH, "main.csv")


def get_kb_extract():
    return pd.read_csv(KNOWLEDGE_BASE_FILE)

if __name__ == "__main__":
    # print(get_kb_extract())


    kb = get_kb_extract()
    ELEMENT = 'Carbon'
    PROPERTY = 'Density'

    print kb[kb["Element"] == ELEMENT][PROPERTY].tolist()[0]

