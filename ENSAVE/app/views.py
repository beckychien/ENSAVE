from django.shortcuts import render
from ENSAVE.common import Common
from django.http import JsonResponse
import datetime
from ENSAVE.myLog import MyLog

# 冷卻塔(Cooling Tower)
# 冷卻泵(condenser pump)
# 冷凍泵(chiller pump)
# 冷水機組(water chiller unit)
# 有功功率(efficientpower)
# 有功電能(powerconsumption)


# 7电錶接2号冷水机
# 3电錶接4号冷冻泵
# 10电錶接4号冷却泵
# 4电錶接冷却水塔
# 2电錶接1+2冷冻泵

mylog = MyLog('ensave')

# Create your views here.
def realtime_view(request):
    try:
        mylog.logger.info("request-realtime")
        sql = ''' SELECT * from mv_autodata_temp '''
        machine = ['chillerpump1', 'chillerpump2', 'chillerpump3', 'chillerpump4', 'cooling1', 'cooling2', 'cooling3',
                   'wchiller1', 'wchiller2', 'wchiller3', 'condenserpump1', 'condenserpump2', 'condenserpump3',
                   'condenserpump4']
        result = {}
        realtimelist = []
        rows = Common.GetData(sql)
        for row in rows:
            chillerpump1_power = float(round(row[1], 2))
            chillerpump1_efficient = float(round(row[2], 2))
            chillerpump4_power = float(round(row[3], 2))
            chillerpump4_efficient = float(round(row[4], 2))
            cooling1_power = float(round(row[5], 2))
            cooling1_efficient = float(round(row[6], 2))
            wchiller2_power = float(round(row[7], 2))
            wchiller2_efficient = float(round(row[8], 2))
            condenserpump4_power = float(round(row[9], 2))
            condenserpump4_efficient = float(round(row[10], 2))

            flow = row[13]
            intemp = row[14]
            outtemp = row[15]
        for i, val in enumerate(machine):
            context = {}
            context1 = {}
            if (i == 0 or i == 1):
                context1['ammeter'] = "电錶#2"
                context1['efficientpower'] = chillerpump1_efficient
                context1['powerconsumption'] = chillerpump1_power
            elif (i == 3):
                context1['ammeter'] = "电錶#3"
                context1['efficientpower'] = chillerpump4_efficient
                context1['powerconsumption'] = chillerpump4_power
            elif (i == 4 or i == 5 or i == 6):
                context1['ammeter'] = "电錶#4"
                context1['efficientpower'] = cooling1_efficient
                context1['powerconsumption'] = cooling1_power
            elif (i == 8):
                context1['ammeter'] = "电錶#7"
                context1['efficientpower'] = wchiller2_efficient
                context1['powerconsumption'] = wchiller2_power
            elif (i == 13):
                context1['ammeter'] = "电錶#10"
                context1['efficientpower'] = condenserpump4_efficient
                context1['powerconsumption'] = condenserpump4_power
            else:
                context1['ammeter'] = "#"
                context1['efficientpower'] = "#"
                context1['powerconsumption'] = "#"
            context[val] = context1
            realtimelist.append(context)

        RT = flow * (intemp - outtemp) * 1000 / 3000
        KW = chillerpump1_efficient + chillerpump4_efficient + cooling1_efficient + wchiller2_efficient + condenserpump4_efficient
        if (RT == 0 or KW == 0):
            COP = 0
            KR = 0
        else:
            KR = KW / RT
            COP = float(round(3.5 / KR, 2))
        realtimelist.append({'COP': COP})
        realtimelist.append({'KR': float(round(KR,2))})
        result['data'] = realtimelist
        return JsonResponse(result)
    except Exception as inst:
        print(inst)
        mylog.logger.error(inst)
        return inst


def yeardata_view(request):
    try:
        mylog.logger.info("request-year")
        now = datetime.datetime.now()
        datepara = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        sql = ''' exec bp_历史数据 '2020-01-01','{0}' '''.format(datepara)
        context = {}
        rows = Common.GetData(sql)

        total_chillerpump = 0
        total_cooling = 0
        total_waterchiller = 0
        total_condenserpump = 0
        total_cop = 0
        total_KR = 0

        for row in rows:
            total_chillerpump = total_chillerpump + row[2] + row[4]
            total_cooling = total_cooling + row[6]
            total_waterchiller = total_waterchiller + row[8]
            total_condenserpump = total_condenserpump + row[10]

            flow = row[13]
            intemp = row[14]
            outtemp = row[15]
            RT = flow * (intemp - outtemp) * 1000 / 3000
            KW = row[2] + row[4] + row[6] + row[8] + row[10]
            if (RT == 0 or KW == 0):
                COP = 0
                KR = 0
            else:
                KR = float((KW / RT))
                COP = 3.5 / KR

            total_cop=total_cop+COP
            total_KR=total_KR+KR

        totalpowerconsumption = round((total_chillerpump + total_cooling + total_waterchiller + total_condenserpump)/10000,2)
        avg_cop=total_cop/len(rows)
        avg_KR=total_KR/len(rows)

        context['totalpowerconsumption'] = float(totalpowerconsumption)
        context['total_chillerpump'] = float(total_chillerpump)
        context['total_cooling'] = float(total_cooling)
        context['total_waterchiller'] = float(total_waterchiller)
        context['total_condenserpump'] = float(total_condenserpump)
        context['avg_cop'] = float(round(avg_cop,2))
        context['avg_KR'] = float(round(avg_KR,2))

        return JsonResponse(context)
    except Exception as inst:
        print(inst)
        mylog.logger.error(inst)
        return inst
