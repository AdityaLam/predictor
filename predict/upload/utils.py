
def netWorkHours(date1, time1, date2, time2):
    from datetime import datetime, time, date
    from workdays import networkdays

    if time1 > time(18):
        time1 = time(18)
    elif time1 < time(8):
        time1 = time(8)
    
    if time1 > time(18):
        time1 = time(18)
    elif time1 < time(8):
        time1 =time(8)

    
    if date1 == date2:
        return str(timeSub(time2, time1))
    elif date1 < date2:
        if time1 < time2 :
            return str(networkdays(date1,date2) - 1) + 'days ' + str(timeSub(time2, time1))
        elif time1 > time2:
            delta1 = timeSub(time(18), time1)
            print( "delta 1: ",  delta1)
            delta2 = timeSub(time2,time(8))
            print("delta 2: " , delta2)
            return str(networkdays(date1,date2) - 2) + 'days ' + str(delta1 + delta2)
    else: 
        return None
    
def timeSub(time2, time1):
    return datetime.combine(date.today(), time2) - datetime.combine(date.today(), time1)


from plotly.graph_objs import * 
import os

script_dir = os.path.dirname(__file__)
rel_data = "../files/upload/data.csv"
data_path = os.path.join(script_dir, rel_data)

def find_count():
    with open(data_path, 'rt') as csvfile:
        reader = csv.reader(csvfile)
        rpm, erf = 0,0
        for row in reader:
            if row[4] == '01':
                rpm += 1
            elif row[4] == '02':
                erf += 1
        return rpm, erf

def analyze():
    import pandas as pd
    import numpy as np
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    from workdays import networkdays
    import plotly.plotly as py
    import os

    df_adv = pd.read_csv(data_path)
    if 'TotalTAT' not in df_adv.columns:
        tat = df_adv.apply(lambda row: networkdays(pd.to_datetime(row['SUBMIT_DATE']), pd.to_datetime(row['RECEIPT_DATE'])) if row['SUBMIT_DATE'] is not None and row['RECEIPT_DATE'] is not None else None, axis=1)
        tat = tat.apply(lambda x: x if x >= 0 else None)
        tat = pd.DataFrame(tat, columns = ['TotalTAT'])
        df_adv = pd.concat([df_adv, tat], axis=1)
    if 'RPM' not in df_adv.columns:
        df_adv['RPM'] = df_adv['ERF_TYPE'] - 1


    py.sign_in('dyp93', 'ax2h1t1kzc')

    trace0 = Box(
        y= df_adv['TotalTAT'][df_adv['RPM']==0],
        name = 'RPMs',
        boxpoints='all',
        jitter = 0.9,
        pointpos = 1.8,
        marker = Marker(color = 'rgb(8, 81, 156)',
            )

    )

    trace1 = Box(
        y = df_adv['TotalTAT'][df_adv['RPM']==1],
        name = 'ERFs',
        boxpoints='all',
        jitter = 0.9,
        pointpos = 1.8,
        marker = Marker(color = 'rgb(40, 180, 220)'
        )
    )

    data = Data([trace0,trace1])
    
    layout = Layout(
            yaxis = YAxis(
                title = 'number of days',
                range = [0, (conf[1][0] * 2)],
                zeroline = True,
            ),
            width = 1000,
            height = 1000,
        )

    script_dir = os.path.dirname(__file__)
    rel_data = "../static/plot.png"
    img_path = os.path.join(script_dir, rel_data)


    fig = Figure(data =data, layout=layout)
    py.image.save_as(fig, img_path)


    #formula: response = constant + predictor + predictor + predictor + predictor(categorical)
    est = smf.ols(formula = 'TotalTAT ~ C(RPM)', data=df_adv).fit()

    return est
