import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures



def gather_data(file_path):
    """""
    Gathers the data from the Data.txt listed in file_path and creates a Dataframe from it
    """""
    datas = pd.read_csv(file_path, header=0, delimiter='|')
    time_x = datas.loc[:, '   missn,_time '].values
    y = datas.loc[:, '   alpha,__deg '].values
    x = list(zip(time_x,y))
    x = pd.DataFrame(x)
    x = x.iloc[:, 0:1].values
    return x, y

def calculate_angle_of_attack(file_path):
    datas = pd.read_csv(file_path, header=0, delimiter='|')
    pitch = datas.loc[:,'   pitch,__deg '].values
    v_path = datas.loc[:,'   vpath,__deg '].values
    g_load = datas.loc[:, '   Gload,axial '].values
    
    y_2 = []

    index = datas.shape[0]-1
    for i in range(1, index):
        y_2.append(pitch[i]-v_path[i])
    
    x_2 = list(zip(x,y_2))
    x_2 = pd.DataFrame(x_2)
    x_2 = x_2.iloc[:, 0:1].values

    return x_2, y_2, g_load

def prediction(x, y, sample_rate, intervals):
    """""
    Takes the Dataframe from gather_data() and creates a sliding window to recreate live data.
    Uses that sliding window at the intervals and fits a 3rd order polynomial to it.
    The polynomial is then used to 'predict' future values.
    Compares the actual time when the data gets to 10 degrees and compares it to when the fitted polynomial to reach 10 degrees
    """""   
    aoa_values = [[],[]] # row 0 = predictided aoa, row 1 = actual aoa at the time value 
    for interval in intervals:
        pred_trigger = False
        ac_trigger = False
        predictive_time = []
        actual_time = []
        cycle_predictive = [[],[]]
        time_difference = []

        
        plt.figure()
        for i in range(len(x)):
            plt.axhline(10, c = 'red', zorder=1)
            
            if i > interval:
                poly = PolynomialFeatures(degree = 3)
                700
                # Setting the sliding window 
                x_slide = [x[(i-d)] for d in range(interval)]
                y_slide = [y[(i-d)] for d in range(interval)]
                
                # Setting the regression parameters
                x_poly = poly.fit_transform(x_slide)
                poly.fit(x_poly, y_slide)
                lin2 = LinearRegression()
                lin2.fit(x_poly, y_slide)
                
                # Calculates the next value in the array - works off of intervals 
                pred = [x_slide[-1] + time_diff/sample_rate for time_diff in range(interval)] # range decides how many estimated values there are 
                
                # Uses polyfit to estimate the next AoA value                        
                predictor = lin2.predict(poly.fit_transform(pred))
                pred = np.concatenate(pred)
                cycle_predictive = [pred, predictor]

                
                # Uses the last value in the most recently polynomial calculation and sees if its above 10, then marks it on the graph
                # pred_trigger stops it from activating concecutively
                if cycle_predictive[1][-1] >= 10 and pred_trigger == False:
                    # plt.plot(cycle_predictive[0][-1], cycle_predictive[1][-1], '', c='black', zorder=2)
                    plt.axvline(cycle_predictive[0][-1], ls='--',c='blue')
                    plt.axvline(cycle_predictive[0][0], c='blue')
                    predictive_time = cycle_predictive[0][0]
                    print("pred time", predictive_time)
                    print("pred value", cycle_predictive[1][-1])
                    aoa_values[0].append(cycle_predictive[1][-1])
                    pred_trigger = True
                    
            
                # Shows when the actual AoA's gathered from data reach 10 and marks it on the graph
                if y_slide[-1] >= 10 and ac_trigger == False: # Actual time when the AoA reaches 10, when stall warning starts to activate in X-Plane
                    plt.axvline(x_slide[-1], c='red', zorder=1)
                    actual_time = float(x_slide[-1])
                    print("ac time",actual_time)
                    print("ac value", y_slide[-1])
                    ac_trigger = True
                    aoa_values[1].append(y_slide[-1])
                
                
                plt.plot(cycle_predictive[0],cycle_predictive[1], zorder=1)

                # if the slope of the most recent values of the prediction polynomial and actual AoAare negative and below 8 
                # then it sets the trigger to False so it can activate again if AoA goes above 10
                if (cycle_predictive[1][-1] - cycle_predictive[1][-2])/(cycle_predictive[0][-1]-cycle_predictive[0][-2]) < 0 and cycle_predictive[1][-1] < 8:
                    pred_trigger = False
                
                if (y_slide[-1]-y_slide[-2])/(x_slide[-1]-x_slide[-2]) < 0 and y_slide[-1] < 8:
                    ac_trigger = False
        
        # Finds the differences between the actual time that AoA > 10 and the prediction > 10
        if type(predictive_time) == list: # if the data goes above 10 two or more times
            time_difference = [i-j for i,j in zip(actual_time,predictive_time)]    
        else:
            time_difference = actual_time - predictive_time
        print(time_difference)
        print("-----------")
       


    # Plots the different interval polynomials 
    plt.figure()
    plt.plot(x,y, c='green')
    plt.axhline(10, c='red')
    
    return aoa_values


if __name__ == '__main__':
    
    sample_rate = 20
    intervals = [10, 20, 50, 100]
    file_path = "Pilot 4/Data1_2.txt"

    x, y = gather_data(file_path)
    x_2, y_2, g_load = calculate_angle_of_attack(file_path)
    actual_aoa = prediction(x, y, sample_rate, intervals)
    calc_aoa = prediction(x_2,y_2, sample_rate, intervals) 
    
    print(actual_aoa)
    print(calc_aoa)

    plt.figure()
    ax1 = plt.subplot()
    l1, = ax1.plot(x,y,c='blue')
    l2, = ax1.plot(x_2,y_2,c='red')
    ax2 = ax1.twinx()
    l3, = ax2.plot(x_2, g_load[:-2], c='green')
    plt.show()



