import requests
import urllib3
import webbrowser
import datetime
urllib3.disable_warnings()
# 请求头部信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer #这里打开网页https://zsb.hneao.cn/ks/home'
                     '右键检查后打开网络选项，在学校名称里面随便选择一项，在名为getMajorList标头下复制Authorization:的全部内容'
}

# 待查询学校列表（从JSON中读取）
schools = [{"name": "吉首大学", "id": "48"},
           {"name": "湖南农业大学", "id": "51"},
           {"name": "中南林业科技大学", "id": "52"},
           {"name": "湖南中医药大学", "id": "94"},
           {"name": "湖南理工学院", "id": "53"},
           {"name": "湘南学院", "id": "54"},
           {"name": "衡阳师范学院", "id": "55"},
           {"name": "怀化学院", "id": "57"},
           {"name": "湖南文理学院", "id": "58"},
           {"name": "湖南科技学院", "id": "59"},
           {"name": "湖南人文科技学院", "id": "91"},
           {"name": "湖南工商大学", "id": "60"},
           {"name": "长沙学院", "id": "63"},
           {"name": "湖南工程学院", "id": "64"},
           {"name": "湖南城市学院", "id": "65"},
           {"name": "湖南工学院", "id": "66"},
           {"name": "湖南财政经济学院", "id": "67"},
           {"name": "湖南警察学院", "id": "68"},
           {"name": "湖南工业大学", "id": "69"},
           {"name": "湖南女子学院", "id": "70"},
           {"name": "湖南第一师范学院", "id": "93"},
           {"name": "湖南医药学院", "id": "71"},
           {"name": "湖南涉外经济学院", "id": "72"},
           {"name": "湘潭大学兴湘学院", "id": "73"},
           {"name": "湖南工业大学科技学院", "id": "74"},
           {"name": "湘潭理工学院", "id": "77"},
           {"name": "中南林业科技大学涉外学院", "id": "79"},
           {"name": "湖南文理学院芙蓉学院", "id": "80"},
           {"name": "湖南理工学院南湖学院", "id": "81"},
           {"name": "衡阳师范学院南岳学院", "id": "82"},
           {"name": "湖南工程学院应用技术学院", "id": "83"},
           {"name": "湖南中医药大学湘杏学院", "id": "84"},
           {"name": "吉首大学张家界学院", "id": "85"},
           {"name": "长沙师范学院", "id": "87"},
           {"name": "湖南应用技术学院", "id": "88"},
           {"name": "湖南信息学院", "id": "89"},
           {"name": "湖南交通工程学院", "id": "92"},
           {"name": "湖南软件职业技术大学", "id": "90"}]   # 可以根据实际情况添加更多学校

# 存储学校专业信息
school_info = {}

for school in schools:
    data = {"pch": None, "zsjhid": school["id"], "zylx": "1"}

    # 发起POST请求
    response = requests.post('https://zsb.hneao.cn/api/bmZy/getMajorList', headers=headers, json=data, verify=False)

    if response.status_code == 200:
        result = response.json()

        if result.get("code") == 200:
            school_info[school["name"]] = result.get("data", [])
            print("正在爬取", school_info[school["name"]], "请稍等......")
        else:
            print(f"请求失败：{result.get('msg')}")
    else:
        print(f"请求失败，状态码：{response.status_code}")

# 生成HTML页面
html_content = "<html><head><title>学校专业信息</title></head><body>" +'上一次和更新时间:'+ datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
for school_name, majors in school_info.items():
    html_content += f"<h2>{school_name}</h2>"
    html_content += "<ul>"

    for major in majors:
        if float(major.get('applyNum')) == 0:
            continue
        html_content += f"<li>专业名称: {major.get('zymc')}，招生人数: {major.get('zsjhs')}，报名人数: {major.get('applyNum')}， 报录比: {int(float(major.get('zsjhs'))/float(major.get('applyNum'))*10000)/100}%</li>"
    html_content += "</ul>"

html_content += "</body></html>"

# 将HTML内容保存到文件中
with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("HTML页面已生成，可查看 index.html 文件")
f = open('index.html','r')
webbrowser.open_new_tab('index.html')