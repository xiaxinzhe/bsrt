import os,time,math
#-------------------------------------#
class Calendar(object):
    def __init__(self):
        self.__monthList = [
        {"name": 'January',   "numdays": 31},
        {"name": 'February',  "numdays": 28},
        {"name": 'March',     "numdays": 31},
        {"name": 'April',     "numdays": 30},
        {"name": 'May',       "numdays": 31},
        {"name": 'June',      "numdays": 30},
        {"name": 'July',      "numdays": 31},
        {"name": 'August',    "numdays": 31},
        {"name": 'September', "numdays": 30},
        {"name": 'October',   "numdays": 31},
        {"name": 'November',  "numdays": 30},
        {"name": 'December',  "numdays": 31}
        ]
    def getTimeLocal(self,hr=int(time.strftime("%H",time.localtime())),mn=int(time.strftime("%M",time.localtime())),sc=int(time.strftime("%S",time.localtime())),docpm=False,docdst=False,stamp=0):
        if(stamp==0):
            dochr=hr
            docmn=mn
            docsc=sc
        else:
            dochr=int(time.strftime("%H",time.localtime(stamp)))
            docmn=int(time.strftime("%M",time.localtime(stamp)))
            docsc=int(time.strftime("%S",time.localtime(stamp)))
        if((docpm) and (dochr < 12)):
            dochr += 12
        if(docdst):
            dochr -= 1
        mins = dochr * 60 + docmn + docsc/60.0
        return mins
    def isLeapYear(self,yr):
        return ((yr % 4 == 0 and yr % 100 != 0)or yr % 400 == 0)
    def getJD(self,month=0,day=0,year=0,stamp=0):
        if(stamp==0):
            TimeStamp=time.time()
        else:
            TimeStamp=stamp
        if((month==0 or day==0 or year==0) or (month > 12 or day > 31 or (month==2 and day > 29))):
            docmonth=int(time.strftime("%m",time.localtime(TimeStamp)))
            docday=int(time.strftime("%d",time.localtime(TimeStamp)))
            docyear=int(time.strftime("%Y",time.localtime(TimeStamp)))
        else:
            docmonth=month
            docday=day
            docyear=year
        if((self.isLeapYear(docyear)) and (docmonth == 2)):
            if(docday > 29):
                docday = 29
        else:
            if(docday > self.__monthList[docmonth-1]['numdays']):
                docday = self.__monthList[docmonth-1]['numdays']
        if(docmonth <= 2):
            docyear -= 1
            docmonth += 12
        A = math.floor(docyear/100)
        B = 2 - A + math.floor(A/4)
        JD = math.floor(365.25*(docyear + 4716)) + math.floor(30.6001*(docmonth+1)) + docday + B - 1524.5
        return JD
    def calcTimeJulianCent(self,jd):
        T = (jd - 2451545.0)/36525.0
        return T
    def calcMeanObliquityOfEcliptic(self,t):
        seconds = 21.448 - t*(46.8150 + t*(0.00059 - t*(0.001813)))
        e0 = 23.0 + (26.0 + (seconds/60.0))/60.0
        return e0
    def calcObliquityCorrection(self,t):
        e0 = self.calcMeanObliquityOfEcliptic(t)
        omega = 125.04 - 1934.136 * t
        e = e0 + 0.00256 * math.cos(math.radians(omega))
        return e
    def calcSunApparentLong(self,t):
        o = self.calcSuntrueLong(t)
        omega = 125.04 - 1934.136 * t
        Lambda = o - 0.00569 - 0.00478 * math.sin(math.radians(omega))
        return Lambda
    def calcSuntrueLong(self,t):
        l0 = self.calcGeomMeanLongSun(t)
        c = self.calcSunEqOfCenter(t)
        O = l0 + c
        return O
    def calcGeomMeanLongSun(self,t):
        L0 = 280.46646 + t * (36000.76983 + t*(0.0003032))
        while(L0 > 360.0):
            L0 -= 360.0
        while(L0 < 0.0):
            L0 += 360.0
        return L0
    def calcSunEqOfCenter(self,t):
        m = self.calcGeomMeanAnomalySun(t)
        mrad = math.radians(m)
        sinm = math.sin(mrad)
        sin2m = math.sin(mrad+mrad)
        sin3m = math.sin(mrad+mrad+mrad)
        C = sinm * (1.914602 - t * (0.004817 + 0.000014 * t)) + sin2m * (0.019993 - 0.000101 * t) + sin3m * 0.000289
        return C
    def calcGeomMeanAnomalySun(self,t):
        M = 357.52911 + t * (35999.05029 - 0.0001537 * t)
        return M
    def calcSunDeclinationOld(self,year=0,month=0,day=0,hour=0,minute=0,second=0,stamp=0,zone=8,pm=False,dst=False):
        if(stamp==0 and year==0 and day==0 and month==0 and hour==0 and minute==0 and second==0):
            jday=self.getJD()
            tl=self.getTimeLocal()
            total=jday + tl/1440.0 - zone/24.0
            t=self.calcTimeJulianCent(total)
        elif(stamp!=0 and year==0 and day==0 and month==0 and hour==0 and minute==0 and second==0):
            jday=self.getJD(stamp=stamp)
            tl=self.getTimeLocal(stamp=stamp)
            total=jday + tl/1440.0 - zone/24.0
            t=self.calcTimeJulianCent(total)
        else:
            jday=self.getJD(year=year,month=month,day=day)
            tl=self.getTimeLocal(hr=hour,mn=minute,sc=second)
            total=jday + tl/1440.0 - zone/24.0
            t=self.calcTimeJulianCent(total)
        e = self.calcObliquityCorrection(t)
        Lambda = self.calcSunApparentLong(t)
        sint = math.sin(math.radians(e)) * math.sin(math.radians(Lambda))
        theta = math.degrees(math.asin(sint))
        return (theta*100+0.5)/100.0
    def calcSunDeclination(self,Stamp=None,PM=False,DST=False,TimeZone=8):
        MonthList = [
        {"name": 'January',   "numdays": 31},
        {"name": 'February',  "numdays": 28},
        {"name": 'March',     "numdays": 31},
        {"name": 'April',     "numdays": 30},
        {"name": 'May',       "numdays": 31},
        {"name": 'June',      "numdays": 30},
        {"name": 'July',      "numdays": 31},
        {"name": 'August',    "numdays": 31},
        {"name": 'September', "numdays": 30},
        {"name": 'October',   "numdays": 31},
        {"name": 'November',  "numdays": 30},
        {"name": 'December',  "numdays": 31}
        ]
        if(Stamp==None):
            TimeStamp = time.time()
        else:
            TimeStamp = Stamp
        Year=int(time.strftime("%Y",time.localtime(TimeStamp)))
        Month=int(time.strftime("%m",time.localtime(TimeStamp)))
        Day=int(time.strftime("%d",time.localtime(TimeStamp)))
        Hour=int(time.strftime("%H",time.localtime(TimeStamp)))
        Minute=int(time.strftime("%M",time.localtime(TimeStamp)))
        Second=int(time.strftime("%S",time.localtime(TimeStamp)))
        if(((Year % 4 == 0 and Year % 100 != 0) or Year % 400 == 0) and (Month == 2)):
            if(Day > 29):
                Day=29
        else:
            if(Day > MonthList[Month-1]['numdays']):
                Day = MonthList[Month-1]['numdays']
        if(Month <= 2):
            Year -= 1
            Month += 12
        JDay = math.floor(365.25*(Year + 4716)) + math.floor(30.6001*(Month+1)) + Day + 2 - math.floor(Year/100) + math.floor(math.floor(Year/100)/4) - 1524.5
        Minutes = Hour * 60 + Minute + Second/60.0
        TimeJulianCent = (JDay + Minutes/1440.0 - TimeZone/24.0 - 2451545.0)/36525.0
        L0 = 280.46646 + TimeJulianCent * (36000.76983 + TimeJulianCent * (0.0003032))
        while(L0 > 360.0):
            L0 -= 360.0
        while(L0 < 0.0):
            L0 += 360.0
        return (math.degrees(math.asin(math.sin(math.radians(23.0 + (26.0 + ((21.448 - TimeJulianCent * (46.8150 + TimeJulianCent * (0.00059 - TimeJulianCent * (0.001813)))) / 60.0)) / 60.0 + 0.00256 * math.cos(math.radians(125.04 - 1934.136 * TimeJulianCent)))) * math.sin(math.radians(L0 + math.sin(math.radians(357.52911 + TimeJulianCent * (35999.05029 - 0.0001537 * TimeJulianCent))) * (1.914602 - TimeJulianCent * (0.004817 + 0.000014 * TimeJulianCent)) + math.sin(math.radians(357.52911 + TimeJulianCent * (35999.05029 - 0.0001537 * TimeJulianCent)) * 2) * (0.019993 - 0.000101 * TimeJulianCent) + math.sin(math.radians(357.52911 + TimeJulianCent * (35999.05029 - 0.0001537 * TimeJulianCent)) * 3) * 0.000289 - 0.00569 - 0.00478 * math.sin(math.radians(125.04 - 1934.136 * TimeJulianCent)))))) * 100 + 0.5) / 100.0
c=Calendar()
print(c.calcSunDeclination())