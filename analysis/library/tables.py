from openpyxl import Workbook
from openpyxl import load_workbook

def df_to_excel(file, df, df_columns, start_col, start_row):
    wb = load_workbook(file)
    ws = wb.active

    col_n = start_col
    for col in df_columns:
        row_n = start_row
        for ob in df[col]:
            if ob < .01:
                ob = '<.01'
            ws.cell(row=row_n, column=col_n).value = ob
            row_n = row_n + 1
        col_n = col_n + 1
    wb.save(file)

def var_diff_to_excel(file, df, control_col, diff_col, se_col, pvalue_col, start_col, start_row):
    wb = load_workbook(file)
    ws = wb.active

    col_n = start_col
    row_n = start_row

    # control
    for ob in df[control_col]:
        ws.cell(row=row_n, column=col_n).value = ob
        row_n = row_n + 2

    col_n = start_col + 1


    # coefficient
    row_n = start_row
    for ob, p in zip(df[diff_col], df[pvalue_col]):
        if p >=.05:
            coef = str(ob)
        if p < .05:
            coef = str(ob) + '*'
        ws.cell(row=row_n, column=col_n).value = coef
        row_n = row_n + 2

    # se
    row_n = start_row + 1
    for ob in df[diff_col]:
        se = '(' + str(ob) + ')'
        ws.cell(row=row_n, column=col_n).value = se
        row_n = row_n + 2
    wb.save(file)
