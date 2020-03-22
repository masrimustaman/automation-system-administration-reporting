# %%
import os
import pandas as pd
import glob
import datetime

# getting list of files for vinfo and vnetwork 
path = os.getcwd()
vinfo_files = glob.glob(path + "/*vinfo.csv")

# %%
li_vinfo = []

for filename in vinfo_files:
    tempvinfo = pd.read_csv(filename, index_col=None, header=0, encoding = "ISO-8859-1", usecols= ['VM', 'Powerstate', 'DNS Name','OS according to the VMware Tools', 'OS according to the configuration file', 'VI SDK Server'])
    print("check point : individual vinfo shape " + str(tempvinfo.shape))
    li_vinfo.append(tempvinfo)

df_vinfo = pd.concat(li_vinfo, axis=0, ignore_index=True, sort=False)


# %%
df_vinfo = df_vinfo[df_vinfo['Powerstate'] == 'poweredOn']

# %%
df_guestnotcorrect = df_vinfo[df_vinfo['OS according to the configuration file'] != df_vinfo['OS according to the VMware Tools']]

# %%
# Create a Pandas Excel writer using XlsxWriter as the engine.
outputfile = datetime.datetime.now().strftime('%Y%m%d') + '-VM-GoestOSNotCorrect.xlsx'
writer = pd.ExcelWriter(outputfile, engine='xlsxwriter')

# Write each dataframe to a different worksheet.
df_guestnotcorrect.to_excel(writer, sheet_name='VM-GoestOSNotCorrect', index=False)

# Close the Pandas Excel writer and output the Excel file.
writer.save()

# %%
