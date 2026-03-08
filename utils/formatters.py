import pandas as pd

def format_inr(number):
    if pd.isna(number) or number is None: return "N/A"
    try:
        is_negative = number < 0
        number = abs(number)
        s, *d = str(round(float(number), 2)).partition(".")
        r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
        formatted_num = "".join([r] + d) if r else s
        return f"-{formatted_num}" if is_negative else formatted_num
    except: return str(number)

def format_large_number(number):
    if pd.isna(number) or number is None: return "N/A"
    try:
        num = float(number)
        if num >= 10000000: return f"{format_inr(round(num / 10000000, 2))} Cr"
        elif num >= 100000: return f"{format_inr(round(num / 100000, 2))} L"
        else: return format_inr(num)
    except: return str(number)

def format_df_to_crores(df):
    if df is None or df.empty: return df
    formatted = df.copy()
    for col in formatted.columns:
        formatted[col] = pd.to_numeric(formatted[col], errors='coerce')
        formatted[col] = formatted[col].apply(lambda x: f"{format_inr(round(x / 10000000, 2))}" if pd.notna(x) else "N/A")
    formatted.columns = [str(c).split(' ')[0] for c in formatted.columns]
    return formatted
