from pyecharts import Geo,Style
import urllib3
import lxml.html
import pandas as pd

def getdetailinfo(roomurl):
    info = []
    geo_cities_coords = {}
    http = urllib3.PoolManager()
    response = http.request('GET',roomurl)
    data = response.data.decode('utf-8')
    allinfo = catchinfo(data,'//table[@class="speed-table1"]/tr/td/text()')
    didian = catchinfo(data,'//table[@class="speed-table1"]/tr/td[6]/a/text()')

    i = 0
    for m in range(len(didian)):
        a = (didian[m],"震级"+allinfo[i]+"时间"+allinfo[i+1]+"深度"+allinfo[i+4])
        info.append(a)
        i = i + 5
    n = 0
    for j in range(len(didian)):
        geo_cities_coords[didian[j]]= [allinfo[n+3], allinfo[n+2]]
        n = n + 5

    #print(info)
    print(geo_cities_coords)
    data = pd.DataFrame(info)
    data.columns = ['city', 'info']
    attr = data['city']
    value = data['info']
    geo.add("地震的地区：", attr, value, symbol_size=3, item_color="#fff", maptype='world', geo_cities_coords=geo_cities_coords)







def catchinfo(data,xpath):
    etree = lxml.html.etree
    content = etree.HTML(data)
    info = content.xpath(xpath)
    return info

style = Style(title_color="#fff",title_pos="center",width=1200,height=600,background_color="#404a59")
geo = Geo('近一年世界地震图', **style.init_style)
k = 1
while(k<42) :
    ks = "http://www.ceic.ac.cn/speedsearch?time=6&&page=" + str(k)
    getdetailinfo(ks)
    k =k+1


geo.render()