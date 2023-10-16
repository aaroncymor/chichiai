from chichiai import ChiChiAI
import pandas as pd


if __name__ == "__main__":
    # df = pd.read_csv('examples/Wellness_Data_All.csv')
    df = pd.read_csv('examples/titanic.csv')
    chichi = ChiChiAI(df)
    # chichi.pd_csv_agent_converse("What is the highest total steps?")
    chichi.pd_csv_agent_converse("Which gender has the highest survival rate?")
