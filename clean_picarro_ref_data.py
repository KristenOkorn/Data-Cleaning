#concatenate all of our data into 1 array
full_data = pd.concat(data_dict.values())

#Convert 'H2O' column to numeric
full_data['H2O'] = pd.to_numeric(full_data['H2O'], errors='coerce')
    
#remove any nans
full_data = full_data.dropna()

#apply the water vapor correction for co2
full_data['CO2'] = full_data['CO2'] / (1+(-0.012*full_data['H2O'])+(-0.000267*full_data['H2O']*full_data['H2O']))
#apply the water vapor correction for ch4
full_data['CH4'] = full_data['CH4'] / (1+(-0.009823*full_data['H2O'])+(-0.000239*full_data['H2O']*full_data['H2O']))
#delete the water column
full_data = full_data.drop(columns=['H2O'])
#apply the calibration correction for co2
full_data['CO2'] = (full_data['CO2']*0.9955) + 2.5842
#apply the calibration correction for ch4
full_data['CH4'] = (full_data['CH4']*-0.0808) + 1.0307

#resample (retime) the data to minutely
full_data['DATE_TIME'] = pd.to_datetime(full_data['DATE_TIME'])
#rename the datetime column
full_data.rename(columns={'DATE_TIME': 'datetime'}, inplace=True)
#make the datetime the index
full_data.index = full_data['datetime']
#drop the original datetime column
full_data.drop(['datetime'],axis=1,inplace=True)
#retime
full_data = full_data.resample("T").mean()

#remove empty rows from retime
full_data = full_data.dropna()

#Picarro runs 1 min and 2-3 sec slower - account for this
full_data.index = full_data.index + pd.Timedelta(minutes=1, seconds=2)

#get the final data in a convenient format
CO2 = pd.DataFrame(data={'CO2': full_data['CO2'].values}, index=full_data.index)
CH4 = pd.DataFrame(data={'CH4': full_data['CH4'].values}, index=full_data.index)

#save out the final data
savePath = os.path.join(path,'CO2_2024.csv')
CO2.to_csv(savePath)
savePath = os.path.join(path,'CH4_2024.csv')
CH4.to_csv(savePath)
