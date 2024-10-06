from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import urllib
import json
from xml.etree.ElementTree import parse
import xmltodict

import pandas as pd
import numpy as np
import time

from datetime import datetime

class ASOSDay():
    def __init__(self,key: str, # ASOS endcoding key not decoding
                 std: list, # Area_code
                 start_year: str, # YYYY ex) 2021
                 end_year: str, # YYYY ex) 2022
                 items: list, # Necessary items
                 start_date: str= '0101', # MMDD
                 end_date: str= '1231', # MMDD
                 startHh: str= '00', # HH
                 endHh: str= '23', # HH
                 url: str= 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'):
        self.std = std
        self.start_year = start_year
        self.end_year = end_year
        self.items = ['지점', '지점명', '일시'] + items
        self.start_date = start_date
        self.end_date = end_date
        self.startHh = startHh 
        self.endHh = endHh
        self.url = url
        self.flagmax = 10

        self.keys = [key]
    
        self.col_names = {'지점 번호': 'stnId', 
                '지점명': 'stnNm', 
                '시간': 'tm ', 
                '평균 기온': 'avgTa', 
                '최저 기온': 'minTa', 
                '최저 기온 시각': 'minTaHrmt', 
                '최고 기온': 'maxTa', 
                '최고 기온 시각': 'maxTaHrmt', 
                '강수 계속시간': 'sumRnDur', 
                '10분 최다강수량': 'mi10MaxRn', 
                '10분 최다강수량 시각': 'mi10MaxRnHrmt', 
                '1시간 최다강수량': 'hr1MaxRn', 
                '1시간 최다 강수량 시각': 'hr1MaxRnHrmt', 
                '일강수량': 'sumRn', 
                '최대 순간풍속': 'maxInsWs', 
                '최대 순간 풍속 풍향': 'maxInsWsWd', 
                '최대 순간풍속 시각': 'maxInsWsHrmt', 
                '최대 풍속': 'maxWs', 
                '최대 풍속 풍향': 'maxWsWd', 
                '최대 풍속 시각': 'maxWsHrmt', 
                '평균 풍속': 'avgWs', 
                '풍정합': 'hr24SumRws', 
                '최다 풍향': 'maxWd', 
                '평균 이슬점온도': 'avgTd', 
                '최소 상대습도': 'minRhm', 
                '평균 상대습도 시각': 'minRhmHrmt', 
                '평균 상대습도': 'avgRhm', 
                '평균 증기압': 'avgPv', 
                '평균 현지기압': 'avgPa', 
                '최고 해면 기압': 'maxPs', 
                '최고 해면기압 시각': 'maxPsHrmt', 
                '최저 해면기압': 'minPs', 
                '최저 해면기압 시각': 'minPsHrmt', 
                '평균 해면기압': 'avgPs', 
                '가조시간': 'ssDur', 
                '합계 일조 시간': 'sumSsHr', 
                '1시간 최다 일사 시각': 'hr1MaxIcsrHrmt', 
                '1시간 최다 일사량': 'hr1MaxIcsr', 
                '합계 일사량': 'sumGsr', 
                '일 최심신적설': 'ddMefs', 
                '일 최심신적설 시각': 'ddMefsHrmt', 
                '일 최심적설': 'ddMes', 
                '일 최심적설 시각': 'ddMesHrmt', 
                '합계 3시간 신적설': 'sumDpthFhsc', 
                '평균 전운량': 'avgTca', 
                '평균 중하층운량': 'avgLmac', 
                '평균 지면온도': 'avgTs', 
                '최저 초상온도': 'minTg', 
                '평균 5cm 지중온도': 'avgCm5Te', 
                '평균10cm 지중온도': 'avgCm10Te', 
                '평균 20cm 지중온도': 'avgCm20Te', 
                '평균 30cm 지중온도': 'avgCm30Te', 
                '0.5m 지중온도': 'avgM05Te', 
                '1.0m 지중온도': 'avgM10Te', 
                '1.5m 지중온도': 'avgM15Te', 
                '3.0m 지중온도': 'avgM30Te', 
                '5.0m 지중온도': 'avgM50Te', 
                '합계 대형증발량': 'sumLrgEv', 
                '합계 소형증발량': 'sumSmlEv', 
                '9-9강수': 'n99Rn', 
                '일기현상': 'iscs', 
                '안개 계속 시간': 'sumFogDur'}
    # key 추가
    def add_keys(self,key: str):
        self.keys.append(key)

    def set_datas(self,datas):
        self.data = []
        self.data.append()
    # ASOS 데이터 가져오기
    def Crwal(self):
        for std in self.std:
            df = pd.DataFrame()
            print(f'지점번호 {std} 시작 -- {datetime.now().time()}')
            breaker = False
            for year in range(int(self.start_year),int(self.end_year)+1,1):
                print(f'{year}년 시작', end = ' ')
                flag=0
                if breaker == True:
                    break
                page = 1
                key_idx = 0                
                while flag<self.flagmax:
                    key = self.keys[key_idx]
                    try:
                        queryParams = '?' + urlencode({
                                quote_plus('ServiceKey') : key,
                                quote_plus('pageNo') : f'{page}',   # 1 ~ 10
                                quote_plus('numOfRows') : '40',  # 36개 인데 혹시몰라서 40으로 함
                                # quote_plus('dataType') : 'XML', # 있어도 되고 없어도 되는데 원인을 모르겠음
                                quote_plus('dataCd') : 'ASOS',
                                quote_plus('dateCd') : 'DAY',
                                quote_plus('startDt') : f'{year}{self.start_date}',
                                quote_plus('endDt') : f'{year}{self.end_date}',
                                # quote_plus('startHh') : self.startHh,
                                # quote_plus('endHh') : self.endHh,
                                quote_plus('stnIds') : f'{std}'})
                        request = urllib.request.Request(self.url + unquote(queryParams))

                        response_body = urlopen(request, timeout=60).read()

                        decode_data = response_body.decode('utf-8')

                        xml_parse = xmltodict.parse(decode_data)     # string인 xml 파싱
                        xml_dict = json.loads(json.dumps(xml_parse))
                        result = xml_dict['response']['header']['resultMsg']
                        if result == 'NO_DATA':
                            breaker = True
                            break
                        elif result == 'LIMITED_NUMBER_OF_SERVICE_REQUESTS_EXCEEDS_ERROR':
                            print('서비스 요청 제한횟수 초과')
                            time.sleep(5)
                            key_idx += 1
                            if key_idx >= len(self.keys):
                                key_idx = 0
                        dicts = xml_dict['response']['body']['items']['item']

                        df_temp = pd.DataFrame(columns = self.items)

                        for i in range(len(dicts)):
                            loc = []
                            for j in self.items:
                                loc.append(dicts[i][self.col_names[j]])
                            df_temp.loc[i] = loc
                                # df_temp.loc[i] = [dicts[i]['stnId'], dicts[i]['stnNm'], dicts[i]['tm'], dicts[i]['minTa'], dicts[i]['maxTa'], 
                                #                 dicts[i]['maxWs'], dicts[i]['avgWs'], dicts[i]['hr24SumRws'], dicts[i]['minRhm'], dicts[i]['avgRhm'],
                                #                 dicts[i]['sumSsHr'], dicts[i]['sumGsr'], dicts[i]['sumSmlEv']]
                        df = pd.concat([df, df_temp])
                        print(f'{page}page 완료', end = ' ')
                        page += 1
                    except:
                        print(f'{page}page 오류 다시 시작. 시도횟수 {flag}/{self.flagmax}', end = ' ')
                        flag+=1
                    if page == 11:
                        break

                print()
                print(f'{year}완료 -- {datetime.now().time()}')
            
            if len(df.values) != 0:
                df.to_csv(f"./춘천/{df['지점명'].unique()[0]}" + ".csv", index = False,encoding='utf-8 sig')
                print(f'지점번호 {std} 완료 -- {datetime.now().time()}')
            else:
                print(f'지점번호 {std} NO DATA')


class ASOSHr():
    def __init__(self,std: list, # Area_code
                 start_year: str, # YYYY ex) 2021
                 end_year: str, # YYYY ex) 2022
                 start_date: str= '0101', # MMDD
                 end_date: str= '1231', # MMDD
                 startHh: str= '00', # HH
                 endHh: str= '23', # HH
                 url: str= 'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList'):
        self.std = std
        self.start_year = start_year
        self.end_year = end_year
        self.start_date = start_date
        self.end_date = end_date
        self.startHh = startHh
        self.endHh = endHh
        self.url = url
        self.flagmax = 10

        self.keys = []

    # key 추가
    def add_keys(self,key: str):
        self.keys.append(key)

    # 지역 추가
    def add_std(self,std: int):
        self.std.append(std)

    # ASOS 데이터 가져오기
    def Crwal(self):
        for std in self.std:
            df = pd.DataFrame()
            print(f'지점번호 {std} 시작 -- {datetime.now().time()}')
            breaker = False
            for year in range(int(self.start_year),int(self.end_year)+1,1):
                print(f'{year}년 시작', end = ' ')
                flag=0
                if breaker == True:
                    break
                page = 1
                key_idx = 0                
                while flag<self.flagmax:
                    key = self.keys[key_idx]
                    try:
                        queryParams = '?' + urlencode({
                                quote_plus('ServiceKey') : key,
                                quote_plus('pageNo') : f'{page}',   # 1 ~ 10
                                quote_plus('numOfRows') : '880',  # 윤년때문에 대충 366으로 해둠
                                quote_plus('dataType') : 'XML',
                                quote_plus('dataCd') : 'ASOS',
                                quote_plus('dateCd') : 'HR',
                                quote_plus('startDt') : f'{year}{self.start_date}',
                                quote_plus('endDt') : f'{year}{self.end_date}',
                                quote_plus('startHh') : self.startHh,
                                quote_plus('endHh') : self.endHh,
                                quote_plus('stnIds') : f'{std}'})
                        request = urllib.request.Request(self.url + unquote(queryParams))

                        response_body = urlopen(request, timeout=60).read()

                        decode_data = response_body.decode('utf-8')

                        xml_parse = xmltodict.parse(decode_data)     # string인 xml 파싱
                        xml_dict = json.loads(json.dumps(xml_parse))
                        result = xml_dict['response']['header']['resultMsg']
                        if result == 'NO_DATA':
                            breaker = True
                            break
                        elif result == 'LIMITED_NUMBER_OF_SERVICE_REQUESTS_EXCEEDS_ERROR':
                            print('서비스 요청 제한횟수 초과')
                            time.sleep(5)
                            key_idx += 1
                            if key_idx >= len(self.keys):
                                key_idx = 0
                        dicts = xml_dict['response']['body']['items']['item']

                        # df_temp = pd.DataFrame(columns = ['날짜', '시간', '지점_번호', '지점명', '기온', '강수량', '풍속', '풍향', '습도', '증기압', '이슬점온도', '현지기압', '해면기압', '일조', '일사', '적설', '3시간_신절설', '전운량', '중하층운량', '운형', '최저운고', '시정', '지면온도', '5cm_지중온도', '10cm_지중온도', '20cm_지중온도', '30cm_지중온도'])
                        df_temp = pd.DataFrame(columns = ['지점', '지점명', '일시', '강수량(mm)'])

                        for i in range(len(dicts)):
                            # df_temp.loc[i] = [dicts[i]['tm'][:10], dicts[i]['tm'][11:], dicts[i]['stnId'], dicts[i]['stnNm'], dicts[i]['ta'], dicts[i]['rn'], dicts[i]['ws'], dicts[i]['wd'], dicts[i]['hm'], dicts[i]['pv'], dicts[i]['td'], dicts[i]['pa'], dicts[i]['ps'], dicts[i]['ss'], dicts[i]['icsr'], dicts[i]['dsnw'], dicts[i]['hr3Fhsc'], dicts[i]['dc10Tca'], dicts[i]['dc10LmcsCa'], dicts[i]['clfmAbbrCd'], dicts[i]['lcsCh'], dicts[i]['vs'], dicts[i]['ts'], dicts[i]['m005Te'], dicts[i]['m01Te'], dicts[i]['m02Te'], dicts[i]['m03Te']]
                            df_temp.loc[i] = [dicts[i]['stnId'], dicts[i]['stnNm'], dicts[i]['tm'], dicts[i]['rn']]
                        df = pd.concat([df, df_temp])
                        print(f'{page}page 완료', end = ' ')
                        page += 1
                    except:
                        print(f'{page}page 오류 다시 시작. 시도횟수 {flag}/{self.flagmax}', end = ' ')
                        flag+=1
                    if page == 11:
                        break

                print()
                print(f'{year}완료 -- {datetime.now().time()}')
            
            if len(df.values) != 0:
                try:
                    ddf = pd.read_csv(f"./{df['지점명'].unique()[0]}.csv")
                    df = pd.concat([ddf,df],axis=0)
                    df.fillna(0,inplace=True)
                    df.to_csv(f"./{df['지점명'].unique()[0]}" + ".csv", index = False,encoding='utf-8 sig')
                    print(f'지점번호 {std} 완료 -- {datetime.now().time()}')
                except:
                    df.fillna(0,inplace=True)
                    df.to_csv(f"./{df['지점명'].unique()[0]}" + ".csv", index = False,encoding='utf-8 sig')
                    print(f'지점번호 {std} 완료 -- {datetime.now().time()}')
            else:
                print(f'지점번호 {std} NO DATA')