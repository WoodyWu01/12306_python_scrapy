
import urllib.request
import re
import ssl
import urllib.parse
import http.cookiejar
import datetime
import time
#Ϊ�˷�ֹssl�������⣬���Լ�������һ�д���
ssl._create_default_https_context = ssl._create_unverified_context

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0"

#��Ʊ
#������������վ���Ӧ��ϵ
areatocode={"�Ϻ�":"SHH","����":"BJP","�Ͼ�":"NJH","��ɽ":"KSH","����":"HZH","����":"GLZ"}
start1=input("��������ʼվ:")
#start1="����"
start=areatocode[start1]
to1=input("�����뵽վ:")
#to1="�Ϻ�"
to=areatocode[to1]
isstudent=input("��ѧ�����ǣ�1�����ǣ�0")
#isstudent="0"
date=input("������Ҫ��ѯ�ĳ˳���ʼ���ڵ����£���2017-03-05��")
#date="2018-04-13"
if(isstudent=="0"):
    student="ADULT"
else:
    student="0X00"
url="https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date="+date+"&leftTicketDTO.from_station="+start+"&leftTicketDTO.to_station="+to+"&purpose_codes="+student

print("url=:" + url)
context = ssl._create_unverified_context()


# centerurl="https://kyfw.12306.cn/otn/index/initMy12306"
req_yun = urllib.request.Request(url)

# print("req_yun:" + req_yun)
req_yun.add_header('User-Agent', user_agent)


data=urllib.request.urlopen(req_yun).read().decode("utf-8","ignore")
print("****"+data)
patrst01='"result":\[(.*?)\]'
rst01=re.compile(patrst01).findall(data)[0]
allcheci=rst01.split(",")
checimap_pat='"map":({.*?})'
checimap=eval(re.compile(checimap_pat).findall(data)[0])
print("����\t����վ��\t����վ��\t����ʱ��\t����ʱ��\tһ����\t������\tӲ��\t����")
for i in range(0,len(allcheci)):
    try:
        thischeci=allcheci[i].split("|")
        #[3]---code
        code=thischeci[3]
        #[6]---fromname
        fromname=thischeci[6]
        fromname=checimap[fromname]
        #[7]---toname
        toname=thischeci[7]
        toname=checimap[toname]
        #[8]---stime
        stime=thischeci[8]
        #[9]---atime
        atime=thischeci[9]
        #[28]---yz
        yz=thischeci[31]
        #[29]---wz
        wz=thischeci[30]
        #[30]---ze
        ze=thischeci[29]
        #[31]---zy
        zy=thischeci[26]
        print(code+"\t"+fromname+"\t"+toname+"\t"+stime+"\t"+atime+"\t"+str(zy)+"\t"+str(ze)+"\t"+str(yz)+"\t"+str(wz))
    except Exception as err:
        pass
isdo=input("��Ʊ��ɣ�������1������")
#isdo=1
if(isdo==1 or isdo=="1"):
    pass
else:
    raise Exception("���벻��1������ִ��")
print("Cookie�����С�")


#���½��е�½����
#����cookie����
cjar=http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
urllib.request.install_opener(opener)

yzmurl="https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand"
while True:
    urllib.request.urlretrieve(yzmurl,"E:/tmp/yzm.png")
    yzm=input("��������֤�룬����ڼ���ͼƬ����")
    if(yzm!="re"):
        break
#x����(35,112,173,253)��y����(45)
#x����(35,112,173,253)��y����(114)
pat1='"(.*?)"'
allpic=re.compile(pat1).findall(yzm)
def getxy(pic):
    if(pic==1):
        xy=(35,45)
    if(pic==2):
        xy=(112,45)
    if(pic==3):
        xy=(173,45)
    if(pic==4):
        xy=(253,45)
    if(pic==5):
        xy=(35,114)
    if(pic==6):
        xy=(112,114)
    if(pic==7):
        xy=(173,114)
    if(pic==8):
        xy=(253,114)
    return xy
allpicpos=""
for i in allpic:
    thisxy=getxy(int(i))
    for j in thisxy:
        allpicpos=allpicpos+str(j)+","
allpicpos2=re.compile("(.*?).$").findall(allpicpos)[0]

print(allpicpos2)

#*************************post��֤����֤***************
yzmposturl="https://kyfw.12306.cn/passport/captcha/captcha-check"
yzmpostdata =urllib.parse.urlencode({
"answer":allpicpos2,
"rand":"sjrand",
"login_site":"E",
}).encode('utf-8')
req1 = urllib.request.Request(yzmposturl,yzmpostdata)
req1.add_header('User-Agent', user_agent)
req1data=urllib.request.urlopen(req1).read().decode("utf-8","ignore")

#******************************post�˺�������֤
loginposturl="https://kyfw.12306.cn/passport/web/login"
loginpostdata =urllib.parse.urlencode({
"username":"wzr1095826",
"password":"**********",
"appid":"otn",
}).encode('utf-8')
req2 = urllib.request.Request(loginposturl,loginpostdata)
req2.add_header('User-Agent', user_agent)
req2data=urllib.request.urlopen(req2).read().decode("utf-8","ignore")

#*********************������֤
loginposturl2="https://kyfw.12306.cn/otn/login/userLogin"
loginpostdata2 =urllib.parse.urlencode({
"_json_att":"",
}).encode('utf-8')
req2_2 = urllib.request.Request(loginposturl2,loginpostdata2)
req2_2.add_header('User-Agent', user_agent)
req2data_2=urllib.request.urlopen(req2_2).read().decode("utf-8","ignore")

loginposturl3="https://kyfw.12306.cn/passport/web/auth/uamtk"
loginpostdata3 =urllib.parse.urlencode({
"appid":"otn",
}).encode('utf-8')
req2_3 = urllib.request.Request(loginposturl3,loginpostdata3)
req2_3.add_header('User-Agent',user_agent)
req2data_3=urllib.request.urlopen(req2_3).read().decode("utf-8","ignore")
pat_req2='"newapptk":"(.*?)"'
tk=re.compile(pat_req2,re.S).findall(req2data_3)[0]

loginposturl4="https://kyfw.12306.cn/otn/uamauthclient"
loginpostdata4 =urllib.parse.urlencode({
"tk":tk,
}).encode('utf-8')
req2_4 = urllib.request.Request(loginposturl4,loginpostdata4)
req2_4.add_header('User-Agent', user_agent)
req2data_4=urllib.request.urlopen(req2_4).read().decode("utf-8","ignore")


#����������ҳ��
centerurl="https://kyfw.12306.cn/otn/index/initMy12306"
req3 = urllib.request.Request(centerurl)
req3.add_header('User-Agent', user_agent)
req3data=urllib.request.urlopen(req3).read().decode("utf-8","ignore")
print("��½���")
#isdo="1"
isdo=input("�����Ҫ��Ʊ��������1������������������������")
if(isdo==1 or isdo=="1"):
    pass
else:
    raise Exception("���벻��1������ִ��")
thiscode=input("������ҪԤ���ĳ��Σ�")
chooseno="None"

#****************************************��Ʊ�Ͷ�Ʊ
while True:
    try:
        #��Ʊ
        #�ȳ�ʼ��һ�¶�Ʊ����
        print("���ڶ�Ʊ������")

        initurl="https://kyfw.12306.cn/otn/leftTicket/init"
        reqinit=urllib.request.Request(initurl)
        reqinit.add_header('User-Agent', user_agent)
        initdata=urllib.request.urlopen(reqinit).read().decode("utf-8","ignore")
        #������Ӧ��Ʊ��Ϣ
       # bookurl="https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date="+date+"&leftTicketDTO.from_station="+start+"&leftTicketDTO.to_station="+to+"&purpose_codes="+student
        bookurl="https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date="+date+"&leftTicketDTO.from_station="+start+"&leftTicketDTO.to_station="+to+"&purpose_codes="+student

        req4 = urllib.request.Request(bookurl)
        req4.add_header('User-Agent', user_agent)
        req4data=urllib.request.urlopen(req4).read().decode("utf-8","ignore")
        #�洢������secretStr��Ϣ
        patrst01='"result":\[(.*?)\]'
        rst01=re.compile(patrst01).findall(req4data)[0]
        allcheci=rst01.split(",")
        checimap_pat='"map":({.*?})'
        checimap=eval(re.compile(checimap_pat).findall(req4data)[0])

        code=[]
        secretStr=[]
        zy=[]
        for i in range(0,len(allcheci)):
            try:
                thischeci=allcheci[i].split("|")
                #print(thischeci)
                #[3]---code
                thiscode1=thischeci[3]
                code.append(thiscode1)
                #[0]---secretStr
                secretStr.append(thischeci[0].replace('"',""))
                #[31]-zy
                thiszy=thischeci[31]
                zy.append(thiszy)
            except Exception as err:
                pass
        #���ֵ�trainzy�洢������û��Ʊ����Ϣ
        trainzy={}
        for i in range(0,len(code)):
            trainzy[code[i]]=zy[i]
        #���ֵ�traindata�洢����secretStr��Ϣ���Թ�������Ʊ����
        #�洢�ĸ�ʽ�ǣ�traindata={"����1":secretStr1,"����2":secretStr2,��}
        traindata={}
        for i in range(0,len(code)):
            traindata[code[i]]=secretStr[i]
        #��Ʊ-��1��post-��Ҫ����ȷ���û�״̬
        checkurl="https://kyfw.12306.cn/otn/login/checkUser"
        checkdata =urllib.parse.urlencode({
        "_json_att":""
        }).encode('utf-8')
        req5 = urllib.request.Request(checkurl,checkdata)
        req5.add_header('User-Agent', user_agent)
        req5data=urllib.request.urlopen(req5).read().decode("utf-8","ignore")
        #�Զ��õ���ǰʱ�䲢תΪ��-��-��ʽ����Ϊ��������������Ҫ�õ���ǰʱ����Ϊ����ʱ��backdate
        backdate=datetime.datetime.now()
        backdate=backdate.strftime("%Y-%m-%d")
        #��Ʊ-��2��post-��Ҫ���С�Ԥ�����ύ
        submiturl="https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"
        submitdata =urllib.parse.urlencode({
        "secretStr":traindata[thiscode],
        "train_date":date,
        "back_train_date":backdate,
        "tour_flag":"dc",
        "purpose_codes":student,
        "query_from_station_name":start1,
        "query_to_station_name":to1,
        })
        submitdata2=submitdata.replace("%25","%")
        submitdata3=submitdata2.encode('utf-8')
        req6 = urllib.request.Request(submiturl,submitdata3)
        req6.add_header('User-Agent', user_agent)
        req6data=urllib.request.urlopen(req6).read().decode("utf-8","ignore")
        #��Ʊ-��3��post-��Ҫ��ȡToken��leftTicketStr��key_check_isChange��train_location
        initdcurl="https://kyfw.12306.cn/otn/confirmPassenger/initDc"
        initdcdata =urllib.parse.urlencode({
        "_json_att":""
        }).encode('utf-8')
        req7 = urllib.request.Request(initdcurl,initdcdata)
        req7.add_header('User-Agent', user_agent)
        req7data=urllib.request.urlopen(req7).read().decode("utf-8","ignore")
        #��ȡtrain_no��leftTicketStr��fromStationTelecode��toStationTelecode��train_location
        train_no_pat="'train_no':'(.*?)'"
        leftTicketStr_pat="'leftTicketStr':'(.*?)'"
        fromStationTelecode_pat="from_station_telecode':'(.*?)'"
        toStationTelecode_pat="'to_station_telecode':'(.*?)'"
        train_location_pat="'train_location':'(.*?)'"
        pattoken="var globalRepeatSubmitToken.*?'(.*?)'"
        patkey="'key_check_isChange':'(.*?)'"
        train_no_all=re.compile(train_no_pat).findall(req7data)
        if(len(train_no_all)!=0):
            train_no=train_no_all[0]
        else:
            raise Exception("train_no��ȡʧ��")
        leftTicketStr_all=re.compile(leftTicketStr_pat).findall(req7data)
        if(len(leftTicketStr_all)!=0):
            leftTicketStr=leftTicketStr_all[0]
        else:
            raise Exception("leftTicketStr��ȡʧ��")
        fromStationTelecode_all=re.compile(fromStationTelecode_pat).findall(req7data)
        if(len(fromStationTelecode_all)!=0):
            fromStationTelecode=fromStationTelecode_all[0]
        else:
            raise Exception("fromStationTelecod��ȡʧ��")
        toStationTelecode_all=re.compile(toStationTelecode_pat).findall(req7data)
        if(len(toStationTelecode_all)!=0):
            toStationTelecode=toStationTelecode_all[0]
        else:
            raise Exception("toStationTelecode��ȡʧ��")
        train_location_all=re.compile(train_location_pat).findall(req7data)
        if(len(train_location_all)!=0):
            train_location=train_location_all[0]
        else:
            raise Exception("train_location��ȡʧ��")
        tokenall=re.compile(pattoken).findall(req7data)
        if(len(tokenall)!=0):
            token=tokenall[0]
        else:
            raise Exception("Token��ȡʧ��")
        keyall=re.compile(patkey).findall(req7data)
        if(len(keyall)!=0):
            key=keyall[0]
        else:
            raise Exception("key_check_isChange��ȡʧ��")
        #����Ҫ��ȡtrain_location
        pattrain_location="'tour_flag':'dc','train_location':'(.*?)'"
        train_locationall=re.compile(pattrain_location).findall(req7data)
        if(len(train_locationall)!=0):
            train_location=train_locationall[0]
        else:
            raise Exception("train_location��ȡʧ��")


        #�Զ�post��ַ4-��ȡ�˿���Ϣ
        getuserurl="https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs"
        getuserdata =urllib.parse.urlencode({
        "REPEAT_SUBMIT_TOKEN":token,
        }).encode('utf-8')
        req8 = urllib.request.Request(getuserurl,getuserdata)
        req8.add_header('User-Agent',user_agent)
        req8data=urllib.request.urlopen(req8).read().decode("utf-8","ignore")
        #��ȡ�û���Ϣ
        #��ȡ����
        namepat='"passenger_name":"(.*?)"'
        #��ȡ���֤
        idpat='"passenger_id_no":"(.*?)"'
        #��ȡ�ֻ���
        mobilepat='"mobile_no":"(.*?)"'
        #��ȡ��Ӧ�˿����ڵĹ���
        countrypat='"country_code":"(.*?)"'
        nameall=re.compile(namepat).findall(req8data)
        idall=re.compile(idpat).findall(req8data)
        mobileall=re.compile(mobilepat).findall(req8data)
        countryall=re.compile(countrypat).findall(req8data)
        #ѡ��˿�
        if(chooseno!="None"):
            pass
        else:
            #����˿���Ϣ�����ڿ����ж�λ�˿ͣ�����ͨ��ѭ�����
            for i in range(0,len(nameall)):
                print("��"+str(i+1)+"λ�û�,����:"+str(nameall[i]))
            chooseno=input("��ѡ��Ҫ��Ʊ���û�����ţ��˴�ֻ��ѡ��һλŶ������ѡ���λ�����������޸�һ�´���")
            #thisnoΪ��Ӧ�˿͵��±꣬�������1���������Ϊ1�ĳ˿����б��е��±�Ϊ0
            thisno=int(chooseno)-1
        if(trainzy[thiscode]=="��"):
            print("��ǰ��Ʊ��������ء�")
            continue
        #������1-����ύ����1-ȷ�϶���(�ڴ�ֻ��һ��������λ����ΪM������ѡ�����������λ�����������޸�һ�´���ʹ��if�ж�һ�¼���)
        checkOrderurl="https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"
        checkdata=urllib.parse.urlencode({
        "cancel_flag":2,
        "bed_level_order_num":"000000000000000000000000000000",
        "passengerTicketStr":"M,0,1,"+str(nameall[thisno])+",1,"+str(idall[thisno])+","+str(mobileall[thisno])+",N",
        "oldPassengerStr":str(nameall[thisno])+",1,"+str(idall[thisno])+",1_",
        "tour_flag":"dc",
        "randCode":"",
        "whatsSelect":1,
        "_json_att":"",
        "REPEAT_SUBMIT_TOKEN":token,
        }).encode('utf-8')
        req9 = urllib.request.Request(checkOrderurl,checkdata)
        req9.add_header('User-Agent', user_agent)
        req9data=urllib.request.urlopen(req9).read().decode("utf-8","ignore")
        print("ȷ�϶�����ɣ�����������һ��")
        #������2-����ύ����2-��ȡ����
        getqueurl="https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount"
        #checkdata=checkOrderdata.encode('utf-8')
        #������תΪ����ʱ��
        #�Ƚ��ַ���תΪ����ʱ���ʽ
        thisdatestr=date#��Ҫ����Ʊʱ��
        thisdate=datetime.datetime.strptime(thisdatestr,"%Y-%m-%d").date()
        #��תΪ��Ӧ�ĸ���ʱ��
        gmt='%a+%b+%d+%Y'
        thisgmtdate=thisdate.strftime(gmt)
        #��leftstr2ת��ָ����ʽ
        leftstr2=leftTicketStr.replace("%","%25")
                                #ע������%3A�ǣ�����urlencode�����Ľ��
        getquedata="train_date="+str(thisgmtdate)+"+00%3A00%3A00+GMT%2B0800&train_no="+train_no+"&stationTrainCode="+thiscode+"&seatType=M&fromStationTelecode="+fromStationTelecode+"&toStationTelecode="+toStationTelecode+"&leftTicket="+leftstr2+"&purpose_codes=00&train_location="+train_location+"&_json_att=&REPEAT_SUBMIT_TOKEN="+str(token)
        getdata=getquedata.encode('utf-8')
        req10 = urllib.request.Request(getqueurl,getdata)
        req10.add_header('User-Agent', user_agent)
        req10data=urllib.request.urlopen(req10).read().decode("utf-8","ignore")
        print("��ȡ����������ɣ�����������һ��")
        #������3-ȷ�ϲ���1-����ȷ���ύ
        confurl="https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
        confdata2=urllib.parse.urlencode({
        "passengerTicketStr":"M,0,1,"+str(nameall[thisno])+",1,"+str(idall[thisno])+","+str(mobileall[thisno])+",N",
        "oldPassengerStr":str(nameall[thisno])+",1,"+str(idall[thisno])+",1_",
        "randCode":"",
        "purpose_codes":"00",
        "key_check_isChange":key,
        "leftTicketStr":leftTicketStr,
        "train_location":train_location,
        "choose_seats":"",
        "seatDetailType":"000",
        "whatsSelect":"1",
        "roomType":"00",
        "dwAll":"N",
        "_json_att":"",
        "REPEAT_SUBMIT_TOKEN":token,
        }).encode('utf-8')
        req11 = urllib.request.Request(confurl,confdata2)
        req11.add_header('User-Agent', user_agent)
        req11data=urllib.request.urlopen(req11).read().decode("utf-8","ignore")
        print("����ȷ���ύ��ɣ�����������һ��")
        time1=time.time()
        while True:
            #������4-ȷ�ϲ���2-��ȡorderid
            time2=time.time()
            if((time2-time1)//60>5):
                print("��ȡorderid��ʱ�����ڽ�����һ������")
                break
            getorderidurl="https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random="+str(int(time.time()*1000))+"&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN="+str(token)
            req12 = urllib.request.Request(getorderidurl)
            req12.add_header('User-Agent', user_agent)
            req12data=urllib.request.urlopen(req12).read().decode("utf-8","ignore")
            patorderid='"orderId":"(.*?)"'
            orderidall=re.compile(patorderid).findall(req12data)
            if(len(orderidall)==0):
                print("δ��ȡ��orderid�����ڽ�����һ�ε�����")
                continue
            else:
                orderid=orderidall[0]
                break
        print("��ȡorderid��ɣ�����������һ��")
        #������5-ȷ�ϲ���3-������
        resulturl="https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue"
        resultdata="orderSequence_no="+orderid+"&_json_att=&REPEAT_SUBMIT_TOKEN="+str(token)
        resultdata2=resultdata.encode('utf-8')
        req13 = urllib.request.Request(resulturl,resultdata2)
        req13.add_header('User-Agent', user_agent)
        req13data=urllib.request.urlopen(req13).read().decode("utf-8","ignore")
        print("��������ɣ�����������һ��")
        try:
            #������6-ȷ�ϲ���4-֧���ӿ�ҳ��
            payurl="https://kyfw.12306.cn/otn//payOrder/init"
            paydata="_json_att=&REPEAT_SUBMIT_TOKEN="+str(token)
            paydata2=paydata.encode('utf-8')
            req14 = urllib.request.Request(payurl,paydata2)
            req14.add_header('User-Agent', user_agent)
            req14data=urllib.request.urlopen(req14).read().decode("utf-8","ignore")
            print("�����Ѿ�����ύ�������Ե�¼��̨����֧���ˡ�")
            break
        except Exception as err:
            break
    except Exception as err:
        print(err)

