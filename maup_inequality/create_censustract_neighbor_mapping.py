import pandas as pd

neighbors_table_location = "../../../ArcGIS/Projects/MyProject1/Census_Tracts_Neighbors_TableToExcel.csv"
tract_info_location = "../../../ArcGIS/Projects/MyProject1/Census_Tracts_TableToExcel.csv"
output_location = "../../../ArcGIS/Projects/MyProject1/Census_Tract_Neighbors.csv"

neighbors_table = pd.read_csv(filepath_or_buffer=neighbors_table_location)
tract_info = pd.read_csv(filepath_or_buffer=tract_info_location,
                            dtype={"FIPS": str})


tract_info['STATECODE'] = tract_info['FIPS'].str[:2]
tract_info['COUNTYCODE'] = tract_info['FIPS'].str[2:5]
tract_info['TRACTCODE'] = tract_info['FIPS'].str[5:]

#print(neighbors_table.head())
#print(tract_info.head())

combined = neighbors_table.merge(tract_info,
                                how="left",
                                left_on="UNIQUE_ID",
                                right_on="Unique_ID")

combined_shorter = combined[['UNIQUE_ID', 'FIPS', 'STATECODE', 'COUNTYCODE', 'TRACTCODE', 'COUNTY', 'STATE', 'NID', 'WEIGHT']]

combined_final = combined_shorter.merge(tract_info,
                                        how="left",
                                        left_on="NID",
                                        right_on="Unique_ID",
                                        suffixes=('', '_Neighbor'))

#print(combined_final.columns)
combined_final = combined_final[['FIPS', 'STATECODE', 'COUNTYCODE', 'TRACTCODE', 'COUNTY', 'STATE', 
                                'FIPS_Neighbor', 'STATECODE_Neighbor', 'COUNTYCODE_Neighbor', 'TRACTCODE_Neighbor', 'COUNTY_Neighbor', 'STATE_Neighbor',
                                'WEIGHT']]

combined_final.to_csv(path_or_buf=output_location)
#print(combined_final.head())