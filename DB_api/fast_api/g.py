import pandas as pd

df = pd.read_csv("target_balanced_20.csv")

type_map = {
    'float64': 'Float',
    'int64': 'Integer',
    'object': 'String'
}

model_name = "LoanAccount"
table_name = "loan_accounts"

with open("models.py", "w") as f:
    f.write("from sqlalchemy.ext.declarative import declarative_base\n")
    f.write("from sqlalchemy import Column, Integer, String, Float\n\n")
    f.write("Base = declarative_base()\n\n")
    f.write(f"class {model_name}(Base):\n")
    f.write(f"    __tablename__ = \"{table_name}\"\n\n")

    for col in df.columns:
        col_type = type_map[str(df[col].dtype)]
        if col == "UNIQUE_ID":
            f.write(f"    {col} = Column({col_type}, primary_key=True, index=True)\n")
        else:
            f.write(f"    {col} = Column({col_type})\n")
