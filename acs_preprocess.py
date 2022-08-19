# Script to pre-process (i.e., filter and merge) state .gdb files
# Each data file has survey data from ACS.

# Column details can be found at https://www2.census.gov/geo/docs/maps-data/data/tiger/prejoined/ACSMetadata2010.txt

# COLUMN DETAILS
'''
Short Name|Full Name
STATEFP10|State FIPS Code
COUNTYFP10|County FIPS Code
TRACTCE10|Census Tract Code
BLKGRPCE10|Block Group Code
GEOID10|Geographic Identifier
NAMELSAD10|Full Name
MTFCC10|MAF/TIGER Feature Classification Code (G5030 = Block Group)
FUNCSTAT|Functional Status (S = Statistical)
ALAND10|Land Area (square meters)
B19001e1|HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2011 INFLATION-ADJUSTED DOLLARS) - Universe:  Households - Total: -- (Estimate)
B19001e2|HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2011 INFLATION-ADJUSTED DOLLARS) - Universe:  Households - Total:  Less than $10,000 -- (Estimate)
B19001e3|HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2011 INFLATION-ADJUSTED DOLLARS) - Universe:  Households - Total:  $10,000 to $14,999 -- (Estimate)
B19001e4|HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2011 INFLATION-ADJUSTED DOLLARS) - Universe:  Households - Total:  $15,000 to $19,999 -- (Estimate)
B19001e5|HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2011 INFLATION-ADJUSTED DOLLARS) - Universe:  Households - Total:  $20,000 to $24,999 -- (Estimate)
B19001e6|HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2011 INFLATION-ADJUSTED DOLLARS) - Universe:  Households - Total:  $25,000 to $29,999 -- (Estimate)
B19001e7|HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2011 INFLATION-ADJUSTED DOLLARS) - Universe:  Households - Total:  $30,000 to $34,999 -- (Estimate)
B19001e8|HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2011 INFLATION-ADJUSTED DOLLARS) - Universe:  Households - Total:  $35,000 to $39,999 -- (Estimate)
B19001e9|HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2011 INFLATION-ADJUSTED DOLLARS) - Universe:  Households - Total:  $40,000 to $44,999 -- (Estimate)
B19001e10|HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2011 INFLATION-ADJUSTED DOLLARS) - Universe:  Households - Total:  $45,000 to $49,999 -- (Estimate)
B19001e11|HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2011 INFLATION-ADJUSTED DOLLARS) - Universe:  Households - Total:  $50,000 to $59,999 -- (Estimate)
B19001e12|HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2011 INFLATION-ADJUSTED DOLLARS) - Universe:  Households - Total:  $60,000 to $74,999 -- (Estimate)
B19001e13|HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2011 INFLATION-ADJUSTED DOLLARS) - Universe:  Households - Total:  $75,000 to $99,999 -- (Estimate)
B19001e14|HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2011 INFLATION-ADJUSTED DOLLARS) - Universe:  Households - Total:  $100,000 to $124,999 -- (Estimate)
B19001e15|HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2011 INFLATION-ADJUSTED DOLLARS) - Universe:  Households - Total:  $125,000 to $149,999 -- (Estimate)
B19001e16|HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2011 INFLATION-ADJUSTED DOLLARS) - Universe:  Households - Total:  $150,000 to $199,999 -- (Estimate)
B19001e17|HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2011 INFLATION-ADJUSTED DOLLARS) - Universe:  Households - Total:  $200,000 or more -- (Estimate)
'''
import fiona
import geopandas as gpd
import os

path = "/Users/jayantgupta/Desktop/ACS_Data"
out_file = "ACS_Merged.shp"

merged_df = None
def filter_and_merge(path, out_file):
  for filename in os.listdir(path):
    if filename.endswith(".gdb") is not True:
      continue
    print("Processing {0}".format(filename))
    data = gpd.read_file(os.path.join(path, filename), layer = 0)
    print("Just read {0} rows".format(len(data)))
    filtered_data = data.filter(items = ['STATEFP10', 'COUNTYFP10', 'TRACTCE10', 'BLKGRPCE10', 'GEOID10', 'NAMELSAD10', 'MTFCC10', 'ALAND10', 'B19001e1', 'B19001e2', 'B19001e3', 'B19001e4', 'B19001e5', 'B19001e6', 'B19001e7', 'B19001e8', 'B19001e9', 'B19001e10', 'B19001e11', 'B19001e12', 'B19001e13', 'B19001e14', 'B19001e15', 'B19001e16', 'B19001e17', 'geometry'])
    print("Finished filtering the data...")
    if merged_df is None:
      merged_df = filtered_data
    else:
      merged_df = merged_df.append(filtered_data)
    print("Merged data has {0} rows".format(len(merged_df)))
  merged_df.to_file(os.path.join(path, out_file))

# filter_and_merge(path, out_file)

#merged_df = gpd.read_file(os.path.join(path, out_file))
#metro_shp_location = "/Users/jayantgupta/Desktop/ACS_Data/gz_2010_us_310_m1_500k/gz_2010_us_310_m1_500k.shp"
#metro_shp = gpd.read_file(metro_shp_location)

#merged_data_with_metro = gpd.sjoin(merged_data, metro_shp, how='left', op='intersects')
#print(len(merged_data_with_metro))

# merged_data_with_metro.to_file(os.path.join(path, "ACS_Merged_with_metro.shp"))
def filter_and_calculate(path, in_file):
  data = gpd.read_file(os.path.join(path, in_file))
  metro_data = data[data['Join_Count'] == 1]
  metro_data['P'] = metro_data['B19001e2'] + metro_data['B19001e3']
  metro_data['NP'] = metro_data['B19001e1'] - metro_data['P']
  metro_data['W'] = metro_data['B19001e17']
  metro_data['NW'] = metro_data['B19001e1'] - metro_data['W']
  drop_col = ['Join_Count', 'TARGET_FID', 'ALAND10', 'B19001e1',
       'B19001e2', 'B19001e3', 'B19001e4', 'B19001e5', 'B19001e6', 'B19001e7',
       'B19001e8', 'B19001e9', 'B19001e10', 'B19001e11', 'B19001e12',
       'B19001e13', 'B19001e14', 'B19001e15', 'B19001e16', 'B19001e17', 
	'geometry', 'NAMELSAD10', 'MTFCC10', 'BLKGRPCE10', 'CENSUSAREA', 
	'CBSA']
  metro_data = metro_data.drop(columns = drop_col)
  return metro_data

path = "/Users/jayantgupta/Desktop/ACS_Data/shpfiles"
in_file = "ACS_Joined.shp"
metro_data = filter_and_calculate(path, in_file)
print(len(metro_data))
print(metro_data.head())
metro_data.to_csv("/Users/jayantgupta/Desktop/ACS_Data/Metro_data.csv")
