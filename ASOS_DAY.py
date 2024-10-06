from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import urllib
import json
from xml.etree.ElementTree import parse
import xmltodict

import pandas as pd
import numpy as np
import time
import os

from datetime import datetime

class ASOS():
    def __init__(self,std: list, # Area_code
                 start_year: str, # YYYY ex) 2021
                 end_year: str, # YYYY ex) 2022
                 start_date: str= '0101', # MMDD
                 end_date: str= '1231', # MMDD
                 startHh: str= '00', # HH
                 endHh: str= '23', # HH
                 url: str= 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'):
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
    def add_keys(self,key: str) -> None:
        self.keys.append(key)

    # 지역 추가
    def add_std(self,std: int) -> None:
        self.std.append(std)

    # ASOS 데이터 가져오기
    def Crwal(self) -> None:
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
                                quote_plus('numOfRows') : '40',  # 윤년때문에 대충 366으로 해둠
                                # quote_plus('dataType') : 'XML',
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
                            continue
                        dicts = xml_dict['response']['body']['items']['item']
                        # df_temp = pd.DataFrame(columns = ['지점', '지점명', '일시','최저기온(°C)', '최고기온(°C)', 
                        #                                   '최대 풍속(m/s)', '평균 풍속(m/s)', '풍정합(100m)', '최소 상대습도(%)', '평균 상대습도(%)', 
                        #                                   '합계 일조시간(hr)', '합계 일사량(MJ/m2)', '합계 소형증발량(mm)'])
                        df_temp = pd.DataFrame(columns = ['지점 번호', '지점명', '시간', '평균 기온', '최저 기온', '최저 기온 시각', '최고 기온', '최고 기온 시각', 
                                                          '강수 계속시간', '10분 최다강수량', '10분 최다강수량 시각', '1시간 최다강수량', '1시간 최다 강수량 시각', 
                                                          '일강수량', '최대 순간풍속', '최대 순간 풍속 풍향', '최대 순간풍속 시각', '최대 풍속', '최대 풍속 풍향', 
                                                          '최대 풍속 시각', '평균 풍속', '풍정합', '최다 풍향', '평균 이슬점온도', '최소 상대습도', '평균 상대습도 시각', 
                                                          '평균 상대습도', '평균 증기압', '평균 현지기압', '최고 해면 기압', '최고 해면기압 시각', '최저 해면기압', 
                                                          '최저 해면기압 시각', '평균 해면기압', '가조시간', '합계 일조 시간', '1시간 최다 일사 시각', '1시간 최다 일사량', 
                                                          '합계 일사량', '일 최심신적설', '일 최심신적설 시각', '일 최심적설', '일 최심적설 시각', '합계 3시간 신적설', 
                                                          '평균 전운량', '평균 중하층운량', '평균 지면온도', '최저 초상온도', '평균 5cm 지중온도', '평균10cm 지중온도', 
                                                          '평균 20cm 지중온도', '평균 30cm 지중온도', '0.5m 지중온도', '1.0m 지중온도', '1.5m 지중온도', '3.0m 지중온도', 
                                                          '5.0m 지중온도', '합계 대형증발량', '합계 소형증발량', '9-9강수', '일기현상', '안개 계속 시간'])

                        for i in range(len(dicts)):
                            # df_temp.loc[i] = [dicts[i]['stnId'], dicts[i]['stnNm'], dicts[i]['tm'], dicts[i]['minTa'], dicts[i]['maxTa'], 
                            #                   dicts[i]['maxWs'], dicts[i]['avgWs'], dicts[i]['hr24SumRws'], dicts[i]['minRhm'], dicts[i]['avgRhm'],
                            #                   dicts[i]['sumSsHr'], dicts[i]['sumGsr'], dicts[i]['sumSmlEv']]
                            df_temp.loc[i] = [dicts[i]['stnId'], dicts[i]['stnNm'], dicts[i]['tm'], dicts[i]['avgTa'], dicts[i]['minTa'], 
                                              dicts[i]['minTaHrmt'], dicts[i]['maxTa'], dicts[i]['maxTaHrmt'], dicts[i]['mi10MaxRn'], dicts[i]['mi10MaxRnHrmt'], 
                                              dicts[i]['hr1MaxRn'], dicts[i]['hr1MaxRnHrmt'], dicts[i]['sumRnDur'], dicts[i]['sumRn'], dicts[i]['maxInsWs'], 
                                              dicts[i]['maxInsWsWd'], dicts[i]['maxInsWsHrmt'], dicts[i]['maxWs'], dicts[i]['maxWsWd'], dicts[i]['maxWsHrmt'], 
                                              dicts[i]['avgWs'], dicts[i]['hr24SumRws'], dicts[i]['maxWd'], dicts[i]['avgTd'], dicts[i]['minRhm'], dicts[i]['minRhmHrmt'], 
                                              dicts[i]['avgRhm'], dicts[i]['avgPv'], dicts[i]['avgPa'], dicts[i]['maxPs'], dicts[i]['maxPsHrmt'], dicts[i]['minPs'], 
                                              dicts[i]['minPsHrmt'], dicts[i]['avgPs'], dicts[i]['ssDur'], dicts[i]['sumSsHr'], dicts[i]['hr1MaxIcsrHrmt'], 
                                              dicts[i]['hr1MaxIcsr'], dicts[i]['sumGsr'], dicts[i]['ddMefs'], dicts[i]['ddMefsHrmt'], dicts[i]['ddMes'], 
                                              dicts[i]['ddMesHrmt'], dicts[i]['sumDpthFhsc'], dicts[i]['avgTca'], dicts[i]['avgLmac'], dicts[i]['avgTs'], 
                                              dicts[i]['minTg'], dicts[i]['avgCm5Te'], dicts[i]['avgCm10Te'], dicts[i]['avgCm20Te'], dicts[i]['avgCm30Te'], 
                                              dicts[i]['avgM05Te'], dicts[i]['avgM10Te'], dicts[i]['avgM15Te'], dicts[i]['avgM30Te'], dicts[i]['avgM50Te'], 
                                              dicts[i]['sumLrgEv'], dicts[i]['sumSmlEv'], dicts[i]['n99Rn'], dicts[i]['iscs'], dicts[i]['sumFogDur']]
                        df = pd.concat([df, df_temp])
                        print(f'{page}page 완료', end = ' ')
                        page += 1
                    except:
                        print(f'{page}page 오류 다시 시작. 시도횟수 {flag}/{self.flagmax} error code : {result}', end = ' ')
                        flag+=1
                    if page == 11:
                        break

                print()
                print(f'{year}완료 -- {datetime.now().time()}')

            if len(df.values) != 0:
                place = df['지점명'].unique()[0]
                path = f'./DataDay/{place}'
                if not os.path.exists(path):
                    os.makedirs(path)
                df.to_csv(f"{path}/{df['지점명'].unique()[0]}" + ".csv", index = False,encoding='utf-8 sig')
                print(f'지점번호 {std} 완료 -- {datetime.now().time()}')
            else:
                print(f'지점번호 {std} NO DATA')

    