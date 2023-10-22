from pyecharts.charts import Page

# 执行之前,请确保:1、已经把json文件放到本目录下 2、把json中的title和table的id替换掉
Page.save_resize_html(
    source="123.html",
    cfg_file="chart_config (2).json",
    dest="大屏_最终_3.html"
)
