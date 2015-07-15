
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
        return "NULL"
    
def timeSub(time2, time1):
    return datetime.combine(date.today(), time2) - datetime.combine(date.today(), time1)


def analyze(file_location):
    import pandas as pd
    import numpy as np
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    from workdays import networkdays
    import plotly.plotly as py
    from plotly.graph_objs import *

    df_adv = pd.read_excel(file_location, 'First Analysis')
    if 'TotalTAT' not in df_adv.columns:
        tat = df_adv.apply(lambda row: networkdays(row['SUBMIT_DATE'], row['RECEIPT_DATE']), axis=1)
        tat = tat.applymap(lambda x: x if x >= 0 else None)
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
        y = df_adv['TotalTAT'][df_adv['RPM']==1]
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
                zeroline = True,
            ),
            width = 1000,
            height = 1000,
        )

    fig = Figure(data =data, layout=layout)
    plot_url = py.plot(fig, filename = 'RPMs')
    py.image.save_as(fig, 'files/plot.png')


    #formula: response = constant + predictor + predictor + predictor + predictor(categorical)
    est = smf.ols(formula = 'TotalTAT ~ C(RPM)', data=df_adv).fit()

    return est
