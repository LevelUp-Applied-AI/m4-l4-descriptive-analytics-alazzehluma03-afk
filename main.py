import pandas as pd
from tier3_analysis import run_tier3

# تحميل البيانات
df = pd.read_csv("data/student_performance.csv")

# effect size (Cohen's d)
effect_size = 0.7061 

run_tier3(df, effect_size)