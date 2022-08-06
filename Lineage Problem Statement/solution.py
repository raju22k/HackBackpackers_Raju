import re

sql_script = """
37 LOCKING ROW FOR ACCESS
38 SELECT
39 T.SWB_CNTRY_ID,
40 T.CNTRY_TYPE_CD,
41 T.DW_EFF_DT,
42 S.DW_AS_OF_DT
43 FROM
44 (SELECT
45 SWB_CNTRY_ID,
46 CNTRY_TYPE_CD,
47 RCV_IN,
48 DW_EFF_OT,
49 MAX(DW_EFF_DT) MAX_EFF_DT
50 FROM IDW_DATA.CNTRY_MULTI_DEF_CD_T
51 WHERE
52 CURR_IN=1 GROUP BY 1,2,3,4) T,
53 (SELECT
54 SWB_CNTRY_ID,
55 CNTRY_SCHEME_CD,
56 DW_AS_OF_OT,
57 DW_ACTN_IND
58 FROM IDW_STAGE.CNTRY_MULTI_DEF_CD_S) S
59 WHERE
60 S.SWB_CNTRY_ID = T.SWB_CNTRY_ID AND S.CNTRY_SCHEME_CD = T.CNTRY_TYPE_CD
61 AND (S.DW_ACTN_IND='U' OR (S.DW_ACTN_IND='I' AND T.RCV_IN=0))
62 AND S.DW_AS_OF_DT > T.MAX_EFF_DT
"""

# get output columns from the select statment
output_cols = re.search(r'(?s)select(.*?)from', sql_script, flags=re.I).group(1).replace('\n',',').replace(' ',',')
cols = [item for item in output_cols.split(',') if item != '' and not item.isnumeric()]
# print(cols)

# get all sub queries
sub_qrys = re.findall(r'(?s)\(select.*?from.*?\)\s+\w', sql_script, flags=re.I)

# get all tables from sub queries
tbls = {}
for sub_qry in sub_qrys:
    tbl_name = re.search('from\s+(\w+)', sub_qry, re.I).group(1)
    tbl_var = sub_qry.split(' ')[-1]
    tbls[tbl_var] = tbl_name

# map cols to tables
print("column=>table")
for col in cols:
    print(col.split('.')[1] + "=>" + tbls[col.split('.')[0]])
