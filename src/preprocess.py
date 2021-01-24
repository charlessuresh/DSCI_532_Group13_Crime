from vega_datasets import data
import pandas as pd

crime_list = ['Homicide', 'Rape', 'Larceny', 'Violent']
sum_list = ['homs_sum', 'rape_sum', 'rob_sum', 'violent_crime']
rate_list = ['homs_per_100k', 'rape_per_100k', 'rob_per_100k', 'violent_per_100k']
sum_dict = {crime_list[i]: sum_list[i] for i in range(len(crime_list))} 
rate_dict = {crime_list[i]: rate_list[i] for i in range(len(crime_list))}
crime_dict = {'sum_dict': sum_dict, 'rate_dict': rate_dict}
pop = data.population_engineers_hurricanes()


def data_filtering_geochart(state, crime, metric, year_range, data_crime):
    if year_range is not None:
        data_crime = data_crime.loc[data_crime["year"].between(year_range[0], year_range[1])]
    crimes = [crime_dict[metric][x] for x in crime]
    results = (data_crime[['State'] + crimes]
                .melt(id_vars = "State", var_name = "crime", value_name = "crime_count")
                .groupby('State')
                .sum())
    results_df = pd.merge(results, pop, how = 'right', left_on = 'State', right_on = 'state')
    return results_df

def data_filtering_trendchart(state, crime, metric, year_range, data_crime):
    
    crimes = [crime_dict[metric][x] for x in crime]
    trend_data = data_crime[data_crime['State'].isin(state)]
    trend_data = trend_data[(trend_data['year']>=year_range[0]) & (trend_data['year']<=year_range[1])]
    trend_data = trend_data.groupby('year')[crimes].mean().reset_index()
    trend_data = trend_data.melt(id_vars = "year", var_name = "crime", value_name = "crime_count")

    return trend_data