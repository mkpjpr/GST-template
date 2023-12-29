#!/usr/bin/env python
# coding: utf-8

# In[28]:


import pandas as pd
import numpy as np

def get_state_code(gst_number):
    try:
        return int(gst_number[0:2])
    except:
        return 0

#extract data
cust_master=pd.read_excel(r"C:\Users\yoges\Desktop\mukesh\Python\projects\excel tamplates and pivot table\CUSTOMER_MASTER.xlsx")
state_code_master=pd.read_excel(r"C:\Users\yoges\Desktop\mukesh\Python\projects\excel tamplates and pivot table\STATE_CODE_MASTERS.xlsx")
prod_master=pd.read_excel(r"C:\Users\yoges\Desktop\mukesh\Python\projects\excel tamplates and pivot table\PRODUCT_CODE_MASTER.xlsx")
main_sales_data=pd.read_excel(r"C:\Users\yoges\Desktop\mukesh\Python\projects\excel tamplates and pivot table\MAIN_SALES_DATA.xlsx",skiprows=2)
template=main_sales_data

#transform data
df=template.merge(right=prod_master,how="left",left_on="Product Code",right_on="Product Code")
df.drop("S.N",axis=1, inplace=True)
df["Sales Before Tax"]=df["Units Sold"]*df["PRICE"]
df["Taxable value"]=df["Sales Before Tax"]-df["Discount"]
df["State Code"]=df["GST Number"].apply(lambda x:get_state_code(x))
df1=df.merge(right=state_code_master,how="left",left_on="State Code",right_on="State Code")

df1.drop("State Code", axis=1, inplace=True)
df1["IGST"]=np.where(df1["Supplier State"]==df1["State Name"],0,df1["Taxable value"]*df1["GST RATE"])
df1["CGST"]=np.where(df1["Supplier State"]==df1["State Name"],df1["Taxable value"]*df1["GST RATE"]/2,0)
df1["SGST"]=np.where(df1["Supplier State"]==df1["State Name"],df1["Taxable value"]*df1["GST RATE"]/2,0)
df1["Total GST"]=df1["IGST"]+df1["CGST"]+df1["SGST"]

#NESTED IF>>>NP.SELECT

df1=df1.replace(np.nan,"")

conditions=[((df1["Doc Type"]=="Invoice")&(df1["GST Number"]!="")),
            ((df1["Doc Type"]=="Invoice")&(df1["GST Number"]=="")),
            (df1["Doc Type"]!="Invoice")]
results=["Table 4A- B2B","Table 5A- B2C","Table 9- CDNR"]
df1["Table GSTR1"]=np.select(conditions,results)

df2=df1.pivot_table(index=["Table GSTR1","GST RATE","HSN Code"],values=["IGST","CGST","SGST","Taxable value"],aggfunc="sum")
writer=pd.ExcelWriter("main output.xlsx",engine="openpyxl")
df1.to_excel(writer,sheet_name="Main Data")
df2.to_excel(writer,sheet_name="Pivot")
writer.close()


# In[ ]:




