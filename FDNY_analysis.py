#!/usr/bin/env python
# coding: utf-8

# # FDNY analysis challenge 
# The New York City Fire Department keeps a log of detailed information on incidents handled by FDNY units. In this challenge I worked on a dataset that contains a record of incidents handled by FDNY units from 2013-2019.
# 
# This challenge was very difficult.... but I learned so much during the process. I expanded my knowledge and skills more than ever. 

# In[15]:


# Import relevant library 
import pandas as pd
# Importing the data into jupyter notebook 
fdny = pd.read_csv("data/Incidents_Responded_to_by_Fire_Companies.csv", low_memory=False)


# **What proportion of FDNY responses in this dataset correspond to the most common type of incident?**

# In[17]:


# Calculating the proportion of most common type of incident
fdny['INCIDENT_TYPE_DESC'].value_counts(normalize=True) * 100


# **How many times more likely is an incident in Staten Island a false call compared to in Manhattan? The answer should be the ratio of Staten Island false call rate to Manhattan false call rate. A false call is an incident for which 'INCIDENT_TYPE_DESC' is '710 - Malicious, mischievous false call, other'.**

# In[18]:


#Checking the borough (town) of incidents
fdny.BOROUGH_DESC.value_counts()


# In[59]:


# Subsetting fdny data frame to extract columns with false call + from Staten Island
false_call_staten = fdny[(fdny["INCIDENT_TYPE_DESC"]=="710 - Malicious, mischievous false call, other") & (fdny["BOROUGH_DESC"]=="3 - Staten Island")]
#Calculating number of rows with criteria == false call + Staten
stat_total_rows = len(false_call_staten)
stat_total_rows


# In[64]:


# Subsetting fdny data frame to extract columns with false call + from Manhattan
false_call_manhattan = fdny[(fdny["INCIDENT_TYPE_DESC"]=="710 - Malicious, mischievous false call, other") & (fdny["BOROUGH_DESC"]=="1 - Manhattan")]
#Calculating number of rows with criteria == false call + Manhattan
manh_total_rows = len(false_call_manhattan)
manh_total_rows


# In[61]:


#To calculate ratios you need to divide both sides by the greatest common divisor.
# Creating a function for gcd:
def gcd(a, b):
    """Calculate the Greatest Common Divisor of a and b.

    Unless b==0, the result will have the same sign as b (so that when
    b is divided by it, the result comes out positive).
    """
    while b:
        a, b = b, a%b
    return a


# In[66]:


# calculating gcd for total number of times false calls are reported in Staten and Manhattan
gcd(stat_total_rows,manh_total_rows)
# We will try and round off the false call for manhattan and staten to the nearest one thousand 


# In[67]:


# rounding off to nearest 1000
manh_total_rows = round(manh_total_rows, ndigits=-3)
stat_total_rows = round(stat_total_rows, ndigits=-3)


# In[68]:


# Find greatest commond divisor so as to calculate ratio
gcd = gcd(manh_total_rows, stat_total_rows)


# In[69]:


gcd


# In[70]:


# Divide both sides by GCD if it is not equal to 1, if it is equal to one leave it as it is
if gcd == 1:
    print("Ratio of Staten Island false call rate to Manhattan false call rate is", stat_total_rows,":", manh_total_rows)
else: 
    manh_total_rows = manh_total_rows/gcd
    stat_total_rows = stat_total_rows /gcd
    print("Ratio of Staten Island false call rate to Manhattan false call rate is", stat_total_rows,":", manh_total_rows)


# In[71]:


# representing ratio as float value
stat_total_rows/manh_total_rows


# **What is the ratio of the average number of units that arrive to a scene of an incident classified as '111 - Building fire' to the number that arrive for '651 - Smoke scare, odor of smoke'?**

# In[30]:


# Subsetting fdny data frame to select incidents reported as "111 - Building fire" and the the total units that arrived at scene each time
building_fire = fdny.loc[fdny.INCIDENT_TYPE_DESC == "111 - Building fire", ["UNITS_ONSCENE","INCIDENT_TYPE_DESC"]]
building_fire


# In[31]:


# Calculating the average number of units that arrive at a scene classified as '111 - Building fire'
building_fire.UNITS_ONSCENE.mean()


# In[43]:


# Saving mean of average units on scene classified as building fire to a variable 
building_fire_mean = round(building_fire.UNITS_ONSCENE.mean())


# In[33]:


# Subsetting fdny data frame to select incidents reported as "651 - Smoke scare, odor of 
#smoke" and the total units that arrived at scene each time
smoke_scare = fdny.loc[fdny.INCIDENT_TYPE_DESC == "651 - Smoke scare, odor of smoke", ["UNITS_ONSCENE","INCIDENT_TYPE_DESC"]]
smoke_scare


# In[34]:


smoke_scare.UNITS_ONSCENE.mean()


# In[45]:


# Saving mean of average units on scene classified as smoke scare to a variable 
smoke_scare_mean = round(smoke_scare.UNITS_ONSCENE.mean())


# In[52]:


gcd = gcd(building_fire_mean,smoke_scare_mean)


# In[53]:


# Checkpoint for gcd
# Divide both sides by GCD if it is not equal to 1, if it is equal to one leave it as it is
if gcd == 1:
    print("Ratio of average units on scene classified as Building fire to Smoke scare is", building_fire_mean,":", smoke_scare_mean)
else: 
    building_fire_mean = building_fire_mean/gcd
    smoke_scare_mean = smoke_scare_mean /gcd
    print("Ratio of average units on scene classified as Building fire to Smoke scare is", building_fire_mean,":", smoke_scare_mean)


# In[56]:


# representing ratio as a float value
building_fire_mean/smoke_scare_mean


# **Check the distribution of the number of minutes it takes between the time a '111 - Building fire' incident has been logged into the Computer Aided Dispatch system and the time at which the first unit arrives on scene. What is the third quartile of that distribution. Note: the number of minutes can be fractional (ie, do not round).**

# In[115]:


# Converting to time data
fdny["ARRIVAL_DATE_TIME"] = pd.to_datetime(fdny["ARRIVAL_DATE_TIME"])


# In[116]:


# Converting to time data
fdny["INCIDENT_DATE_TIME"] = pd.to_datetime(fdny["INCIDENT_DATE_TIME"])


# In[121]:


# subsetting data frame to extract columns with incident as building and also extracting arrival time and incident time
time_stamp = fdny.loc[fdny.INCIDENT_TYPE_DESC == "111 - Building fire", ["ARRIVAL_DATE_TIME","INCIDENT_TYPE_DESC","INCIDENT_DATE_TIME"]]


# In[136]:


# Checking dataframe
time_stamp.head()


# In[128]:


# Calculating duration (difference in time between arrival time of units and incident time as per computer aided system)
# Creating a new column for it called duration
time_stamp["Duration"]= time_stamp.ARRIVAL_DATE_TIME - time_stamp.INCIDENT_DATE_TIME


# In[135]:


# Calculating the 3rd quantile of distribution of duration 
time_stamp.Duration.quantile(q=[0.75])


# **What is the coefficient of determination (R squared) between the number of residents at each ZIP code and the number of inicidents whose type is classified as '111 - Building fire' at each of those zip codes. Note: the population for each ZIP code in New York state can be found here. Ignore ZIP codes that do not appear on the website.**

# In[803]:


# Getting Zip code data for New York state.
# Copy pasted data from url: "https://www.newyork-demographics.com/zip_codes_by_population" into csv file
# importing csv file with zip code information in New York state
zip_code_ny = pd.read_csv("data/new_york_zip_codes.csv", low_memory=False)


# In[878]:


# Renaming colum zip code for easier downstream analysis
zip_code_ny_clean = zip_code_ny.rename(columns={'Zip Code': 'ZIP_CODE'})
zip_code_ny_clean


# In[805]:


# subsetting data frame to extract columns with incident as building fire plus zip code
fdny_zip_code = fdny.loc[fdny.INCIDENT_TYPE_DESC == "111 - Building fire", ["INCIDENT_TYPE_DESC","ZIP_CODE"]]


# In[806]:


# Check subsetted dataframe
fdny_zip_code


# In[886]:


# Checking zip code from fdny_zip_code and zip_code_ny_clean 
# Then merging the two data sets only if the columns have similar zip codes. option Inner looks at codes that are similar and combines
merged_zip_data = pd.merge(fdny_zip_code, zip_code_ny_clean, on=['ZIP_CODE'], how='inner')


# In[808]:


# Checking data
merged_zip_data.head()


# In[809]:


# Checking brief statisitics of dataframe
merged_zip_data.describe()


# In[903]:


# Check summary statistic information of dataframe (checks null data and data types)
merged_zip_data.info()


# In[956]:


# In order to calculate co-efficient of determination using sklearn I have to have two values:
# y true - which is considered as the ground truth (correct values)
# y pred which is considered as the estimated target value.
# In this case I considered the population values as per criteria mentioned in the question
# Counting Population values as per criteria
value_counts_pop = merged_zip_data['Population'].value_counts()
# converting to dataframe and assigning new names to the columns
df_value_counts = pd.DataFrame(value_counts_pop)
df_value_counts = df_value_counts.reset_index() # resetting index
df_value_counts.columns = ['unique_values', 'Population_count'] # change column names
# convert to numpy array for easy downstream analysis
arr_1 = df_value_counts.unique_values.to_numpy()
# Checking shape of numpy array
print(arr_1.shape)# This will be our y true (ground truth)


# In[957]:


# Calculating y pred 
# Y pred in this case is the the number of inicidents whose type is classified 
#as '111 - Building fire' at each zip code (appearing in NY zip code webpage)
# Counting the zip codes as per criteria in the question
value_counts_zip = merged_zip_data['ZIP_CODE'].value_counts()
# converting to df and assigning new names to the columns
df_value_counts = pd.DataFrame(value_counts_zip)
df_value_counts = df_value_counts.reset_index() #resetting index
df_value_counts.columns = ['unique_values', 'ZIP_CODE_count'] # change column names
# Convert to numpy array for easy downstream analysis
arr_2 = df_value_counts.ZIP_CODE_count.to_numpy()
# Checking the shape of numpy array
print(arr_2.shape) # this will our y_pred (estimated target value)


# In[963]:


# Importing relevant library
from sklearn.metrics import r2_score
### Assume a is our y_true and b is our y_pred
a = arr_1
b = arr_2
# Calculate r2 (co-efficient of determination)
r2 = r2_score(a, b)
print("The co-efficient of determination is", r2)


# **Calculate the chi-square test statistic for testing whether an incident is more likely to last longer than 60 minutes when CO detector is not present. Again only consider incidents that have information about whether a CO detector was present or not.**

# In[744]:


# Subsetting data frame to pick "CO_DETECTOR_PRESENT_DESC" and "TOTAL_INCIDENT_DURATION". 
# dropped null values in both columns
fdny_CO_detector = fdny[["CO_DETECTOR_PRESENT_DESC", "TOTAL_INCIDENT_DURATION"]].dropna()


# In[747]:


# Checking no NA values in data 
fdny_CO_detector.value_counts()


# In[748]:


fdny_CO_detector.head()


# In[750]:


# Dividing the INCIDENT_DURATION_TIME by 60 to convert into minutes then created a new column for minutes
fdny_CO_detector["INCIDENT_DURATION_min"] = fdny_CO_detector["TOTAL_INCIDENT_DURATION"]/60


# In[755]:


# Subsetting data frame to extract only data with above 60 minutes TOTAL INCIDENT DURATION 
#(CO detector is present and absent in this dataframe)
df_above_60 = fdny_CO_detector[(fdny_CO_detector["INCIDENT_DURATION_min"] > 60)]


# In[ ]:


# Importing relevant libraries for calculating chi-square statisitics
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[761]:


# creating cross tab 
contigency= pd.crosstab(fdny_CO_detector_60["CO_DETECTOR_PRESENT_DESC"],fdny_CO_detector_60["INCIDENT_DURATION_min"])
contigency


# In[762]:


# Showing contigenecy percentage statistics
contigency_pct= pd.crosstab(fdny_CO_detector_60["CO_DETECTOR_PRESENT_DESC"],fdny_CO_detector_60["INCIDENT_DURATION_min"],
                           normalize = "index")
contigency_pct


# In[740]:


# Plotting contigency table on a heatmap 
plt.figure(figsize=(12,8)) 
sns.heatmap(contigency, annot=True, cmap="YlGnBu")
plt.title("Contigency heatmap indicating CO present or not");


# In[765]:


# Chi-square test of independence. 
c, p, dof, expected = chi2_contingency(contigency) 
# Print the p-value, chi-square statistic and dof
print("The p-value is ", p)
print("The chi-square test statistic is ", c)
print("The degree of freedom is", dof)

