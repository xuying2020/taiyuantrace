import webbrowser
from pyecharts.charts import Graph
from pyecharts import options as opts
import pandas as pd
import numpy as np

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
    Graph()
    .add("", nodes, links, repulsion=50, categories=categories)
    # .add("", nodes, links, repulsion=50,itemstyle_opts=itemstyle_opts)
    .set_global_opts(legend_opts=opts.LegendOpts(is_show=False),
                     title_opts=opts.TitleOpts(title="病例关系图"))
    .render("病例关系图.html")
)

webbrowser.open("病例关系图.html")
