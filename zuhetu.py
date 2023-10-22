import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map, Timeline, Pie, Page, Line, Graph,Geo
from pyecharts.globals import SymbolType, GeoType
import datetime
from pyecharts.globals import ThemeType
import numpy as np
from pyecharts.components import Table

# 全局设置主题颜色
theme_config = ThemeType.CHALK  # 颜色方案
# 表格和标题的颜色
table_color = ""
if theme_config == ThemeType.DARK:
    table_color = '#333333'
elif theme_config == ThemeType.CHALK:
    table_color = '#293441'
elif theme_config == ThemeType.PURPLE_PASSION:
    table_color = '#5B5C6E'
elif theme_config == ThemeType.ROMANTIC:
    table_color = '#F0E8CD'
elif theme_config == ThemeType.ESSOS:
    table_color = '#FDFCF5'
else:
    table_color = ''

data = pd.read_csv("yq.csv")  # 导入数据
# print(data)
temp = data['日期']
temp = data['日期']
Time = list(set(temp))
def get_list(date):  # 提取日期数据
    return datetime.datetime.strptime(date, "%Y.%m.%d").timestamp()
Time = sorted(Time, key=lambda date: get_list(date))  # 排序

# print(Time)
tl = Timeline(init_opts=opts.InitOpts(theme=theme_config, width="470px", height="400px", chart_id='time')).add_schema(
    play_interval=1000, height=40, is_loop_play=True, is_auto_play=False,
    control_position="left",
    is_rewind_play=False)  # 时间轴
data_pair = []
qz_list = []
wzz_list = []
lj_list = []

# h = 0
# for i, val in zip(Time, ['2022.9.28', '2022.9.29', '2022.9.30', '2022.10.1', '2022.10.2', '2022.10.3', '2022.10.4',
#                          '2022.10.5', '2022.10.6', '2022.10.7', '2022.10.8', '2022.10.9', '2022.10.10',
#                          '2022.10.11',
#                          '2022.10.12', '2022.10.13', '2022.10.14', '2022.10.15']):  # 以天为单位进行遍历
#     data_2 = data[data['日期'] == i]
#     h += int(data_2.sum()['新增本土确诊病例']) + int(data_2.sum()['新增本土无症状感染者'])
#     lj_list.append(h)
#     qz_list.append(int(data_2.sum()['新增本土确诊病例']))
#     wzz_list.append(int(data_2.sum()['新增本土无症状感染者']))

def map_plot():
    h = 0
    for i, val in zip(Time, ['2022.9.28', '2022.9.29', '2022.9.30', '2022.10.1', '2022.10.2', '2022.10.3', '2022.10.4',
                             '2022.10.5', '2022.10.6', '2022.10.7', '2022.10.8', '2022.10.9', '2022.10.10',
                             '2022.10.11',
                             '2022.10.12', '2022.10.13', '2022.10.14', '2022.10.15']):  # 以天为单位进行遍历
        data_2 = data[data['日期'] == i]
        h += int(data_2.sum()['新增本土确诊病例']) + int(data_2.sum()['新增本土无症状感染者'])
        lj_list.append(h)
        qz_list.append(int(data_2.sum()['新增本土确诊病例']))
        wzz_list.append(int(data_2.sum()['新增本土无症状感染者']))
        k = 0
        for j in data_2['地区']:
            data_3 = data_2[data_2['地区'] == j]
            k = int(data_3['新增本土确诊病例']) + int(data_3['新增本土无症状感染者'])
            data_pair.append((j, k))
        map = (Map(init_opts=opts.InitOpts(theme=theme_config, width="470px", height="400px", chart_id='map')))  # 画地图
        map.add("确诊病例",  # 系列名称，用于 tooltip 的显示，legend 的图例筛选。
                data_pair,  # 数据项 (坐标点名称，坐标点值)
                maptype='太原')  # 地图类型
        map.set_global_opts(  # 全局配置项
            title_opts=opts.TitleOpts(title='太原疫情地图'),  # title_opts = opts.TitleOpts()主标题函数
            visualmap_opts=opts.VisualMapOpts(  # visualmap_opts=opts.VisualMapOpts()视觉映射函数
                is_piecewise=True,  # 是否分段
                # 自定义的每一段的范围，以及每一段的文字，以及每一段的特别的样式。
                pieces=[{"max": 9, "min": 0, "label": "0-9", "color": "#FFECEC"},
                        {"max": 19, "min": 10, "label": "10-19", "color": "	#FFB5B5"},
                        {"max": 39, "min": 20, "label": "20-39", "color": "#ff7575"},
                        {"max": 79, "min": 40, "label": "40-79", "color": "#FF2D2D"},
                        {"max": 999, "min": 80, "label": "80-999", "color": "	#EA0000"}, ]), )
        tl.add(map, "{}新增病例".format(val))  # 将日期加入到timeline中
    return tl

def map_plot2():
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
    timeLine = Timeline(init_opts=opts.InitOpts(theme=theme_config, width="705px", height="400px", chart_id='time1'))
    timeLine.add_schema(is_auto_play=False)  # 开启自动播放模式

    for day in range(len(days)):
        ## 设置基本画布，地区为太原市  itemstyle_opts=opts.ItemStyleOpts(color='#b2d235', border_color='#111')
        geo = (Geo(opts.InitOpts(theme=theme_config, width="705px", height="400px"))
               .add_schema(maptype='太原',))
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
    #timeLine.render('check_timeline.html')
    return timeLine


area = data['地区']
areas = list(set(area))
num_list = []
for i in areas:
    data_4 = data[data['地区'] == i]
    # print(data_4)
    num_list.append((int(data_4.sum()['新增本土确诊病例']) + int(data_4.sum()['新增本土无症状感染者'])))
    # print(num_list)


def line_plot():
    line = (
        Line(init_opts=opts.InitOpts(theme=theme_config, width="470px", height="400px", chart_id='line1'))
        .add_xaxis(xaxis_data=Time)
        .add_yaxis("今日本土确诊人数", y_axis=qz_list, is_smooth=True)
        .add_yaxis("今日本土无症状感染者人数", y_axis=wzz_list, is_smooth=True)
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=""),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            # toolbox_opts=opts.ToolboxOpts(is_show=True, orient="vertical", pos_left="90%"),
        ))
    return line


def pie_plot():
    pie = (Pie(init_opts=opts.InitOpts(theme=theme_config, width="470px", height="400px", chart_id='pie1')))
    pie.add(
        series_name="累计确诊",
        radius=["40%", "55%"],
        data_pair=[list(z) for z in zip(areas, num_list)],
        label_opts=opts.LabelOpts(
            position="outside",
            formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
            background_color="#eee",
            border_color="#aaa",
            border_width=1,
            border_radius=4,
            rich={
                "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                "abg": {
                    "backgroundColor": "#e3e3e3",
                    "width": "100%",
                    "align": "right",
                    "height": 22,
                    "borderRadius": [4, 4, 0, 0],
                },
                "hr": {
                    "borderColor": "#aaa",
                    "width": "100%",
                    "borderWidth": 0.5,
                    "height": 0,
                },
                "b": {"fontSize": 16, "lineHeight": 33},
                "per": {
                    "color": "#eee",
                    "backgroundColor": "#334455",
                    "padding": [2, 4],
                    "borderRadius": 2,
                },
            },
        )
    )
    pie.set_global_opts(legend_opts=opts.LegendOpts(pos_left="left", orient="vertical"))
    pie.set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"))
    return pie


# def line_plot2():
#     line = (
#         Line(init_opts=opts.InitOpts(theme=theme_config, width="470px", height="400px", chart_id='line2'))
#         .add_xaxis(Time)
#         .add_yaxis("累计确诊人数", y_axis=lj_list)
#         .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
#         .set_global_opts(
#             title_opts=opts.TitleOpts(title=""),
#             tooltip_opts=opts.TooltipOpts(trigger="axis"),
#             toolbox_opts=opts.ToolboxOpts(is_show=True, orient="vertical", pos_left="90%", ),
#             xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False)
#         )
#     )
#     return line


def graph_plot():
    # 数据预处理 0代表是这条传播链的首例
    data = pd.read_csv('trace_new1.csv')  # 读入数据
    data = data[['病例号', '父代/首例']]  # 在此只需要使用这两列
    data = data.dropna(axis=0, how='all')  # 删除空行
    data['病例号'] = data['病例号'].astype(int)  # 将病例号改为int型数据

    data.duplicated('病例号')  # 查看重复值
    data.drop_duplicates('病例号', keep='last', inplace=True)  # 删除重复值
    data = data.reset_index(drop=True)  # 重设索引

    data['首例'] = data['父代/首例'].map(lambda x: x.split(',')[0])
    # 5,6,12,13  第一个为首例，最后一个为上一个节点，即病例13传播给本节点
    data['上个节点'] = data['父代/首例'].map(lambda x: x.split(',')[-1])

    data['首例'] = data['首例'].astype(int)  # 将float64型数据改为int型
    data['上个节点'] = data['上个节点'].astype(int)

    counts = data['首例'].value_counts()  # 计数：首例传染了多少个人
    # print(counts)
    nodes = []
    links = []
    categories = []

    # 每个首例设置成一个类别，不同的类别呈现不同的颜色
    fuli = data[data['首例'] == 0]
    # type(fuli)
    for index, row in fuli.iterrows():
        category = {'name': str(row['病例号'])}
        categories.append(category)
    # categories = [{}, {'name': '类1'}, {'name': '类2'}, {'name': '类3'}]

    # 循环生成结点和关系
    # 取数
    for i in data['病例号']:
        if i not in counts.keys():
            counts[i] = 0  # 某些首例没有传染人
        data_2 = data[data['病例号'] == i]
        data_2 = np.array(data_2)
        k = data_2[0:, 2]  # 当前结点
        before = data_2[0:, 3]  # 上一个结点
        # 生成结点
        if k[0] == 0:  # 如果是首例，大小根据传播的人数多少决定
            if counts[i].item() == 0:
                g = opts.GraphNode(name="病例" + str(i), symbol_size=20, category=str(i))
            elif 0 < counts[i].item() <= 3:
                g = opts.GraphNode(name="病例" + str(i), symbol_size=30, category=str(i))
            elif 3 < counts[i].item() <= 5:
                g = opts.GraphNode(name="病例" + str(i), symbol_size=40, category=str(i))
            elif 5 < counts[i].item() <= 10:
                g = opts.GraphNode(name="病例" + str(i), symbol_size=50, category=str(i))
            else:
                g = opts.GraphNode(name="病例" + str(i), symbol_size=65, category=str(i))
            # g = opts.GraphNode(name="病例" + str(i), symbol_size=30)

        else:  # 如果不是首例，大小都是20
            g = opts.GraphNode(name="病例" + str(i), symbol_size=20, category=str(k[0]))
            # g = opts.GraphNode(name="病例" + str(i), symbol_size=20)
        nodes.append(g)

        #  生成关系
        if k[0] != 0:
            h = opts.GraphLink(source="病例" + str(before[0]), target="病例" + str(i))
            links.append(h)

    # 画出关系图
    c = (
        Graph(init_opts=opts.InitOpts(theme=theme_config, width="705px", height="400px", chart_id='graph'))
        .add("", nodes, links, repulsion=50, categories=categories)
        # .add("", nodes, links, repulsion=50,itemstyle_opts=itemstyle_opts)
        .set_global_opts(legend_opts=opts.LegendOpts(is_show=False),
                         title_opts=opts.TitleOpts(title="病例关系图"))
        #.render("病例关系图.html")
    )

    return c


def make_title(v_title):
    table = Table()
    table.add(headers=[v_title], rows=[], attributes={
        "align": "center",
        "border": False,
        "padding": "2px",
        "style": "background:{}; width:1410px; height:50px; font-size:25px; color:#FFFFFF;".format(table_color)
    })
    return table


def page_plot():
    page = Page(layout=Page.DraggablePageLayout, page_title="疫情数据大屏")
    page.add(
        make_title(v_title='疫情轨迹可视化分析'),
        map_plot2(),
        map_plot(),
        pie_plot(),
        line_plot(),
        #line_plot2(),
        graph_plot(),
    )
    return page


page_plot().render('123.html')
