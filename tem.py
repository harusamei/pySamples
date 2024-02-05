# 时间归一化: 只支持英文和中文点时间，且为明确的时间, 英文只限规范格式
# 如格式不正确输出None
# year is range in [1,9999]
# str2val, 中文整数转为 int,  不支持英文或非整数
# author:  mengyao1@lenovo.com;  2021-12-13

import time
from datetime import datetime, timedelta
import re


class DateTimeProc:
    """
    A class for processing date and time in different formats and languages.

    Attributes:
        curLocal (str): The current language and timezone mode.
        dateFormat (dict): A dictionary containing date formats for different languages.

    Methods:
        __init__(): Initializes the DateTimeProc class.
        cnDateNorm(timeStr): Normalizes the original Chinese date and time input.
        enDateNorm(timeStr): Normalizes the original English date and time input.
        parseDateTime(dtStr, curLocal='en_US'): Parses the date and time string and returns a struct_time object.
        outFormatDate(tDt, fmt=None): Formats the datetime object and returns a string representation.
        extraAdjust(baseTime, exInfo): Makes additional adjustments to the base time based on the extra information provided.
        numStd(oneStr): Standardizes Chinese numerals to Arabic numerals.
        str2val(oneStr): Converts Chinese numerals to integers.
        str2DateTime(oneStr): Converts a string representation of date and time to a datetime object.
    """

    def __init__(self):
        self.curLocal = 'en_US'
        self.dateFormat = {
            'en_US': ["%Y-%m-%d", "%Y.%b.%d", "%Y.%m.%d", "%Y/%m/%d",
                      "%b %d %Y", "%B %d %Y", "%d %b %Y", "%d %B %Y",
                      "%m/%d/%Y", "%b %Y", "%B %Y", "%d %b", "%m/%d",
                      "%b %d", "%B %d", "%Y"],
            'zh_CN': ["%Y年", "%y年",
                      "%Y年%m月", "%m月%d日", "%y年%m月",
                      "%y年%m月%d日", "%Y年%m月%d日"]
        }

        # Other attributes and methods...

    # Other methods...
# 时间归一化: 只支持英文和中文点时间，且为明确的时间, 英文只限规范格式
# 如格式不正确输出None
# year is range in [1,9999]
# str2val, 中文整数转为 int,  不支持英文或非整数
# author:  mengyao1@lenovo.com;  2021-12-13

import time
from datetime import datetime, timedelta
import re


class DateTimeProc:  # 只处理标准英语格式的时间format 如： 2019.2.20 14:23

    def __init__(self):

        self.curLocal = 'en_US'  # 默认语言和时区模式
        # 如果支持的语言和格式变多了， 可以独立成 config
        self.dateFormat = {'en_US': ["%Y-%m-%d", "%Y.%b.%d", "%Y.%m.%d", "%Y/%m/%d",
                                     "%b %d %Y", "%B %d %Y", "%d %b %Y", "%d %B %Y",
                                     "%m/%d/%Y", "%b %Y", "%B %Y", "%d %b", "%m/%d",
                                     "%b %d", "%B %d", "%Y"],
                           'zh_CN': ["%Y年", "%y年",
                                     "%Y年%m月", "%m月%d日", "%y年%m月",
                                     "%y年%m月%d日", "%Y年%m月%d日"]
                           }

        cnNumStr = "〇;零;壹;弌;一;二;弍;贰;三;弎;叁;四;肆;五;伍;陆;六;七;柒;捌;八;九;玖;廿;卅;卌;两"
        valList = [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 20, 30, 40, 2]
        cnQuan = "拾;十;百;佰;千;仟;万;亿"
        quanList = [10, 10, 100, 100, 1000, 1000, 10000, 100000000]
        fullNum = "１;２;３;４;５;６;７;８;９;０"
        halflist = '1;2;3;4;5;6;7;8;9;0'.split(';')

        self.cnNumMap = {}  # {String, Integer },  数词
        for indx, tKey in enumerate(cnNumStr.split(';')):
            self.cnNumMap[tKey] = valList[indx]
        self.cnQuanMap = {}  # {String, Integer },  数量词
        for indx, tKey in enumerate(cnQuan.split(';')):
            self.cnQuanMap[tKey] = quanList[indx]
        self.fullHalfMap = {}
        for indx, tKey in enumerate(fullNum.split(';')):
            self.fullHalfMap[tKey] = halflist[indx]

    # 规范原始输入，返回[0]:规范后，[1:]需要调整部分
    def cnDateNorm(self, timeStr):

        timeStr = re.sub(r'\s+', '', timeStr)
        if len(timeStr) < 2:
            return []
        timeStr = self.numStd(timeStr)  # 规范数字，然后才有然后
        aList = [timeStr]

        ignore = "(公元|上午|过|整|\\s)"
        adj = "(公元前|下午|差\\d+[分刻])"  # 差后面只能接分和刻，如差5分，差1刻
        for x in re.findall(adj, timeStr):
            aList.append(x)
            timeStr = timeStr.replace(x, '')
        timeStr = re.sub(ignore, '', timeStr)

        oriList = "点1刻;点2刻;点3刻;点半;点;号".split(';')
        repsList = "时15分00秒;时30分00秒;时45分00秒;时30分00秒;时;日".split(";")
        for indx, xStr in enumerate(oriList):
            timeStr = timeStr.replace(xStr, repsList[indx])

        aList[0] = timeStr
        return aList

    # 规范原始英文输入
    def enDateNorm(self, timeStr):

        aList = []
        timeStr = re.sub('\s+', " ", timeStr).strip()
        aList.append(timeStr)
        # Jan. 1st 2nd 3rd 4th ,am, AD
        ignoreList = ["([a-zA-Z]+)\.", "(\\d+)th", "st", "nd", "rd", "am", "a\.m\.", "AD"]
        for tPat in ignoreList:
            m = re.search(tPat, timeStr)
            if m:
                if len(m.groups()) > 1:
                    timeStr = timeStr.replace(m.group(0), m.group(1))
                else:
                    timeStr = timeStr.replace(m.group(0), "")

        timeStr = re.sub('\s+', " ", timeStr).strip()

        # 时间调整部分, PM  p.m.pm
        tPat = '[pP][\.]*[mM][\.]*'
        if re.search(tPat, timeStr):
            aList.append("下午")
            timeStr = re.sub(tPat, '', timeStr)

        # B.C.
        tPat = "[bB][\.]*[cC][\.]*"
        if re.search(tPat, timeStr):
            aList.append("公元前")
            timeStr = re.sub(tPat, '', timeStr).strip()

        aList[0] = timeStr
        return aList

    # 主函数， parse year in range [1,9999]
    def parseDateTime(self, dtStr, curLocal='en_US'):
        """
            dtStr:  日期或时间字符串
            curLocal: 时区，支持 zh_CN, en_US
            return: struct_time or None
        """
        if len(dtStr.strip()) < 2: return None
        if curLocal not in self.dateFormat.keys(): return None

        if curLocal == 'en_US':
            self.curLocal = 'en_US'
            tList = self.enDateNorm(dtStr)
        else:
            self.curLocal = 'zh_CN'
            tList = self.cnDateNorm(dtStr)
        if tList is None: return None

        curDate = self.str2DateTime(tList[0])
        if curDate is None: return None

        for tStr in tList[1:]:
            curDate = self.extraAdjust(curDate, tStr)
        return curDate

    def outFormatDate(self, tDt, fmt=None):

        if tDt is None: return ''
        if fmt is None:
            fmt = "%Y-%m-%d %H:%M:%S"
        tDt.strftime(fmt)
        return tDt.strftime(fmt)

    # 额外调整， 比如差X分，下午
    def extraAdjust(self, baseTime, exInfo):
        """
        baseTime: object of datetime
        return: object of datetime
        """
        if exInfo == '公元前':  # python, 不支持B.C
            print('warning: B.C is out of range')
        elif exInfo == '下午':
            baseTime = baseTime + timedelta(hours=12)
        elif exInfo.find('差') > -1:  # 5点差10分； 分解为 5点10分，差
            m = re.match('差(\d+)(.*)$', exInfo)
            spanTime = timedelta(minutes=0)
            if m.group(2) == '分':
                spanTime = timedelta(minutes=int(m.group(1)))
            elif m.group(2) == '刻':
                spanTime = timedelta(minutes=int(m.group(1)) * 15)
            baseTime = baseTime - spanTime

        return baseTime

    # 将汉字数据转化为阿拉伯数字
    def numStd(self, oneStr):
        if len(oneStr) < 1: return None
        tStr = ''
        for x in list(oneStr):  # 全角变半角
            if x in self.fullHalfMap:
                tStr += self.fullHalfMap[x]
            else:
                tStr += x
        oneStr = tStr
        tStr = ''
        for x in list(oneStr):
            if x in self.cnNumMap:
                tStr += 'N'
            elif x in self.cnQuanMap:
                tStr += 'Q'
            else:
                tStr += "#"
        hanNumList = []
        for fit in re.finditer('[NQ]+', tStr):
            numStr = oneStr[fit.span()[0]:fit.span()[1]]
            tVal = self.str2val(numStr)
            hanNumList.append((numStr, tVal, fit.span()[0], fit.span()[1]))
        tStr, shift = '', 0
        for aTuple in hanNumList:
            tStr += oneStr[shift:aTuple[2]]
            tStr += str(aTuple[1])
            shift = aTuple[3]
        tStr += oneStr[shift:]
        return tStr

    # 汉字数字变阿拉伯数字
    def str2val(self, oneStr):

        if len(oneStr) < 1: return 0
        if re.match('\d+$', oneStr):  # 全部是数字
            return int(oneStr)

        sum, numStr = 0, ''
        for x in list(oneStr):
            if x in self.cnNumMap.keys():
                numStr += str(self.cnNumMap[x])
            elif '0123456789'.find(x) > -1:
                numStr += x
            elif x in self.cnQuanMap.keys():
                if numStr != '':
                    sum += int(numStr) * self.cnQuanMap[x]
                else:
                    sum = sum * self.cnQuanMap[x]
                numStr = ''
        # 一万五； 一万零五
        if numStr != '':
            if len(oneStr)>2 and oneStr[-2] in self.cnQuanMap.keys():
                sum += int(numStr)*self.cnQuanMap[oneStr[-2]]/10
            else:
                sum += int(numStr)
        return int(sum)

    def str2DateTime(self, oneStr):
        """
        :param oneStr: string of date and time, such as '2019年三月七日下午10点差五分'
        :return: object of datetime
        """

        if len(oneStr) < 1 or re.search(r'\d{2}', oneStr) is None:
            return None

        tResult = []
        m = re.search(r'(\d{1,2})[:时][\d:分秒]*$', oneStr)  # 必须有hour, minute,second可以没有
        if m:
            tResult = re.findall('\d+', oneStr[m.span()[0]:])
            oneStr = oneStr[:m.span()[0]].strip()
        tResult.extend(['0'] * 3)
        timeSpan = timedelta(hours=int(tResult[0]), minutes=int(tResult[1]), seconds=int(tResult[2]))

        parsedDate = None
        dateFormat = self.dateFormat[self.curLocal]
        for tFormat in dateFormat:
            try:
                parsedDate = time.strptime(oneStr, tFormat)
                break
            except ValueError as v:
                continue
        if parsedDate is not None:
            tDate = datetime(*list(parsedDate[:3]))
            return tDate + timeSpan
        elif timeSpan > timedelta(seconds=0):
            return datetime(1900, 1, 1) + timeSpan
        return None


if __name__ == '__main__':
    p = DateTimeProc()
    testList = ["公元二千零五年", "二零二一年12月12点3刻", "三月11号下午", "2019年三月七日下午10点差五分", "今年"]
    testList2 = ["BC 2019/3/8 8:32 PM", "January 2019"]
    testList3 = ['一千万','二十五','一亿三千五百万零三十','2千五']
    for x in testList:
        tDt = p.parseDateTime(x, 'zh_CN')
        print(p.outFormatDate(tDt))
    for x in testList2:
        tDt = p.parseDateTime(x, 'en_US')
        print(p.outFormatDate(tDt))
    for x in testList3:
        print(p.str2val(x))
