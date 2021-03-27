import requests


class Search_for_suggestions():  # 搜索建议
    def __init__(self):
        self.url_bing = 'https://api.bing.com/qsonhs.aspx?type=cb&q={}'
        self.url_baidu = 'http://suggestion.baidu.com/su?wd={}'
        self.url_360 = 'https://sug.so.360.cn/suggest?encodein=utf-8&encodeout=utf-8&format=json&word={}'
        self.hd = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    def get_suggestions(self, content):
        url = self.url_baidu.format(content)
        sugges = requests.get(url, self.hd)
        content = sugges.text.split(',')
        content[2] = content[2].replace('s:[', '')
        content[-1] = content[-1].replace(']});', '')
        content_list = []
        for i in range(2, len(content)):
            content_list.append(content[i].replace('"', ''))
        return content_list
