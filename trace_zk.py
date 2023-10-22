from pyecharts import options as opts
from pyecharts.charts import Geo, Timeline
from pyecharts.globals import SymbolType, GeoType
import pandas as pd
import datetime
import webbrowser

# *** 数据预处理 ***##
CovidTaiYuan_09 = pd.read_csv('trace_new1.csv')
CovidTaiYuan_09 = CovidTaiYuan_09.iloc[:, [0, 4, 8, 9]]  # 病例号、时间（年/月/日）、经度、纬度
CovidTaiYuan_09 = CovidTaiYuan_09.dropna(axis=0, how='all')  # 删除空行
# 首先以日期为索引，找到不同日期下的所有病例
temp_day = CovidTaiYuan_09['日期']
days = list(set(temp_day))  # 日期去重


def get_list(date):  # 提取日期数据
    return datetime.datetime.strptime(date, "%Y/%m/%d").timestamp()


days = sorted(days, key=lambda date: get_list(date))  # 排序

##*** 绘制确诊病例活动轨迹曲线轮播图 ***##
timeLine = Timeline()
timeLine.add_schema(is_auto_play=True)  # 开启自动播放模式

for day in range(len(days)):
    ## 设置基本画布，地区为太原市
    geo = (Geo(opts.InitOpts(width="1200px", height="600px")).add_schema(maptype='太原',
                                                                         itemstyle_opts=opts.ItemStyleOpts(
                                                                             color='#b2d235', border_color='#111')))
    ## 设置全局选项：标题、标题与左侧距离；开启图例、模式为scroll、可以选择多个图例、与左侧距离、竖向排列
    geo.set_global_opts(
        title_opts=opts.TitleOpts(title='太原市确诊病例活动轨迹图', pos_left="center"),
        legend_opts=opts.LegendOpts(is_show=True, type_='scroll', selected_mode="multiple", pos_left='left',
                                    orient='vertical'))
    ## 读取当日所有病例信息
    dataByday = CovidTaiYuan_09[CovidTaiYuan_09['日期'] == days[day]]
    ## 开始绘制当日每个病例的活动轨迹图
    temp_case = dataByday['病例号'].astype('int')  # 读取所有病例号
    ID = list(set(temp_case))  # 日期去重
    for id in range(len(ID)):
        dataByid = dataByday[dataByday['病例号'] == ID[id]]  # 读取当日下该病例的信息
        pairs = []  # 地点对
        if len(dataByid) != 1:  # 判断该病例当日是否只在一个地方活动
            for i in range(len(dataByid) - 1):
                ## 读取该病例当日活动轨迹时间对及活动地点经纬度
                geo.add_coordinate('时间' + str(i), dataByid.iloc[i]['经度'], dataByid.iloc[i]['纬度'])
                geo.add_coordinate('时间' + str(i + 1), dataByid.iloc[i + 1]['经度'], dataByid.iloc[i + 1]['纬度'])
                pairs.append(('时间' + str(i), '时间' + str(i + 1)))
                ## 绘制活动轨迹曲线
                geo.add('病例' + str(ID[id]), pairs, type_=GeoType.LINES,
                        effect_opts=opts.EffectOpts(symbol=SymbolType.ARROW, symbol_size=5, color='red'),
                        label_opts=opts.LabelOpts(is_show=False),
                        linestyle_opts=opts.LineStyleOpts(curve=0.2))  # 绘制两点之间的连线
            else:
                geo.add_coordinate('时间' + str(0), dataByid.iloc[0]['经度'], dataByid.iloc[0]['纬度'])
                geo.add_coordinate('时间' + str(1), dataByid.iloc[0]['经度'], dataByid.iloc[0]['纬度'])
                pairs.append(('时间' + str(0), '时间' + str(1)))
                geo.add('病例' + str(ID[id]), pairs, type_=GeoType.LINES,
                        effect_opts=opts.EffectOpts(symbol=SymbolType.ARROW, symbol_size=5, color='red'),
                        label_opts=opts.LabelOpts(is_show=False),
                        linestyle_opts=opts.LineStyleOpts(curve=0.2))
    ## 将绘制的当日活动轨迹图添加到timeLine中
    timeLine.add(geo, str(days[day]))
timeLine.render('check_timeline.html')
webbrowser.open("check_timeline.html")
