import sys
import threading
import warnings
from datetime import datetime
from math import sqrt

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from django.core.management import BaseCommand
from django.db.models import Count
from impyute import mice
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sqlalchemy import create_engine
from statsmodels.graphics.tsaplots import month_plot
import pmdarima as pm
from statsmodels.tsa.seasonal import seasonal_decompose
from stldecompose import decompose
from stldecompose import forecast
from stldecompose.forecast_funcs import (seasonal_naive)

from tabiri_api.apps.tabiri_gis.models import Country, VaccineDemandFeature, HealthFacility

warnings.filterwarnings("ignore")
plt.style.use('seaborn-bright')
sys.setrecursionlimit(100000)  # Increase the recursion limit of the OS


# Function to convert string to date
def convert_string_date(date_str):
    return datetime.strptime(date_str, '%Y%m')


class VaccineDemandForecastor(threading.Thread):
    def __init__(self, queryset, vaccine, health_facility,wastage_rate_type, metadata):
        threading.Thread.__init__(self)
        self.DB_TYPE = 'postgresql'
        self.DB_USER = 'ochomoswill'
        self.DB_PASS = '5ky302ld'
        self.HOST = 'localhost'
        self.PORT = '5432'
        self.DB_NAME = 'sample_db'
        self.INFANT_MORTALITY_RATE = 0.337
        self.queryset = queryset
        self.vaccine = vaccine
        self.wastage_rate_type = wastage_rate_type
        self.health_facility = health_facility
        self.df = None
        self.trunc_df = None
        self.series = None
        self.train = None
        self.valid = None
        self.metadata = metadata
        self.has_validation_error = False

    def data_collection(self):
        try:
            self.df = pd.DataFrame(list(self.queryset))
            # print(self.df.columns)
        except Exception as e:
            self.metadata['report_status'] = 'ERROR'
            self.metadata['report_description'] = 'Query <-> File structure mismatch. Sync up your queries mahn. => ' \
                                                  '' + str(e)

            print(self.metadata['report_description'])
            return

    def data_collection_sql(self):
        try:
            # connecting to database and fetching data
            engine = create_engine('{}://{}:{}@{}:{}/{}'.format(
                self.DB_TYPE,
                self.DB_USER,
                self.DB_PASS,
                self.HOST,
                self.PORT,
                self.DB_NAME))

            self.df = pd.read_sql(QUERY, engine)
        except Exception as e:
            self.metadata['report_status'] = 'ERROR'
            self.metadata['report_description'] = 'Query <-> File structure mismatch. Sync up your queries mahn. => ' \
                                                  '' + str(e)
            print(self.metadata['report_description'])
            return

    def data_description(self):
        self.df.describe()

    def data_preparation(self):
        # Function to preprocess the data

        # merging the month and year columns to create a new column ['Period']
        self.df['Period'] = self.df['year'].map(str) + self.df['month'].map(str)
        # categorize period
        self.df['Period'] = self.df["Period"].apply(lambda value: (convert_string_date(str(value))))

        # normalize the data
        self.df[self.wastage_rate_type] = (self.df[self.wastage_rate_type] - self.df[self.wastage_rate_type].min()) / (
                self.df[self.wastage_rate_type].max() - self.df[self.wastage_rate_type].min())

        # Drop Unnecessary Columns
        cols = ['month', 'year']
        self.df.drop(cols, axis=1, inplace=True)

        # Set Period Column as the index
        self.df = self.df.set_index('Period')

    def data_quality_verification(self):
        try:
            cols = ["bcg_wastage_rate", "totalbirths"]
            self.df[cols] = self.df[cols].replace({0: np.nan})
            self.df["bcg_wastage_rate"] = self.df["bcg_wastage_rate"].replace({1: np.nan})
            # dealing with the missing data
            # imputed_training = fast_knn(org_unit_group.values, k=3)
            # print(self.df.values)
            imputed_training = mice(self.df.values)
            self.df[cols] = imputed_training

            # convert column "totalbirths" to int64 dtype
            self.df = self.df.astype({"totalbirths": int})
        except Exception as e:
            self.metadata['report_status'] = 'ERROR'
            self.metadata['report_description'] = 'Data <-> Data Quality Verification Failed. => ' \
                                                  '' + str(e)
            self.has_validation_error = True
            return

    def data_integration(self):
        if self.has_validation_error:
            return
        # calculate wastage factor
        # wastage_factor = 100 / (100 - Wastage Rate)
        self.df['wastage_factor'] = 100 / (100 - (self.df[self.wastage_rate_type] * 100))

        # calculate target_population
        # births [BCG]
        # surviving_infants [The Rest]
        # Surviving infants = Births × (1 − Infant mortality rate[33.6 as of 2017]).
        # surviving_infants + women_child_bearing_age [Tetanus]
        if self.wastage_rate_type == "bcg_wastage_rate":
            self.df['target_pop'] = abs(self.df['totalbirths'])
        else:
            self.df['target_pop'] = self.df['totalbirths'] * (1 - self.INFANT_MORTALITY_RATE)

        # total doses = target_pop * no_of_doses * target_coverage(assuming its 100%) * wastage_factor
        # therefore, total doses = target_pop * no_of_doses * wastage_factor
        self.df['total_doses'] = self.df['target_pop'] * 1 * self.df['wastage_factor']

    def show_month_plot(self):
        if self.has_validation_error:
            return
        # Month_plot() requires the data to have a monthly (12 or 'M') frequency
        # Alternative: quarter_plot() for dataset with a frequency of 4 or 'Q'
        fig, ax1 = plt.subplots(1, 1, figsize=(12, 8))
        month_plot(self.series, ax=ax1)
        plt.title("Month Plot of Vaccine Demand of {} in {}".format(self.vaccine, self.health_facility))
        plt.grid(axis='both')
        plt.tight_layout()
        plt.show()

    def show_season_plot(self):
        if self.has_validation_error:
            return
        # Restructuring of df by pandas pivot_table
        pivot_df = pd.pivot_table(self.trunc_df, index=self.trunc_df.index.month,
                                  columns=self.trunc_df.index.year,
                                  values='total_doses')
        # Add a new index to the pivot table
        month_names = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
        pivot_df.index = month_names
        #
        # Creating the season plot
        plt.figure(figsize=(12, 8))
        plt.plot(pivot_df)
        plt.title("Seasonal Plot of Vaccine Demand of {} in {}".format(self.vaccine, self.health_facility))
        plt.grid(axis='both')
        plt.legend(pivot_df.columns)
        plt.tight_layout()
        plt.show()

    def org_vaccine_demand_plot(self):
        if self.has_validation_error:
            return
        plt.figure(figsize=(12, 8))
        plt.plot(self.series, label='Vaccine Demand')
        plt.title('Original Dataset')
        plt.legend()
        plt.show()

    def seasonal_arima(self):
        if self.has_validation_error:
            return

        try:
            # Seasonal ARIMA model with pmdarima
            mySA = pm.auto_arima(self.series, error_action="ignore", suppress_warnings=True,
                                 seasonal=True, m=12, start_q=1, start_p=1,
                                 start_Q=0, start_P=0, max_order=5, max_d=1,
                                 max_D=1, D=1, stepwise=False, trace=False)
            mySA.fit(self.train)

            forecast = mySA.predict(n_periods=len(self.valid))
            forecast = pd.DataFrame(forecast, index=self.valid.index, columns=['Prediction'])

            # plot the predictions for self.validation set
            plt.figure(figsize=(12, 8))
            plt.plot(self.train, label='Train')
            plt.plot(self.valid, label='Valid')
            plt.plot(forecast, label='Prediction')
            plt.title('SARIMA Forecast')
            plt.legend()
            plt.show()

            mae = mean_absolute_error(self.valid, forecast)
            print('MAE: %f' % mae)

            mse = mean_squared_error(self.valid, forecast)
            print('MSE - {}'.format(mse))

            #  an RMSE of zero indicates no error
            rms = sqrt(mse)
            print('RMS - {}'.format(rms))
        except Exception as e:
            self.metadata['report_status'] = 'ERROR'
            self.metadata['report_description'] = 'Seasonal ARIMA <-> Seasonal ARIMA Failed. => ' \
                                                  '' + str(e)
            self.has_validation_error = True
            return

    def additive_or_multiplicative_decomposition(self):
        if self.has_validation_error:
            return
        # Additive or multiplicative decomposition
        plt.figure(figsize=(12, 6))
        plt.plot(self.series)
        plt.title('Additive or multiplicative decomposition')
        plt.show()

    def simple_seasonal_decomposition(self):
        if self.has_validation_error:
            return
        # Seasonal Decomposition
        # By default model = "additive"
        # For a multiplicative model use model = "multiplicative"
        org_unit_group_decomposed = seasonal_decompose(self.series)
        #
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(14, 9))
        self.series.plot(ax=ax1)
        org_unit_group_decomposed.trend.plot(ax=ax2)
        org_unit_group_decomposed.seasonal.plot(ax=ax3)
        org_unit_group_decomposed.resid.plot(ax=ax4)
        ax1.set_title("Vaccine Demand for {} in {}".format(self.vaccine, self.health_facility))
        ax2.set_title("Trend")
        ax3.set_title("Seasonality")
        ax4.set_title("Residuals")
        plt.tight_layout()
        plt.show()

    def stl_seasonal_decomposition(self):
        if self.has_validation_error:
            return
        # Decomposition based on stl - Package: stldecompose
        org_unit_group_stl = decompose(self.series, period=12)

        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(14, 9))
        self.series.plot(ax=ax1)
        org_unit_group_stl.trend.plot(ax=ax2)
        org_unit_group_stl.seasonal.plot(ax=ax3)
        org_unit_group_stl.resid.plot(ax=ax4)
        ax1.set_title("Vaccine Demand for {} in {}".format(self.vaccine, self.health_facility))
        ax2.set_title("Trend")
        ax3.set_title("Seasonality")
        ax4.set_title("Residuals")
        plt.tight_layout()
        plt.show()

        # Eliminating the seasonal component
        org_unit_group_adjusted = self.series - org_unit_group_stl.seasonal
        plt.figure(figsize=(12, 8))
        org_unit_group_adjusted.plot()
        plt.title(
            "Plot of Vaccine Demand of {} in {} without Seasonal Component".format(self.vaccine, self.health_facility))
        plt.show()
        #
        # Getting the seasonal component only
        # Seasonality gives structure to the data
        plt.figure(figsize=(12, 8))
        org_unit_group_stl.seasonal.plot()
        plt.title("Plot of Seasonal Component of Vaccine Demand of {} in {}".format(self.vaccine, self.health_facility))
        plt.show()

        # Creating a forecast based on STL
        stl_fcast = forecast(org_unit_group_stl, steps=12, fc_func=seasonal_naive,
                             seasonal=True)

        # Plot of the forecast and the original data
        plt.figure(figsize=(12, 8))
        plt.plot(self.series, label='BCG Wastage Rate')
        plt.plot(stl_fcast, label=stl_fcast.columns[0])
        plt.title("Plot of Vaccine Demand of {} in {} Next Year Forecast".format(self.vaccine, self.health_facility))
        plt.legend()
        plt.show()

    def feature_select_and_split_dataset(self):
        if self.has_validation_error:
            return
        # Pandas DataFrame object with time stamp (monthly frequency)
        self.trunc_df = pd.DataFrame(self.df.total_doses.values, columns=['total_doses'],
                                     index=self.df.index)

        # divide into train and validation set
        self.train = self.trunc_df[:int(0.8 * (len(self.trunc_df)))]
        self.valid = self.trunc_df[int(0.8 * (len(self.trunc_df))):]
        #
        # Pandas Series object with time stamp (monthly frequency)
        self.series = pd.Series(self.df.total_doses.values,
                                index=self.df.index)

    def run(self):
        self.data_collection()
        self.data_preparation()
        self.data_quality_verification()
        self.data_integration()
        self.feature_select_and_split_dataset()
        self.show_month_plot()
        self.show_season_plot()
        self.org_vaccine_demand_plot()
        self.seasonal_arima()
        self.additive_or_multiplicative_decomposition()
        self.simple_seasonal_decomposition()
        self.stl_seasonal_decomposition()


QUERY = "select vdf.month, vdf.year, vdf.bcg_wastage_rate, totalbirths from vaccine_demand_features vdf inner join health_facilities h on vdf.orgUnitId = h.orgUnitId where orgUnitName='Ndaragwa Health Centre' and year>=2014 and year<2019 order by year, month asc"

metadata = {
    'report_status': "",
    'report_description': ""
}

# VaccineDemandFeature.objects.filter(orgunitid__dhis2parentid__const_code__county_cod=18).count()
# Get Unique Org Units
# query = VaccineDemandFeature.objects.filter(orgunitid__dhis2parentid__const_code__county_cod=18).order_by('year','-month')
# health_facilities_list = query.values('orgunitid').distinct
# forecast_vaccine_demand = VaccineDemandForecastor(QUERY, 'BCG', 'Ndaragwa Health Centre', metadata)
# forecast_vaccine_demand.run()


# Queries for total count
# Constituency.objects.filter(county_cod=18).count()
# Ward.objects.filter(const_code__county_cod=18).count()
# HealthFacility.objects.filter(dhis2parentid__const_code__county_cod=18).count()


query = VaccineDemandFeature.objects.filter(orgunitid__dhis2parentid__const_code__county_cod__county_cod=18).order_by('year','-month')
health_facilities_list = HealthFacility.objects.filter(dhis2parentid__const_code__county_cod=18).values('orgunitid', "orgunitname").distinct()

vaccines_list = [
    {'vaccine': 'BCG', 'wastage_rate_type':'bcg_wastage_rate'},
    {'vaccine': 'Tetanus', 'wastage_rate_type':'tetanus_toxoid_wastage_rate'},
    {'vaccine': 'Measles', 'wastage_rate_type':'measles_wastage_rate'},
    {'vaccine': 'OPV', 'wastage_rate_type':'opv_wastage_rate'},
    {'vaccine': 'Pneumococal', 'wastage_rate_type':'pneumococal_wastage_rate'},
    {'vaccine': 'Vitamin A', 'wastage_rate_type':'vit_a_wastage_rate'},
    {'vaccine': 'Yellow Fever', 'wastage_rate_type':'yellow_fever_wastage_rate'},
    {'vaccine': 'DPT', 'wastage_rate_type':'dpt_wastage_rate'},
]


def forecast_demand_by_vaccine(start_year=2014, wastage_rate_type='bcg_wastage_rate', vaccine='BCG'):
    now = datetime.now()
    i = 1
    for hf in health_facilities_list:
        print('{} - {} '.format(str(i), hf))
        i = i + 1
        query = VaccineDemandFeature.objects.filter(orgunitid=hf['orgunitid'], year__gte=start_year, year__lt=2020).order_by('year','month').values('month', 'year', wastage_rate_type, 'totalbirths')
        forecast_vaccine_demand = VaccineDemandForecastor(query, vaccine, hf['orgunitname'], wastage_rate_type, metadata)
        forecast_vaccine_demand.run()


for vaccine in vaccines_list:
    print(vaccine['vaccine'])
    forecast_demand_by_vaccine(2016, vaccine['wastage_rate_type'], vaccine['vaccine'])



#


class Command(BaseCommand):
    help = 'Custom Command to Forecast Vaccine Demand'

    def handle(self, *args, **kwargs):
        self.forecast()

    def forecast(self):
        pass
        i = 1
        for hf in health_facilities_list:
            print('{} - {} '.format(str(i), hf))
            i = i + 1
            forecast_vaccine_demand = VaccineDemandForecastor(VaccineDemandFeature.objects.filter(orgunitid=hf['orgunitid']).order_by('year','-month').values('month', 'year', 'bcg_wastage_rate', 'totalbirths'), 'BCG', hf['orgunitname'], metadata)
            forecast_vaccine_demand.run()














