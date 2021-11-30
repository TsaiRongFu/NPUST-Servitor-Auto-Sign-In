from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import PySimpleGUI as sg
import datetime

timeList = ["08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00", "13:30-14:30", "14:30-15:30", "15:30-16:30", "16:30-17:30"]
amTimeList = ["08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00"]
pmTimeList = ["13:30-14:30", "14:30-15:30", "15:30-16:30", "16:30-17:30"]
weekList = ["一", "二", "三", "四", "五"]
weekEnglishList = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
monthList = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
nonleapYearDay = ["", ""]
weekResult = {"MondayAm":"", "MondayPm":"", "TuesdayAm":"", "TuesdayPm":"", "WednesdayAm":"", "WednesdayPm":"", "ThursdayAm":"", "ThursdayPm":"", "FridayAm":"", "FridayPm":""}

CE = datetime.datetime.now().year
nowMonth = datetime.datetime.now().month

cn_number = {
    "一":1,
    "二":2,
    "三":3,
    "四":4,
    "五":5,
    "六":6,
    "七":7,
    "八":8,
    "九":9,
    "十":10,
    "十一":11,
    "十二":12,
}

monthKeyValue={
    1:'一月',
    2:'二月',
    3:'三月',
    4:'四月',
    5:'五月',
    6:'六月',
    7:'七月',
    8:'八月',
    9:'九月',
    10:'十月',
    11:'十一月',
    12:'十二月',
}

dayKeyValue_CE={
    '一月':True,
    '二月':2,
    '三月':True,
    '四月':False,
    '五月':True,
    '六月':False,
    '七月':True,
    '八月':True,
    '九月':False,
    '十月':True,
    '十一月':False,
    '十二月':True,
}

dayKeyValue_nonleap={
    '一月':True,
    '二月':2,
    '三月':True,
    '四月':False,
    '五月':True,
    '六月':False,
    '七月':True,
    '八月':True,
    '九月':False,
    '十月':True,
    '十一月':False,
    '十二月':True,
}

AmPermutations={
    "0000":["0"],
    "1111":["8-12"],
    "1000":["8-9"],
    "0100":["9-10"],
    "0010":["10-11"],
    "0001":["11-12"],
    "1100":["8-10"],
    "0110":["9-11"],
    "0011":["10-12"],
    "1010":["8-9", "10-11"],
    "0101":["9-10", "11-12"],
    "1001":["8-9", "11-12"],
    "1110":["8-11"],
    "0111":["9-12"],
    "1101":["8-10", "11-12"],
    "1011":["8-9", "10-12"],
}

PmPermutations={
    "0000":["0"],
    "1111":["13-17"],
    "1000":["13-14"],
    "0100":["14-15"],
    "0010":["15-16"],
    "0001":["16-17"],
    "1100":["13-15"],
    "0110":["14-16"],
    "0011":["15-17"],
    "1010":["13-14", "15-16"],
    "0101":["14-15", "16-17"],
    "1001":["13-14", "16-17"],
    "1110":["13-16"],
    "0111":["14-17"],
    "1101":["13-15", "16-17"],
    "1011":["13-14", "15-17"],
}

monthConversion = monthKeyValue.get(nowMonth)

if (CE%4 == 0 ) & (CE%100 != 0 ):
    leap = True
elif (CE%400 == 0):
    leap = False
else:
    leap = False

if leap:
    if (dayKeyValue_CE.get(monthConversion) == True):
        defualtDayList = ['1-7號', '8-14號', '15-21號', '22-28號', '29-31號']
    elif (dayKeyValue_CE.get(monthConversion) == False):
        defualtDayList = ['1-7號', '8-14號', '15-21號', '22-28號', '29-30號']
    elif (dayKeyValue_CE.get(monthConversion) == 2):
        defualtDayList = ['1-7號', '8-14號', '15-21號', '22-28號', '29號']
else:
    if dayKeyValue_nonleap.get(monthConversion) == True:
        defualtDayList = ['1-7號', '8-14號', '15-21號', '22-28號', '29-31號']
    elif dayKeyValue_nonleap.get(monthConversion) == False:
        defualtDayList = ['1-7號', '8-14號', '15-21號', '22-28號', '29-30號']
    elif dayKeyValue_nonleap.get(monthConversion) == 2:
        defualtDayList = ['1-7號', '8-14號', '15-21號', '22-28號']

def amCheckTime(values, week):
    amBinary = ""

    for amitem in amTimeList:
        if (values[week + amitem]):
            amBinary += "1"
        else:
            amBinary += "0"
    
    return amBinary

def pmCheckTime(values, week):
    pmBinary = ""
    
    for pmitem in pmTimeList:
        if (values[week + pmitem]):
            pmBinary += "1"
        else:
            pmBinary += "0"

    return pmBinary

def fillIn(browser, weekCode, day):
    if (weekCode == 1):
        if (weekResult['MondayAm'][0] != "0"):
            for j in range (len(weekResult['MondayAm'])):
                Select(browser.find_element(By.NAME , 'jump[ClockDate][day]')).select_by_value(str(day))
                Select(browser.find_element(By.NAME , 'jump[ClockDate][month]')).select_by_value(str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")))
                Select(browser.find_element(By.NAME , 'jump[ClockIn][hour]')).select_by_value(weekResult['MondayAm'][j].split('-')[0])
                Select(browser.find_element(By.NAME , 'jump[ClockIn][minu]')).select_by_value("0")
                Select(browser.find_element(By.NAME , 'jump[ClockOut][hour]')).select_by_value(weekResult['MondayAm'][j].split('-')[1])
                Select(browser.find_element(By.NAME , 'jump[ClockOut][minu]')).select_by_value("0")
                browser.find_element(By.NAME , 'cmd').click()
                browser.switch_to.alert.accept()

        if (weekResult['MondayPm'][0] != "0"):
            for j in range (len(weekResult['MondayPm'])):
                Select(browser.find_element(By.NAME , 'jump[ClockDate][day]')).select_by_value(str(day))
                Select(browser.find_element(By.NAME , 'jump[ClockDate][month]')).select_by_value(str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")))
                Select(browser.find_element(By.NAME , 'jump[ClockIn][hour]')).select_by_value(weekResult['MondayPm'][j].split('-')[0])
                Select(browser.find_element(By.NAME , 'jump[ClockIn][minu]')).select_by_value("30")
                Select(browser.find_element(By.NAME , 'jump[ClockOut][hour]')).select_by_value(weekResult['MondayPm'][j].split('-')[1])
                Select(browser.find_element(By.NAME , 'jump[ClockOut][minu]')).select_by_value("30")
                browser.find_element(By.NAME , 'cmd').click()
                browser.switch_to.alert.accept()
                
    elif (weekCode == 2):
        if (weekResult['TuesdayAm'][0] != "0"):
            for j in range (len(weekResult['TuesdayAm'])):
                Select(browser.find_element(By.NAME , 'jump[ClockDate][day]')).select_by_value(str(day))
                Select(browser.find_element(By.NAME , 'jump[ClockDate][month]')).select_by_value(str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")))
                Select(browser.find_element(By.NAME , 'jump[ClockIn][hour]')).select_by_value(weekResult['TuesdayAm'][j].split('-')[0])
                Select(browser.find_element(By.NAME , 'jump[ClockIn][minu]')).select_by_value("0")
                Select(browser.find_element(By.NAME , 'jump[ClockOut][hour]')).select_by_value(weekResult['TuesdayAm'][j].split('-')[1])
                Select(browser.find_element(By.NAME , 'jump[ClockOut][minu]')).select_by_value("0")
                browser.find_element(By.NAME , 'cmd').click()
                browser.switch_to.alert.accept()
                
        if (weekResult['TuesdayPm'][0] != "0"):
            for j in range (len(weekResult['TuesdayPm'])):
                Select(browser.find_element(By.NAME , 'jump[ClockDate][day]')).select_by_value(str(day))
                Select(browser.find_element(By.NAME , 'jump[ClockDate][month]')).select_by_value(str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")))
                Select(browser.find_element(By.NAME , 'jump[ClockIn][hour]')).select_by_value(weekResult['TuesdayPm'][j].split('-')[0])
                Select(browser.find_element(By.NAME , 'jump[ClockIn][minu]')).select_by_value("30")
                Select(browser.find_element(By.NAME , 'jump[ClockOut][hour]')).select_by_value(weekResult['TuesdayPm'][j].split('-')[1])
                Select(browser.find_element(By.NAME , 'jump[ClockOut][minu]')).select_by_value("30")
                browser.find_element(By.NAME , 'cmd').click()
                browser.switch_to.alert.accept()
                
    elif (weekCode == 3):
        if (weekResult['WednesdayAm'][0] != "0"):
            for j in range (len(weekResult['WednesdayAm'])):
                Select(browser.find_element(By.NAME , 'jump[ClockDate][day]')).select_by_value(str(day))
                Select(browser.find_element(By.NAME , 'jump[ClockDate][month]')).select_by_value(str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")))
                Select(browser.find_element(By.NAME , 'jump[ClockIn][hour]')).select_by_value(weekResult['WednesdayAm'][j].split('-')[0])
                Select(browser.find_element(By.NAME , 'jump[ClockIn][minu]')).select_by_value("0")
                Select(browser.find_element(By.NAME , 'jump[ClockOut][hour]')).select_by_value(weekResult['WednesdayAm'][j].split('-')[1])
                Select(browser.find_element(By.NAME , 'jump[ClockOut][minu]')).select_by_value("0")
                browser.find_element(By.NAME , 'cmd').click()
                browser.switch_to.alert.accept()
                
        if (weekResult['WednesdayPm'][0] != "0"):
            for j in range (len(weekResult['WednesdayPm'])):
                Select(browser.find_element(By.NAME , 'jump[ClockDate][day]')).select_by_value(str(day))
                Select(browser.find_element(By.NAME , 'jump[ClockDate][month]')).select_by_value(str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")))
                Select(browser.find_element(By.NAME , 'jump[ClockIn][hour]')).select_by_value(weekResult['WednesdayPm'][j].split('-')[0])
                Select(browser.find_element(By.NAME , 'jump[ClockIn][minu]')).select_by_value("30")
                Select(browser.find_element(By.NAME , 'jump[ClockOut][hour]')).select_by_value(weekResult['WednesdayPm'][j].split('-')[1])
                Select(browser.find_element(By.NAME , 'jump[ClockOut][minu]')).select_by_value("30")
                browser.find_element(By.NAME , 'cmd').click()
                browser.switch_to.alert.accept()
                
    elif (weekCode == 4):
        if (weekResult['ThursdayAm'][0] != "0"):
            for j in range (len(weekResult['ThursdayAm'])):
                Select(browser.find_element(By.NAME , 'jump[ClockDate][day]')).select_by_value(str(day))
                Select(browser.find_element(By.NAME , 'jump[ClockDate][month]')).select_by_value(str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")))
                Select(browser.find_element(By.NAME , 'jump[ClockIn][hour]')).select_by_value(weekResult['ThursdayAm'][j].split('-')[0])
                Select(browser.find_element(By.NAME , 'jump[ClockIn][minu]')).select_by_value("0")
                Select(browser.find_element(By.NAME , 'jump[ClockOut][hour]')).select_by_value(weekResult['ThursdayAm'][j].split('-')[1])
                Select(browser.find_element(By.NAME , 'jump[ClockOut][minu]')).select_by_value("0")
                browser.find_element(By.NAME , 'cmd').click()
                browser.switch_to.alert.accept()

        if (weekResult['ThursdayPm'][0] != "0"):
            for j in range (len(weekResult['ThursdayPm'])):
                Select(browser.find_element(By.NAME , 'jump[ClockDate][day]')).select_by_value(str(day))
                Select(browser.find_element(By.NAME , 'jump[ClockDate][month]')).select_by_value(str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")))
                Select(browser.find_element(By.NAME , 'jump[ClockIn][hour]')).select_by_value(weekResult['ThursdayPm'][j].split('-')[0])
                Select(browser.find_element(By.NAME , 'jump[ClockIn][minu]')).select_by_value("30")
                Select(browser.find_element(By.NAME , 'jump[ClockOut][hour]')).select_by_value(weekResult['ThursdayPm'][j].split('-')[1])
                Select(browser.find_element(By.NAME , 'jump[ClockOut][minu]')).select_by_value("30")
                browser.find_element(By.NAME , 'cmd').click()
                browser.switch_to.alert.accept()
                
    elif (weekCode == 5):
        if (weekResult['FridayAm'][0] != "0"):
            for j in range (len(weekResult['FridayAm'])):
                Select(browser.find_element(By.NAME , 'jump[ClockDate][day]')).select_by_value(str(day))
                Select(browser.find_element(By.NAME , 'jump[ClockDate][month]')).select_by_value(str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")))
                Select(browser.find_element(By.NAME , 'jump[ClockIn][hour]')).select_by_value(weekResult['FridayAm'][j].split('-')[0])
                Select(browser.find_element(By.NAME , 'jump[ClockIn][minu]')).select_by_value("0")
                Select(browser.find_element(By.NAME , 'jump[ClockOut][hour]')).select_by_value(weekResult['FridayAm'][j].split('-')[1])
                Select(browser.find_element(By.NAME , 'jump[ClockOut][minu]')).select_by_value("0")
                browser.find_element(By.NAME , 'cmd').click()
                browser.switch_to.alert.accept()
                

        if (weekResult['FridayPm'][0] != "0"):
            for j in range (len(weekResult['FridayPm'])):
                Select(browser.find_element(By.NAME , 'jump[ClockDate][day]')).select_by_value(str(day))
                Select(browser.find_element(By.NAME , 'jump[ClockDate][month]')).select_by_value(str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")))
                Select(browser.find_element(By.NAME , 'jump[ClockIn][hour]')).select_by_value(weekResult['FridayPm'][j].split('-')[0])
                Select(browser.find_element(By.NAME , 'jump[ClockIn][minu]')).select_by_value("30")
                Select(browser.find_element(By.NAME , 'jump[ClockOut][hour]')).select_by_value(weekResult['FridayPm'][j].split('-')[1])
                Select(browser.find_element(By.NAME , 'jump[ClockOut][minu]')).select_by_value("30")
                browser.find_element(By.NAME , 'cmd').click()
                browser.switch_to.alert.accept()
                
layout = [[sg.DropDown(monthList, enable_events=True, key='MonthDropDown', size=(15,4), default_value = monthConversion), sg.DropDown(defualtDayList, enable_events=True, key='WeekDropDown', size=(15,4))],
          [[sg.Text(f'時間', pad=(18,10))] + [sg.Text(f'星期{item}', pad=(35,10)) for item in weekList]],
          [[sg.Text(team, pad=(0,5)), sg.Checkbox(' ', key='Monday'+team, default=False, pad=(43,5)), sg.Checkbox(' ', key='Tuesday'+team, default=False, pad=(36,5)), sg.Checkbox(' ', key='Wednesday'+team, default=False, pad=(41,5)), sg.Checkbox(' ', key='Thursday'+team, default=False, pad=(38,5)), sg.Checkbox(' ', key='Friday'+team, default=False, pad=(40,5))] for team in timeList],
          [sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Button('登入', size=(25,1)), sg.Button('登入檢查', size=(25,1)), sg.Button('開始自動填入', size=(25,1)), sg.Button('Exit', size=(10,1))],
          [sg.Text('任何問題歡迎到：https://git.io/NPUST-Servitor-Auto-Sign-In，回報',font = ("Arial, 15"))]]

iconBase64 = b'iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAYAAAD0eNT6AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAACAASURBVHic7d15gB1lne//z1PLOX16SUJC2JcAYUt3BxicmaAO0JKVEIJLcAXnjvsV3EZGnatXrs7FHbyOOjrjMo4LY9T7k6uOond+6PxmuHKFdILEQNLpJCJLSEJWkvRy6vn90YQkpNM5fbrOeZ6qer/+0XS6qz4kOfX5nqfqVBkBAABv2XtmtGhKW7dMcIkS+0cKdJGsOUOyJ0kakrRD0noZPSBrfqZS8r9N5+rBY23XNDw5AACoiV3dWdL+8I9kkj+RsZdI5o8kzZIUjWMzm2Xsl7V/4DNmTt+uo30TAwAAAI7Y/9t5kkrmMlm9UNJlMrpUVi0pbX6zjN5hLn5o+Wi/yQAAAECT2Pu7L1Bgr5TRiyW9UNJZTdjtF7XuwneY679XPfSLDAAAADSIXTX7fFl7pWSvlNUVkk52EmT7/ntlhq8yPRv3H/jSeM4pAACAMdgHu8/WcPJiGb1IMguVJGe4zqSt+6Vt+1+o9vjXki4+8GVWAAAAqJO974JpKkdzZbVA0nxJp7rOdJiR8j/46+NKd5gF/e+RGAAAAKiZXb4s1DkPX6xQc2XtXElXSIpd5xrV88tfkkKTaGr72eaqNZs4BQAAwBjsb7tO1LC5XMYukV1zjaTjZF2nOobRyl+SqjbQwMBXJc1lBQAAgEPY1Z0lDZkrZe1CySzQyOfws+No5X9AaBIdP2kyKwAAgMKzq2a3SdWXyJplGtS1kiZn8iz5scpfGlkF2D9wcwb/6wAAmDj7267TNWyXSOY6jZzLL7nONCG1lP8B7fEqBgAAQGHYlbM6pfAaWbtEIzfiyUcPjqf8Jakc7szHfzgAAKOwy5eFOnfNn0n2WskslXS260ypG2/5S1JoEgYAAECu2HuujDRpy1wFeqVklkia5jpTw9RT/pJkTE6WPgAAhWatAq3sulxWr5LRyyUd7zpTw9Vb/pJk8nLuAwBQSHblrE4l5gaZ4AbJnuI6T9NMpPwlKTJVPgYIAMgUu3JWp2ywTNJrZTVz5K2s73fmSdFEy1+SwmAPAwAAwHv2ga4LFdpXyZpXyup813mcSaP8JSkONjAAAAC8ZO/vPEOheamkZZJeJFvws9Zplb8kxeFPC/6nCQDwiX2w+zgN21cp0I2ymuM6jzfSLH8j6fjW0xgAAABO2eXLQs18uEeBvVFWL5fU6jqTV9Isf0lqCbeb6zZN5RQAAMAJu6JzlqQbFax5vaxOKtJ1fDVLu/wlKQ7vlSQGAABA09j7LpimUvQ6SX8u6eKRL7pM5LFGlL8klcKvSdwHAADQYNbKaFXni2R1g2ReJ5b4j61R5R+Zql7+aMkYJawAAAAawt5/4cmKohu10r5J0jmu82RGo8pfkkpRnzFKJE4BAABSZO+5MtLkLVdL5o0yWiRr6ZnxaGT5S1LJ3HXg//IXAwCYMLtq9mmy1TfJbnujZIpzS940Nbr8jaRycseBXzIAAADqYq2MeruvkrFvVpJcJ5mYK/rq1Ojyl6SWaIvp2fjkgV8yAAAAxsX2XjxFpnq9Vtp3ythZrvNkXjPKX5Li8F8P/SUDAACgJvaB2XMUJG+TGb5eVi2u8+RCs8pfkoKDy/8SHwMEAIzBru4saTBYKtl3SXqh6zy50szyL4d7zUs3tR36JVYAAABHsKtmnyBr/5MG7U2SPc11ntxpZvlLUin4zfO/xAAAAHiOXTnrElnzViXJDZIqrvPkUrPLX5Li8CvP/xKnAACg4Ow9V0Y6buvLZPUOSS9ynSfXXJT/IXf/O+zLzU0BAPCFXd3ZrkHzBmnru2V1pus8ueei/CWpHK1+fvlLDAAAUDj2t10nalhv06BuljTVdZ5CcFX+khTrn0b7MgMAABSEXXnReVL17arqzRIf42sal+UfGquy/cJov8UAAAA5Z1d2vljWvE+2ulhc+9VcLstfklqC9aZn46gBGAAAIIfs8mWhZv5umUzwV7L2Etd5Csl1+UtSGC8/2m8xAABAjtj7L40V7H+1gjUfkDUXcG9+R3wof2OkSnDH0X6bAQAAcsCum1nWM5XXKxn4oIw5nd53yIfyl6TW6A+mZ+3Wo/02AwAAZNhzH+XbY/5Ksqdwht8xX8pfkiJz15i/3awcAID02PsumKZSdPPBj/Lxlt85n8rfSCqVP3WsbwEAZIRdNfsEJcktkt4qqd11HjzLp/KXpJZwq7lu0/SxvoUVAADIAHv/eccrLN2kJHm3pEmu8+AQvpW/JJWCnxzrWxgAAMBjzy31SxS/j3wsfyMpMv+9lm8DAHjmkOJ/l6TJrvNgFD6WvyRVoi1m6cYTjvVtrAAAgEfs6s6pGjTvEMXvN1/LX5JK0f+q5dsYAADAA7b34ikyQ+/RoHmnWOr3m8/lbyTFwW21fisAwBG7urOkoeDPZe1HJR1z2RaO+Vz+klSJNpulG0+q5VtZAQAAB6xVoJXdL9dg8knJznCdBzXwvfwlqRT8sNZvZQAAgCazK7rnqtfeLmO7WYjNiCyUv5EUtB7z6v9Dvx0A0AR2RfdcGfsxSS9wnQXjkIXyl6RK+KRZuunkWr+dFQAAaDDb2/nHkrlNsnNdZ8E4ZaX8JakU/mA8384AAAANYnsvPFeKbpPsy8WKa/ZkqfyNpDCu6er/AxgAACBl9sHu4zScvE8y75Js2XUe1CFL5S9JLdHjZv4jj4/nRxgAACAldnVnSYP6z6raD8mYqa7zoE5ZK39Jise3/C8xAABAKuyK7rka1Gcl2+k6CyYgi+UfGGlqUvPV/wcwAADABNhVs/9ISXK7ZK9wnQUTlMXyl6RK2G/mbNg83h9jAACAOtiVF50qO/xflSRvkBS6zoMJymr5S1I5+mo9P8YAAADjYFfNbpOtvk+2+peSaXWdBynIcvmHJlE8fHs9P8oAAAA1sqs6lyhJ/lYyZ7rOgpRkufwlqRI9aHo21PUfwAAAAMdgV80+X0nyOSWa7zoLUpT18pekOPhsvT/KjSkA4CjsqtltSpJbJH1AUsl1HqQoD+UfBUN6+e9bjFFS14+nnQcAss5aGfV23qAk+aSkE13nQcryUP6S1Br+R73lLzEAAMBh7MpZl2hl8LcyepHrLGiAvJS/JEXhxyby45wCAAA9e/vexN4qq7eLj/XlU57KvxzuMS/d1DGRTbACAKDQrFWgVd1vUtX+d0nTXOdBg+Sp/CWpHN490U0wAAAoLPtgd7dW2i9L9jLXWdBAeSt/GSks35rCVgCgWOy9l1VU2f0+cXV//uWu/CVVwq1m6abpE90MKwAACsX2dl0p7f6SpPNdZ0GD5bH8Jakcfj+NzTAAACgE+9uuEzVs7pDsq11nQRPktfwDI02xt6axKQYAALn23Gf6h3W7ZLnIrwjyWv6SVAn66nny32gYAADklu298Fz1Rl+SsS9xnQVNkufyl6RS9Lm0NsVFgAByx94zo0VT2j8o6RZxkV9x5L38J3jr3yM2l8ZGAMAX9oHZcxQkX5N0oessaKK8l78ktUb/llb5SwwAAHLC3jOjRZPbbpVJ3ivu5FcsRSh/IylOPpj2JgEg0+yK7ssU2K/J6gLXWdBkRSh/SaqE28zSTcenuUlWAABklr33sopadn1Yxr5Xlnf9hVOU8pekcnRn2ptkAACQSba364XS7q9Jhhv6FFGRyj+QVTn8b2lvlgEAQKY8965f4lx/URWp/CWppbTG9KzdmvZmGQAAZAbv+lG48pekij7diM1yESAA79l7L6uodffHZXWTpMB1HjhSxPKPwkHzik3lhmy6ERsFgLTYVbO7lOz+tqxmu84Ch4pY/pJUCX/eqE0zSQPwkrUytrfrnUqSByTKv9CKWv4yksIPNXLrAOAVe3/nGQrNNyRd6ToLHCts+UtqiTab6zae1KjNswIAwCu2t3uZQrNSlD+KXP6S1BL9YyM3zzUAALxgey+eIjP8d7L2Va6zwANFL//QJCqX/6aRu2AAAODcyMf7hr8pq7NdZ4EHil7+klSJVpie1XsauQsGAADO2PsvjRUO/BdJHxKnJCFR/geUwv/S6F1wESAAJ+zKWZ2ywbclXeQ6CzxB+Y+oRNvN0o1TG70bJm4ATWdXdN4oG9wnyh8HUP4HlYNvNGM3nAIA0DT23ssqquz5H5J9k+ss8Ajlf1BoEk0JPtyMXTEAAGgK+0DXhQp2L5fU5ToLPEL5H641+r9mTt+uZuyKUwAAGs6u6LxRgX4jyh+HovyPFJsPNmtXXAQIoGHs6s52DZovSXqt6yzwDOV/pJZwm7lu0/HN2h2nAAA0hF3ROUuDwXLJdrrOAs9Q/qMrB19r5u44BQAgdXZF540y5jeUP45A+Y8uNImGp97azF2yAgAgNfbh8zu0L/qSZF7jOgs8RPkfXSW611zzwN5m7pIBAEAq7IPd3dqXfF8y57nOAg9R/kdnJJWC97vYLQBMiF3Z9UpZfVVSm+ss8BDlP7ZKtMUs3XhCs3fLNQAA6maXLwvtis6Py+pOUf4YDeV/bOXw713slhUAAHWx910wTaXonyXNdZ0FnqL8jy0yVU0L203Pxqb/QXENAIBxsytnXSIb/EDSWa6zwFOUf21ao//P9Gxw8gfFKQAA42J7u18rG/y7KH8cDeVfIyPF9gMO9w4Ax2bvvzRWOHiHZN/uOgs8RvnXrjV80ly76WRXu+cUAIBjsisumS4z8F1JPa6zwGOU//iU4g+53D0rAADGZFd0Xyaj70v2FNdZ4DHKf3wq0WazdONJLiNwDQCAo7Iru98iY39J+WNMlP/4BMaqEr7cdQxOAQA4gl2+LNR5a26Xte9wnQWeo/zHryP+rJm//j9cx+AUAIDD2NWd7Row35HREtdZ4DnKf/w64uVm8YZXuo4hMQAAOIRdceGZUvgjGXW7zgLPUf7jYyRNbvmaWdj3BtdRDmAAACBJsqtm/amS4C5JJ7rOAs9R/uNTCgbUXrrBzO/7nusoh+IaAACyKzpfocR8Q1Kr6yzwHOVfOyOpPf61Bu0iM79vh+s4z8cKAFBwtrfrnZJuF58KwrFQ/rVriXapJbrRLOy7y3WUo2EAAArKrptZ1p6Wv5d0o+ssyADKvzaBrNpLP1Sl/3rTo2HXccbCAAAU0LNP8vuBpCtcZ0EGUP61qUSbVQqWmEX9v3EdpRZcAwAUjO298Fwp+LGk81xnQQZQ/scWmaraojvMog23uI4yHqwAAAViV3TPlbHflzTZdRZkAOU/NiOpNX5Ik5P55vJNT7iOM14MAEBB2BWdL1dgviWrFtdZkAGU/9hKwX61hTeZBRu+6jpKvRgAgAKwK7pultFnxZX+qAXlf3QjH+37lVpbrzE9q/e4jjMRDABAjlkro5VdH5b0YddZkBGU/9G1hDvUHr3azF3/M9dR0hC6DgCgMezyZaGGgi9Leo/rLMgIyn90obGaVPq2rtl4mTln+zrXcdLCCgCQQ3bV7DYlyXclLXadBRlB+Y+uEv9Bk+J5pmftw66jpI0BAMgZu7pzqgbNjyS90HUWZATlf6Q4GFJr6cNmUd/HXEdpFAYAIEfsigvPlAnvlnS+6yzICMr/eYzUHq1SHMw3C9Y/5TpNIzEAADlhV87qlA1+Juk011mQEZT/4UrhPrXHbzbz+77lOkozcCdAIAfsiu4rZO1d4gY/qBXlf5AxUkf8U+2pXGfmrx50HadZWAEAMo4b/GDcKP+DKtFmtWipWbDxPtdRmo0BAMgw29v9Gsl+Q6zmoVaU/4jQJGqPvmIWbXiL6yiuMAAAGWV7O98kmS+Ju/uhVpT/iLaoX63RfHNV33rXUVziXQOQQXZF19skfUEM8agV5S/F4ZDaw/eZBf13uI7iAw4eQMbY3q5bJH3SdQ5kSNHLf+T+/b/WtHCBmdO3y3UcXzAAABliV3a/T9Z+3HUOZEjRy78c7lJ7+Bozr/8nrqP4hgEAyAi7svMjsuZDrnMgQ4pc/oGxao9/qEr/9aZHw67j+IgBAPDcyBP9Oj8jmXe7zoIMKXL5V6LN6ggXm5esf8B1FJ9xESDgMWtltKrrf0i62XUWZEhRyz8yVbWXP20W9r3fdZQs4HHAgKeefZzvVyQV9nPKqEMRy99Iao/WaKq52Fy14Yeu42QFpwAAD9nly0Kdt+brsrrBdRZkSBHLvxTuU0f4djOv/+uuo2QNAwDgGbu6s6QBc6eMXuY6CzKkaOVvJLXGP9e+k64z1/+ffa7jZBEDAOARu7qzpEHzXUnXuc6CDCla+ZfDp1WJXmEWrr/HdZQsYwAAPEH5oy5FKv/AJGqPv2Gu7v8L11HygAEA8ADlj7oUqfxbo01qDeabuf1rXUfJCwYAwDHKH3UpSvnHwZDa4g+aheu5/XXKuA8A4BDlj7oUofwP3L9/0C4yC9fvcB0nj1gBAByh/FGXIpR/Odqt1vBGs2A9n+lvIJ4jDjhgl09v137KH+OU9/IPZTWp9P9oqO14yr/xOAUANJldPr1dm/at1Tn2ZBbhULO8l38l2qwWLTUL+u9zHaUoGACAJnqu/DfvO9l1FmRInss/NIk6ojvMwg3vdR2laBgAgCah/FGXPJd/e7RGtjTPLFz7mOsoRcT6I9AEdvn0dm3cv05P7T3puS+++gIp4CWIMeS5/GVGzvmnyyoIhhWZHYrMwyqZf9Tc/m8YoyTl/eQCRx+gwUYtf4kBAGPLdfk3URwMqTX6vo4L3mrm9O1yHccnfAoAaKDnlv2fX/7AWCj/9AwlsXYOvlqPDWyzd5/DdQaHYAAAGuS5d/6c88d4UP6NMWQjbR/4lP3JWT93HcUXDABAAxx12R8YC+XfeLuH5tkfn7XSdQwfMAAAKaP8URfKv3n2DF3ESgADAJAqzvmjLpR/8+0ZmmfvPucdrmO4xAAApIRz/qgL5e+GlbR76NP2R5e2uo7iCgMAkALe+aMulL9bw0msaPuXXcdwhQEAmCDe+aMulL8f9lavdx3BFQYAYAK44A91ofz9MVQt2bvPeb3rGC4wAAB1YtkfdaH8/VO1N7iO4AIPAwLqcPCd/z7KH7Wj/P00mHS5juACAwAwTgff+VP+GAfK319JMsV1BBcYAIBx4J0/6kL5+61qY9cRXGAAAGrEO3/UhfKHpxgAgBrwzh91ofyzIQiGXUdwgQEAOAbe+aMulH92RGaH6wguMAAAY+CdP+pC+WdLFPS5juACAwBwFLzzR10o/+yJzDdcR3CBAQAYBe/8URfKP3viYFil9V9zHcMFBgDgeXjnj7pQ/tlUif/F9IiLAIGi450/6kL5Z1NoErUPv9V1DFd4FgDwLO7tj7pQ/tnVFt9pLt/0hOsYrjAAADqk/HmkL8aD8s+uUjCgSvJG1zFcYgBA4VH+qAvln22t0W2mZ2Oh/wIZAFBodnVnSRsof4wT5Z9tLeF2s7D/I65juMYAgMKyqztLGjTf1bb9lD9qR/lnm5HUFt7kOoYPGABQSM+Vv3Sd6yzIEMo/+1qjtWZe/3dcx/ABAwAKh/JHXSj/7DOSSrrRdQxfMACgUCh/1IXyz4f2+Fdmwcb7XMfwBQMACoPyR10o/3wITaKO5NWuY/iEAQCFQPmjLpR/frRF3yryTX9GwwCA3KP8URfKPz/iYEAV+xbXMXzDAIBco/xRF8o/XzpKHyn6TX9GwwCA3KL8URfKP18q0XYzv+821zF8xACAXKL8URfKP2eM1BoX+n7/Y2EAQO5Q/qgL5Z8/rdEjZt66/+k6hq8i1wGANI2Uf/A9yV7rOgsyhPLPn8BYhdGrXMfwGQMAcuPgO3/KH+NA+edTe/xjc/W6la5j+IxTAMgFlv1RF8o/n+JgQNXjePd/DKwAIPMof9SF8s+vjtJHzPwH9rqO4TsGAGQa5V8gQ8PStt3S3v3SUFUaGpKCQCpFUimWJrdJk1olY469Lco/vyrxo3zsrzYMAMgsyr8ArKStO6XHt0p79o38eixRKB0/STptutRSGv17KP/8MkZqSVj6rxEDADKJ8i+A7XukjU9Kz4yjrIer0pPbpad2SCdNlU4/QYrDg79P+edbR/xTs6D/XtcxsoIBAJlD+eedlTZslh7bWv8mEis9vk3atku64Aypo0L5510UDGlqwLv/cWAAQKZQ/jmXWOmRR0eKOw0DQ9JDG6Spx0s6yikB5EN7/FEzpy+lfzjFwMcAkRmUf84lVnr49+mV/wHbJD2wTdrJReG5VYkeNwvXf9R1jKxhAEAmUP45d+Cd/9O7093ujkDaaUYuHuzfOfJJAuSLkdRaeqXrGFnEAADvUf45l/ay/wEHyv+AqqTfb093H3Cvo/SvZt7af3cdI4sYAOA1yj/nmlX+B2wflvYNpLsvuBMHQxpIXuE6RlYxAMBblH/ONeqc/9HK/4A/7Ex3f3CnNbrNvHTjDtcxsooBAF6i/HOu0ef8x7K7KiXp7hYOtIZPmkX9t7qOkWUMAPDOwUf6Uv651Oxl/yP2L2nXM+nuG81lJLXEfOZ/ghgA4BUe6Ztzrpb9j/j+fenuH83VHv/CzO/7lesYWccAAG84W/YfR2/kYr+uuFz2f74hzgFkVhzsVzKV1cEUcCdAeMHpOf8wkKrV5u+zlqfW5YXrZf/nG2YAyCQjaVL8DjOPR/2mgRUAOOf8gr8WB3Nwa4Fm78RKD3tU/tKxnyoIP7XFD5h56//BdYy8YACAU87LX5KOKzd/n5MLcl/655b9PSp/SYo49GVOHAzreC12HSNPeBXAGS/KX5JOaXOwz/bm77PZfFv2PxQDQPZ0lD5s5mzY7DpGnvAqgBPelL8kndbR3PPxRtKpOR8AfFz2P1SRTsHkQVu03szvu811jLxhAEDTeVX+klQKm7sKcGKb1Bo3b3/N5uuy/6Gm5XwAy5PQJGovXeM6Rh4xAKCpvCv/Ay46oTmrAEbSRdMbvx9XfH/nL0ktkmJWADKjo/RF07P2Ydcx8ih0HQDF4W35S1IlkvYMStsb/KCYMydJF0xt7D5cycI7f2lktafNwYWfGL9KtMVcs+ElrmPkFSsAaAqvy/+AF5wkTW5gMbSVpD8+sXHbd8nnC/4OVZZ0wqT0tofGCYzUHvOkvwZiAEDDZaL8JSkOpMtPHbkmoBHbvuI0qZzDpecsLPtLI6dfTqP8M6M9/r65at2/uY6RZwwAaKjMPdhnUll6yRkjpwTSUomknjPc3G+g0Q6Uv+/L/pI0NZaOc/CRT4xfOdijE/pf4zpG3jEAoGHs8mWhBsw/Ze7BPtNapIUzRv53oqaWR7Y1vTLxbfkmS+XfEUhnHZ/uNtEYRlKl9DrzAg25jpJ3BboZOZrJLl8Wauaab8vola6z1M1aqW+H9Nut0r7h8f1sKZRmTZUumCaFOXyZZeWcvyS1Gun8E0aevwD/dcS/Mos3XOk6RhHk8MgE16xVoFVd/yirG1xnScVwIm3YKT26W9q8d6T8RmOMdGKrdFq7dPaUkfP+eUT5o1FK4T4d136C6Vm9x3WUImAAQKqsldGqrn+Q1RtcZ2mIoaq0bb+0e1AafPYJgqVQai+NnDJoxAWEPqH80ShG0rTyS83c9T90HaUoGACQKtvb9SlJ73WdAw1A+aOROuK7zOIN2bhYOCd4dSA1trfrFlH++UT5o5HK4S61buAz/03GKwSpsL3dr5X0Cdc50ACUPxoplFWrFpkejfNKW0wUrxJMmO3tvlqyXxenlPKH8kejdZS/ahZsutd1jCLigI0JsStnXSIb/JskHq+WN5Q/Gq0SPmmWbjrZdYyi4tWCutkV55+iJLhLlH/+UP5otNAkammd5zpGkfGKQV3s6s52mfgnMjrddRakjPJHM7RHt5sFax5yHaPIeNVg3OzyZaEGzT9Luth1FqSM8kcztEbrzKINt7iOUXS8cjB+5675mKTFrmMgZZQ/miE2wzKlHtcxIOXw2aRoJLuy62WyfNY/dyh/NIOR1BbfYhaufcx1FPApAIyDfaBrtgLdK4lnquYJ5Y9m6Yh/YxZv+BPXMTCCVxFqYu+7YJoC/VCUf75Q/miWUjCgQTvfdQwcxCsJx2StApXjb0k6y3UWpIjyR7MYSe2lG8xLN+5wHQUH8WrCsa3q/GtZu9B1DKSI8kczTSrdaeb3fc91DByOawAwJrui+woZ+6+Scv6c2wKh/NFMlehxs3Tjqa5j4Ei8qnBUdtXsE2T0HVH++UH5o5kiU1V7dLnrGBgdryyMyloFSpJvS/YU11mQEsofTWWkSfFN5qq+9a6TYHS8ujC63q53S5rrOgZSQvmj2TqiX5j5/V9yHQNHxzUAOIJd0XmRjLlPUtl1FqSA8keztYRPa/KmE02Phl1HwdHxKsNh7LqZZRnzT6L884HyR7OFJlFcuory9x+3Asbhnmn5pKTZrmMgBZQ/ms5Ik+L3mgXrVrpOgmPjFACeY3u7rpT0/4p/F9lH+cOFjvjnZvGGBa5joDa84iBJsvdf2irpH0T5Zx/lDxcq0Ra1buApoRnCqw4jooGPS5rpOgYmiPKHC5Gpqi14Mef9s4VXHmR7u14oq7e7zoEJovzhgtHI5/3n9q91HQXjw3Jvwdl1M8vaU35QMue5zoIJoPzhyqTS983V/ctcx8D48SmAotvT8gFJlH+WUf5wpRJtpPyzi1dhgdkHOmfK6H2uc2ACKH+4Ugr3aVLpj13HQP14JRZZYP5OVi2uY6BOlD9cCY1Ve7zI9Kzd6joK6sersaBsb/drxL3+s4vyhytGUnvpv5r5fb9yHQUTw0WABWRXd7ZrMHiEJ/1lFOUPlzriX5jFG+a7joGJ41VZRIPmA5R/RlH+cKk1elxXb1joOgbSwSuzYOyD3WfL6D2uc6AOlD9cioMBmdKfGKPEdRSkg48BFk01uV0yXPiXNZQ/XAqMVVu8yCxc+5jrKEgPr9ACsas6XyKZpa5zYJwof7hkJHWU3mUWrr/HdRSki1dpQVgroyS4zXUOjBPlD9cmlb5tFq3/nOsYSB+fAigIu7LrlbL6Z9c5MA6UP1xrix80SzZc5DoGGoNXawHYcS0whwAAGWhJREFU+y+NZfVR1zkwDpQ/XGsJn1a7/VPXMdA4vGKLINz/Zknnuo6BGlH+cK0UDKjS8gLTs3G/6yhoHE4B5Jy997KKKrvXSzrZdRbUgPKHa6FJNKV8lZnX90vXUdBYvHLzrrLrLaL8s4Hyh2tG0pTSWyn/YmAFIMfsPTNaNKW9T9KprrPgGCh/+GBy6QtmUf9NrmOgOXgF59lxbW8T5e8/yh8+aI/vpvyLhRWAnOLcf0ZQ/vBBa/yIuXbDBa5joLl4JedVZddfiPL3G+UPH1Sip9RhL3YdA83HqzmH7PJloWTe5ToHxkD5wwfl4Bm1hN183K+YeEXn0XlrXiFppusYOArKHz6IgyGVS39iFqx/ynUUuMHTAPPpFtcBcBSUP3wQmkTt4WKzoO93rqPAHV7ZOWNXdb5EVpe6zoFRUP7wQWCspsQ3mAUbfuE6Ctzi1Z03SfBO1xEwCsofPjCSJpXeb+b1f8d1FLjHxwBzxPZePEMa7pMUus6CQ1D+8IKRJsd3mEX973GdBH7gVZ4nduhmUf5+ofzhi0nRNyh/HIoVgJyw91/aqnDgUUlTXWfBsyh/+GJS6Ufm6v5rXceAX3i150U0+DpR/v6g/OGLSfEvKX+Mhld8btg3u06AZ1H+8EV7vMpcvaHHdQz4iVd9DtgHumbz0T9PUP7wRVu0Vm0bXuA6BvzFKz8PjH2T6wgQ5Q9/VKL1at/YaXo07DoK/MWdADPO3jOjRca81nWOwqP84YtK/KgGWmdR/jgWBoCsm9LxMske5zpGoVH+8EUl/IPi8FyzdPWg6yjwH0eBrLP2RtcRCo3yhy8q4RMKjj/fXN034DoKsoH7AGSYXTX7BCXJY2Ilxw3KH75oDZ9UR/u5pmf1HtdRkB0UR5ZVk1fK8HfoBOUPX1SiLTohOt/MofwxPhwRsoyL/9yg/OGLSrRFJ0YzzZy+lP8xogg4BZBR9v6ucxRqnfg7bC7KH76oRJs1rXyuefEju11HQTaxfJxVgVkmWcq/mSh/+GLknf95Zg7lj/pxdMgqY1/qOkKhUP7wBcv+SAnvIDPIrrzoVNnqo+Lvrzkof/iC8keKOEpkUvJSUf7NQfnDF5Q/UsaRIosSsfzfDJQ/fDFywd85lD/SxLvIjLG9F0+Rhp+SFLvOkmuUP3zBO380CEeMzKkuFuXfWJQ/fEH5o4E4amSNtUtcR8g1yh++oPzRYJwCyBB7/6WxwoGnJE1xnSWXKH/4gvJHE3D0yJJg8ApR/o1B+cMXlD+ahCNIlgQs/zcE5Q9fUP5oIo4iWWLFAJA2yh++oPzRZBxJMsI+2N0t6SzXOXKF8ocvKH84wNEkK6r2WtcRcoXyhy8ofzjCESUzDMv/aaH84QvKHw7xMcAMsKtmn6AkeUIMbBNH+cMXlD8c48iSBUn1WvF3NXGUP3xB+cMDHF0yIWD5f6Iof/iC8ocnOAXgOXvvZRVVdm+R1OY6S2ZR/vAF5Q+PcJTxXduuuaL860f5wxeUPzzDkcZ3Ccv/daP84QvKHx7iaOMxa2Uke7XrHJlE+cMXlD88xRHHZ6s6/1jSqa5jZA7lD19Q/vAYRx2fsfw/fpQ/fEH5w3MceXxmePrfuFD+8AXljwzgY4Cesvd3nqHQbBR/R7Wh/OELyh8ZwRHIV4FZKsq/NpQ/fEH5I0M4CvnKiOX/WlD+8AXlj4zhHaaH7OrOdg2arZLKrrN4jfKHLyh/ZBBHIx8NmatF+Y+N8ocvKH9kFEckH1mW/8dE+cMXlD8yjKOSZ+zyZaGkha5zeIvyhy8of2QcRybfzHz4xZKOdx3DS5Q/fEH5Iwc4Ovkm4OY/o6L84QvKHznBEco3lgHgCJQ/fEH5I0c4SnnE3t99gWTOc53DK5Q/fEH5I2c4Uvkk5N3/YSh/+ILyRw5xtPIJy/8HUf7wBeWPnOJOgJ6w910wTaXoSUmR6yzOUf7wBeWPHKNsfBGHi8XfB+XfbNaquq+qZH9VNkmkxHUgf0TTW54OKH/kGIXjCxMskazrFG5R/k1hhxMNbtmnwa37NfT0ftlqwf/djaI0vTJQOr58PuWPPOMUgAfsupll7WnZIqnDdRZnKP+Gs1Wr/Y/t0b5Nu2WHeKt/NKXjWwbNxVNO67j+yS2uswCNxAqAD54pXynKn/JvoOGdg9r90DYlA1XXUbxWml4Z6Og87jRz/eNbXWcBGo0BwAe2wMv/lH/DDWzeq2fWbJdNCvpvrEal41sGzUWTT6f8URQMAF5IFhfybAzl33ADjz+jPQ9vdx3De7zzRxExADhmV866RNbMcJ2j6Sj/hhveMaBn1u5wHcN7vPNHUTEAuJaES2QKtjRL+TecHUq0+6FtLPsfA+/8UWQMAK6Zgt39j/Jvin2/361kkCv9x8I7fxQdA4BDdsX5p0i61HWOpqH8myIZqGr/o3tcx/Aa7/wBBgC3gtISWVuMq/8o/6YZeHIvS/9j4J0/MCKbR7i8KMrDfyj/phrcus91BG9xkx/gIFYAHLH3X9oqDfS4ztFwlH9TJUOJhncOuo7hJZb9gcMxALgSDs6X1Oo6RkNR/k1X3T3kOoKXWPYHjsQA4Iq1S3J97x/K34lkYNh1BO/wzh8YXfaPeBlkrQIFutp1joah/J3hyX6He678X0P5A8/HCoALvd1/KmNPch2jISh/t4I8LyuND8v+wNgYAFzI681/LOXvWhDn67+nXiz7A8fG0cIJc63rBKmzVnqY8nctbGWmZ9kfqE3+joCesw92ny3ZTtc5UkX5eyNsjRWUQ9cxnHlu2Z/yB44pn0dBn1WTfL37p/z9YqTS8RXXKZzgJj/A+OT4SOgpG+Tn/D/l76XSicUbAErTKwMdXVNPpfyB2uX/aOgRe/+lk2Xsn7nOkQrK31vxlLLiqWXXMZqGZX+gPsU4Ivoi2H+1pNh1jAmj/L3XOnOK6whNwbI/UL9iHRVdMzlY/qf8MyFqj1U5s8N1jIZi2R+YmOIdGR2x91wZSXah6xwTQvlnSus5k3N7QSDL/sDEFffo2GxTt1wu6TjXMepG+WdS+6ypubsegHf+QDoKedeQ7W/QmdVI1yrRC0ygs+zBp/JtlVWfsbqnGuvuE76oPantNAmWSBm9Tzvln1kmMpp00XTtXb9T+36/23WcCeP2vkB6CnPjcLtM4dNT9efW6u2SLqnhR/bL6m4b6G+mf1n3T3j/vV3rJM2c6HaajvLPjcGt+7V3/U5Vn8nmI4O5wx+QrkIMANveooXW6jOSZtXx49ZKy4NIt0z7oh6tZ/925axO2eChen7WKco/f6w08OQzGnhir4Z2DmRmUYryB9KX6wHASmbbW/RXsrpNE7zewUpbFWjZ9C/pl+P+2d6uD0i6bSL7bzrKP/fsUKLBbftVfWZIyUBVNvFzGghao31tMzrOoPyBdOV2ALDLFD49Rd+0Rq9OcbOD1ujPp39Zd44rS2/XvZIuSzFHY1H+8EUl2qITo5lmTl/K/xgB5PaouXWKPply+UtSyVh9Y8ubdEWtP2BXzT5B0p+mnKNxKH/4gvIHGiqXR86tb9brjdF7GrT52Bgt3/afdXpN322Ta5SVP2fKH76g/IGGy93Rc8fbdJyk2xu8mxOSYX2qpu+0uqbBWdJB+cMXlehxTWo7m/IHGit3R9Bqor+WNLXR+zHS9dveqDljfY9dN7MsaV6js0wY5Q9ftEa/VzDtXNOzOr17cAAYVa6OojvepuOs1U1N2p2xRu8f8zv2tMyV1N6cOHWi/OGL1mijOnS+WfLAXtdRgCLI1ZF0ONFiSS1N26HRwi1/oaM/ccV4vvxP+cMXraXfqWPjuaZn437XUYCiyNfRNNHSJu+xHISaP9pvWCvj9fl/yh++aI9XaUl/t+nRsOsoQJHk64hqav94Xlqs0ZWj/kZv16WSTmtqmFpR/vBFR+nH5poNFxujxHUUoGhyc1R99ur/6U3fsdG5o349sEuanKQ2lD98YCRNKX/eLO7383UCFEBujqwD1cZf+T8qq2mjfz3w78BG+cMHoawmtfy1Wbj+ZtdRgCLLzeOAI6sW6+bGxpXnf8H+tut0DduLXYQ5KsofPohMVW3hDWZR37hupw0gfbkZALwybK+VjD/PWaD84YNSuE+V8AqzqP83rqMAYABoDGuWePOYJcofPmiNHldH6SLTs5Yn+gGeYABImV3d2a4hXeHFc9Ypf/igI/61Wjf8GR/zA/zCAJC2AS2UaeLNiI6G8odrgbHqiD5jFm24xXUUAEdiAEibMe6v/qf84VocDGlyy/Vm7tofuo4CYHQcdVNkly8LJV3tNgTlD8cq0VOa3HIB5Q/4jRWANJ3/yAuV6Hhn+6f84ZSROqJfqXXDXM73A/5jAEhTkrhb/qf84VJkquoov8Ms6Pui6ygAasMAkC43D/+h/OFSJdqijvKfmZc88ojrKABqxwCQEvtA50xJFzZ/x5Q/HDGSOko/VaX/Wpb8gexhAEhLYK5r+j4pf7hSCgbUUnqdubrv+66jAKgPA0B6mrv8T/nDBSOpPf6NpoVzzZy+lP/xAWgmBoAU2NWdUzWoFzVvh5Q/HIiDIbXH7zUL1n/OdRQAE8cAkIYBs1imSX+WlD+azUhqi9YoDq80C9Y/5ToOgHQwAKTBNGn5n/JHs8XBgNpKN5mFfV9xHQVAuhgAJiowRtL8hu+H8kczjZzr/5Wmhddyrh/IJwaACYrP7GiTNKWhO6H80Uwt4Q61R682c9f/zHUUAI3DADBBpRkdHQ3dAeWPZolMVW2lL5hF69/pOgqAxmMAmKDS6e3tDds45Y9mGFnu/7U6kpeZy9c/4ToOgOZgAJiAcFqLgra41JCNU/5ohkq0We3x9eaqdf/mOgqA5mIAmIDSjAat/lP+aLRytFut0ft5eA9QXAwAE1CaMSn9jVL+aKQ4HFRr+AUt7H+vMUpcxwHgDgNAnYJKpGh6Jd2NUv5olMhU1Rp9WxX7FtPTv991HADuMQDUqXRWx8jFU2mh/NEIkamqNf5fGkj+wly9YYfrOAD8wQBQp/jMFJf/KX+k7bDi76f4ARyBAaAOJgoUn9aWzsYof6QpDgdVCe5UpfUm07N6j+s4APzFAFCH+LR2mSiFEqT8kZZyuFctwbe0u/Vmc/XqQddxAPiPAaAOqXz8j/LHhBmpEj6ulvDjZsH6v3WdBkC2MACMl5HiiQ4AlD8mIpBVa/ygyvFNZt7af3cdB0A2MQCMU3RCRUFlAn9slD/qVY52qxJ9T/uG/9JcwxX9ACaGAWCcJnTzH8of4xUYq9bwYZWiD5v5fd9zHQdAfjAAjFPpzDqX/yl/1MpIaok2qxzcqSnBh82cvpT/0QAAA8C4BB2xwmkt4/9Byh+1KAV71RLdLQUfNFf3/c51HAD5xgAwDqV6bv5D+eNojKRStFvl4JcKqx83Czbd6zoSgOJgABiH0lnjXP6n/HEEI7UET6sU/UKx+YSZ19frOhGAYmIAqJEphYpPHsfd/yh/HBAYqRxuVin4hWzwMZb3AfiAAaBG8RntUlhj8VL+iM2wyuE6xeYHKrV+gtvyAvANA0CNar76n/IvJiMpDvaqHP5GcfgVzev7jjFKXMcCgKNhAKiFMbUNAJR/sRhJ5ehplYJfKQ4+yvl8AFnCAFCD+ORWmXI49jdR/sUQmkQt4UZFwV06zn7CzNmw2XUkAKgHA0ANjvnwH8o/3+JgQC1hr6Lwmyr1/b3p0bDrSAAwUQwANYjHuv0v5Z9DRmoJd6kU/Iei4LNmft/PXScCgLQxABxDeFxZ4eTS6L9J+edHaKxK0WMq6V8UtP2NWfDQo64jAUAjMQAcw1Ef/kP5Z18cDKkc/k5R8B0NTfm8WfLAXteRAKBZGACOYdTz/5R/RhmpZJ77qJ6Z3/ct14kAwBUGgDEElUjRiZXDv0j5Z4sxUsuzd+FT/Cmz6JEHXUcCAB8wAIwhPrNjpEAOoPyzIQ6GVQ5G7sI3OfwUj9MFgCMxAIzhsJv/UP5+O/SjevP7vsRd+ABgbAwAR2FCo/i09pFfUP7+OfQufEYfM4v6f+M6EgBkCQPAUUSntsuUAsrfJ4feha+t+ilz+cYnXEcCgKxiADiK0owOyt8Hh35Ur1z9nOnZuN91JADIAwaA0RipdEY75e/EIXfhM/q8WdT/L64TAUAeMQCMIppeUfCHJyn/ZgmMVA43q2TuUqnlNnPVmk2uIwFA3jEAPJ+R2k9JKP9Gi8ywWsKRj+qVWj9helbvcR0JAIqEAeBQRuo4QwqrA+lul/IfuWo/DrgLHwB4ggHggGfLvzTGg//qUuTyN5JaopG78EXB7WZeX6/rSACAEQwAEuWfppGP6vUpCn6g4f23myUbt7qOBAA4EgMA5T9x3IUPADKn2AMA5V8nI5WD7SoH/1uh/YxZsPE+14kAAONT3AGA8h+fwFiVo8dU0r9oOP6IWbL2MXdhAAATVcwBgPKvTRQMqSV8UJH9lp6Y8SVz/S+5Cx8A5ETxBgDKfwyH3IUvDP7OLOj70cHf29ikDACAZijWAED5HykwVuXwCYXBz9Qaf9K85JFHGrtDAIAPUm4td7a9SZ3W6KGjfgPl/xwbBhoerCbPPLa3uuOhnUPJ/hQu2g+1NzB6IpTuHm7Vp8/+ijZPfKMAgEYpxgBA+csGRvt3Dmln3x7t7t8j2VQ3f4Qw0pNRrL8685v6ZmP3BACoR/4HgKKWv5GqCrRv24Ce/u0ODWxJ+fbGNYoj/T6q6PrTvy4+KggAHsn3AFC08g+Mhoas9vxhr7Y/tFPVfdX08k1AYJTEJf3lmd/WZ11nAQCMyO9FgAUpfxsaDe5LtKtvj3as2dnwpf16JFbBwIDu2PganTPjO7rZdR4AQF4HgFyXv1FipH1PD2rHml3a+/i+dPM00NCgbnr0Bq07/Zv6nOssAFB0+TsFkMfyD4yGq9IzT+7T0w/u1PDuoXRzNFEQKCm36YVcEwAAbuVrBSBH5W8Do8H9Ve3a8Ix2/W63kmo+nq+TJAqG92m5pDNdZwGAIsvNABC0KGo9Kcvlb5QE0r4dQ9q5ZpeeeXRvuvv0yNCwznj01Xrj6XfqK66zAEBR5eIUgP2yYu3TTxXqqlQ33OjyN0ZVSXufGtD2h3ZqYJubj+q5EEZ68px/1smucwBAUWV+ALBfVqxBLZd0XaobblT5zzpRg8PS7o17tWPNTiUD+VjaHzcjlco6Zca39ITrKABQRJk+BZCl8retRk+bNj39Px+TCtr5h7FSkOg9km5xHQUAisjhA+YnJkvlXw2t+h8Z1tOrd1L+h0is5rvOAABFlckBIGvlv3FjosSPm/J5pSqd4joDABRV5gYAyj8/jFXFdQYAKKpMDQCUf75Ym61/fwCQJ5k5AFP++WOMBl1nAICiysQAQPnnkzHa6joDABSV9wMA5Z9fQagVrjMAQFF5PQBQ/jkX8FRAAHDF2zsBUv75Fobae8531eY6BwAUlZcrAJR//oWx7nSdAQCKzLsVAMo//8JQ+89ONNl8j08BAIArXq0AUP7FUIp1K+UPAG55swJA+RdDqax/nfFtzXWdAwCKzosBgPIvhjjWphl36mzDI5EAwDnnpwAo/2IoRVqjsi6g/AHAD05XACj//DNGtlzW35/xLb3VdRYAwEHOBgDKP//iWKvKRktP+Y42uc4CADickwGA8s+nIFAShHosMLqrJH2a4gcAf0XN3mGWyt+W7K7tTyR/WY60v/l/UpmRKNBjQaT+U7+uR12HAQDUpqm1lqXyV8luMaVk5vSva1e6GwYAwL2mnQLIWvmrlMw0t1L+AIB8asoAQPkDAOCXhg8AlD8AAP5p6ABA+QMA4KeGDQCUPwAA/mrIAED5AwDgt9QHAMofAAD/pdqolD8AANmQWqtS/gAAZEcqzUr5AwCQLRNuV8ofAIDsmVDDUv4AAGRT3S1L+QMAkF11NS3lDwBAto27bSl/AACyb1yNS/kDAJAPNbcu5Q8AQH7U1LyUPwAA+XLM9qX8AQDInzEbmPIHACCfjtrClD8AAPk1ahNT/gAA5NsRbUz5AwCQf8Ghv7DLFWpQ31U2yn+zhpNzKH8AAMbvsAFAT+kLkl6a6h4aV/7nmk9qd7obBgCgGJ5rZvt5vUpWd6a6dcofAAAvGUmyX1eL9midpNNS2zLn/AEA8NbIKYDdulmUPwAAhWHsrYo0TY9Lmp7KFln2BwDAe4Gm6cXyu/y3qJScR/kDAJCeQNLiVLbEsj8AAJkRyWpO7Q8FPopGLvvfxjt/AADSFsjo5AltgWV/AAAyJ5B0Ut0/zbI/AACZFEiydf0k5Q8AQGYFkp4c909R/gAAZFog6Ylx/QQP9gEAIPMCSf+n5u/mgj8AAHIhkNFPavpOlv0BAMiNQFt1r6Snxvwulv0BAMiVwNyqYUmfOup3sOwPAEDujDwNsF2fl/ToEb/Lsj8AALkUSJL5T9ovo/ce9jss+wMAkFvBgf9jbtJyWf2dJB7pCwBAzgWH/eok3azd5r7Uy7/FPq5SMpPyBwDAD4cNAOZ6VTVoL1eLXZ3aHir2t4qSs8yt2pPaNgEAwIQc9a2+/W/BZ/WMuUmJwrq2HKqqVvs58+HkPXWnAwAADTHmWr+9Q1O03fyTBoLFqj7vdMHRhErUkvxYU+zrzbu1I5WUAAAgVTWd7Le3qqQweJOGzA0athfImoqGVZIkRRqUsfsUmTWK7DeVJF8xt2qwoakBAMCE/P/FgYFGTMum2wAAAABJRU5ErkJggg=='

window = sg.Window('NPUST-Servitor-Auto-Sign-In', layout, icon = iconBase64)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

    if event == 'Exit':
        try:
            browser.quit()
        except:
            pass
        window.close()
    
    if event == '登入':
        try:
            browser = webdriver.Chrome("./chromedriver")
            browser.get('https://www.npust.edu.tw/login.aspx?url=http://osas.npust.edu.tw/alltop/login.php')
        except:
            sg.Popup('啟動網頁出現了問題！請確認是否有安裝正確的ChromeDrive！', title='System Message', keep_on_top=True)

    if event == '登入檢查':
        try:
            browser.switch_to.frame("Menu")
            Select(browser.find_element(By.CLASS_NAME , 'form_combo')).select_by_value("BC")
            browser.switch_to.default_content()
            browser.switch_to.frame("MenuFrame")
            browser.find_element(By.ID , 'menu10').click()
            browser.find_element(By.ID , 'submenu10.3').click()
            browser.switch_to.default_content()
            browser.switch_to.frame("main")
        except:
            sg.Popup('您似乎沒登入成功！詳情請看github教學！', title='System Message', keep_on_top=True)

    if event == '開始自動填入':
        if(values['WeekDropDown'] == "") :
            sg.Popup('尚未選擇周日期！請選擇周日期後再進行此操作。', title='System Message', keep_on_top=True)
        else:
            try:
                for item in weekEnglishList:
                    weekResult[f'{str(item) + "Am"}'] = AmPermutations.get(amCheckTime(values, item))
                    weekResult[f'{str(item) + "Pm"}'] = PmPermutations.get(pmCheckTime(values, item))
                    print(weekResult[f'{str(item) + "Pm"}'], weekResult[f'{str(item) + "Am"}'])
                if (values['WeekDropDown'] ==  "1-7號"):
                    for day in range(1,8):
                        if (datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday() == 6 or datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday() == 7):
                            continue
                        else:
                            fillIn(browser, datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday(), day)
                    sg.Popup('新增完畢！', title='System Message', keep_on_top=True)
                elif (values['WeekDropDown'] ==  "8-14號"):
                    for day in range(8,15):
                        if (datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday() == 6 or datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday() == 7):
                            continue
                        else:
                            fillIn(browser, datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday(), day)
                    sg.Popup('新增完畢！', title='System Message', keep_on_top=True)
                elif (values['WeekDropDown'] ==  "15-21號"):
                    for day in range(15,22):
                        if (datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday() == 6 or datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday() == 7):
                            continue
                        else:
                            fillIn(browser, datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday(), day)
                    sg.Popup('新增完畢！', title='System Message', keep_on_top=True)
                elif (values['WeekDropDown'] ==  "22-28號"):
                    for day in range(22,29):
                        if (datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday() == 6 or datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday() == 7):
                            continue
                        else:
                            fillIn(browser, datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday(), day)
                    sg.Popup('新增完畢！', title='System Message', keep_on_top=True)
                elif (values['WeekDropDown'] ==  "29-30號"):
                    for day in range(29,31):
                        if (datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday() == 6 or datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday() == 7):
                            continue
                        else:
                            fillIn(browser, datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday(), day)
                    sg.Popup('新增完畢！', title='System Message', keep_on_top=True)
                elif (values['WeekDropDown'] ==  "29-31號"):
                    for day in range(29,32):
                        if (datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday() == 6 or datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday() == 7):
                            continue
                        else:
                            fillIn(browser, datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday(), day)
                    sg.Popup('新增完畢！', title='System Message', keep_on_top=True)
                elif (values['WeekDropDown'] ==  "29號"):
                    for day in range(29,30):
                        if (datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday() == 6 or datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday() == 7):
                            continue
                        else:
                            fillIn(browser, datetime.datetime.strptime(str(CE) + str(cn_number.get(values['MonthDropDown'].split('月')[0], "normal")) + str(day),"%Y%m%d").isoweekday(), day)
                    sg.Popup('新增完畢！', title='System Message', keep_on_top=True)
            except:
                sg.Popup('似乎出現了點問題，請至github回報', title='System Message', keep_on_top=True)

    if event == 'MonthDropDown':
        if leap:
            if dayKeyValue_CE.get(values['MonthDropDown']) == True:
                window.Element('WeekDropDown').update(values=['1-7號', '8-14號', '15-21號', '22-28號', '29-31號'])
            elif dayKeyValue_CE.get(values['MonthDropDown']) == False:
                window.Element('WeekDropDown').update(values=['1-7號', '8-14號', '15-21號', '22-28號', '29-30號'])
            elif dayKeyValue_CE.get(values['MonthDropDown']) == 2:
                window.Element('WeekDropDown').update(values=['1-7號', '8-14號', '15-21號', '22-28號', '29號'])
        else:
            if dayKeyValue_nonleap.get(values['MonthDropDown']) == True:
                window.Element('WeekDropDown').update(values=['1-7號', '8-14號', '15-21號', '22-28號', '29-31號'])
            elif dayKeyValue_nonleap.get(values['MonthDropDown']) == False:
                window.Element('WeekDropDown').update(values=['1-7號', '8-14號', '15-21號', '22-28號', '29-30號'])
            elif dayKeyValue_nonleap.get(values['MonthDropDown']) == 2:
                window.Element('WeekDropDown').update(values=['1-7號', '8-14號', '15-21號', '22-28號'])

window.close()