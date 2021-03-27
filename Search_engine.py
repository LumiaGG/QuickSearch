from PIL import Image, ImageTk

search_engine_urls = ["http://www.bing.com/search?q={}", "translation",
                      "https://www.google.com/search?q={}", "https://www.baidu.com/s?word={}"]
search_engine_logos_path = [r'D:\code_lib_python\快速搜索\search\icon\bing_logo.png', r'D:\code_lib_python\快速搜索\search\icon\google_翻译_logo.png',
                            r'D:\code_lib_python\快速搜索\search\icon\google.png', r'D:\code_lib_python\快速搜索\icon\baidu.png']
search_engine_names = ["bing", "google翻译", "google", "baidu"]


class Search_engine():
    def __init__(self):
        self.search_engines_num = len(search_engine_urls)
        self.search_engines = []

        for i, url in enumerate(search_engine_urls):
            self.search_engines.append(
                {"url": url, "name": search_engine_names[i]})

        self.cur_engine = self.search_engines[0]

    def load_img(self):
        for i, logo in enumerate(search_engine_logos_path):
            logo_img = Image.open(logo)
            self.search_engines[i]["logo"] = ImageTk.PhotoImage(
                logo_img.resize((30, 30)), Image.ANTIALIAS)
            self.search_engines[i]["logo_big"] = ImageTk.PhotoImage(
                logo_img.resize((40, 40)), Image.ANTIALIAS)

    def swap_search_engin(self):
        self.search_engines.append(self.search_engines[0])
        self.search_engines.pop(0)
        self.cur_engine = self.search_engines[0]


search_engine = Search_engine()
