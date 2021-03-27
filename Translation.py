import requests
import urllib
import json


def translation_token(a):

    def int_overflow(val):
        maxint = 2147483647
        if not -maxint-1 <= val <= maxint:
            val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
        return val

    def unsigned_right_shitf(n, i):
        n &= 0xffffffff
        return n >> i

    def TL(a):
        k = ""
        b = 406644
        b1 = 3293161072

        _b = "+-a^+6"
        Zb = "+-3^+b+-f"

        e = []
        for g in range(len(a)):
            m = ord(a[g])
            if 128 > m:
                e.append(m)
            else:
                if 2048 > m:
                    e.append(m >> 6 | 192)
                else:
                    if (55296 == (m & 64512)) and (g + 1) < len(a) and (56320 == ord(a[g + 1]) & 64512):
                        m = 65536 + ((m & 1023) << 10) + ord(a[g]) & 1023
                        e.append(m >> 18 | 240)
                        e.append(m >> 12 & 63 | 128)
                    else:
                        e.append(m >> 12 | 224)
                        e.append(m >> 6 & 63 | 128)
                        e.append(m & 63 | 128)

        a = b
        for f in range(len(e)):
            a += e[f]
            a = RL(a, _b)
        a = RL(a, Zb)
        a = a & 0xffffffff if 0 > a else a
        a = a ^ b1
        if 0 > a:
            a = (a & 2147483647) + 2147483648
        a %= 1E6
        float_part = str(int((int(a) ^ int(b))))
        return f"{int(a)}.{float_part}"

    def RL(a, b):
        t = "a"
        Yb = "+"
        c = 0
        while c < len(b) - 2:
            d = b[c+2]
            d = ord(d[0])-87 if d >= t else int(d)
            d = unsigned_right_shitf(
                a, d) if b[c+1] == Yb else int_overflow(a << d)
            a = a + \
                int_overflow(
                    d & 0xffffffff) if b[c] == Yb else int_overflow(a ^ d)
            c += 3

        return a

    return TL(a)


class Translation():  # 谷歌翻译
    def translat(self, txt):
        ischinses = 0
        isparagraph = 0
        if '\n' in txt:
            isparagraph = 1
        for ch in txt:
            if '\u4e00' <= ch <= '\u9fff':
                ischinses = 1
                break
        if isparagraph:
            if ischinses:
                return self.tranlate_caiyun(txt, "auto2en")
            else:
                return self.tranlate_caiyun(txt, "auto2zh")
        else:
            if ischinses:
                all_ret = self.cn_to_en(txt)
                # [0]表示结果是单词(0)还是句子(1)还是未查询到(-1), 段落(2)
        # ----单词---
            # [1,2,3]表示翻译的结果 [1,2,3][0]是词性
            # [1,2,3][1][0]是原文
                # [1,2,3][1][1]是查询结果
        # -----句子-----
                # [1][0]拼音
                # [1][1,2,3] 句子
        # -----段落-----
                # [1][0]  翻译的结果
                return self.parse_ret(all_ret)
            else:
                all_ret = self.en_to_cn(txt)
                return self.parse_ret(all_ret)

    def tranlate_caiyun(self, source, direction):
        url = "http://api.interpreter.caiyunai.com/v1/translator"
        # WARNING, this token is a test token for new developers, and it should be replaced by your token
        token = "7msav8n2mm7p9rolkysq"
        payload = {
            "source": source,
            "trans_type": direction,
            "request_id": "demo",
            "detect": True,
        }

        headers = {
            'content-type': "application/json",
            'x-authorization': "token " + token,
        }

        response = requests.request("POST", url, data=json.dumps(
            payload), headers=headers, timeout=5)

        # return json.loads(response.text)['target']
        return [2, [json.loads(response.text)['target']]]

    def buildUrl(self, content, tk, tl):
        baseUrl = 'http://translate.google.cn/translate_a/single'
        baseUrl += '?client=webapp&'
        baseUrl += 'sl=auto&'
        baseUrl += 'tl=' + str(tl) + '&'
        baseUrl += 'hl=zh-CN&'
        baseUrl += 'dt=at&'
        baseUrl += 'dt=bd&'
        baseUrl += 'dt=ex&'
        baseUrl += 'dt=ld&'
        baseUrl += 'dt=md&'
        baseUrl += 'dt=qca&'
        baseUrl += 'dt=rw&'
        baseUrl += 'dt=rm&'
        baseUrl += 'dt=ss&'
        baseUrl += 'dt=t&'
        baseUrl += 'ie=UTF-8&'
        baseUrl += 'oe=UTF-8&'
        baseUrl += 'clearbtn=1&'
        baseUrl += 'otf=1&'
        baseUrl += 'pc=1&'
        baseUrl += 'srcrom=0&'
        baseUrl += 'ssel=0&'
        baseUrl += 'tsel=0&'
        baseUrl += 'kc=2&'
        baseUrl += 'tk=' + str(tk) + '&'
        baseUrl += 'q=' + content
        return baseUrl

    def open_url(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        r = requests.get(url, headers=headers, timeout=3)
        return r

    def en_to_cn(self, txt):

        # tl是要翻译的目标语种，值参照ISO 639-1标准，如果翻译成中文"zh/zh-CN简体中文"
        tl = "zh-CN"

        chinese_txt = txt
        tk = translation_token(chinese_txt)

        content = urllib.parse.quote(chinese_txt)
        url = self.buildUrl(content, tk, tl)
        result = self.open_url(url)
        r_json = json.loads(result.text)
        return r_json

    def cn_to_en(self, txt):

        # tl是要翻译的目标语种
        tl = "en"

        chinese_txt = txt
        tk = translation_token(chinese_txt)

        content = urllib.parse.quote(chinese_txt)
        url = self.buildUrl(content, tk, tl)
        result = self.open_url(url)
        r_json = json.loads(result.text)
        return r_json

    def parse_ret(self, all_ret):
        translation_results = [0]
        for i in range(3):  # 先以单词的格式清洗
            try:
                speech = all_ret[1][i][0]  # 词性
                single_list = all_ret[1][i][2]
                to_clean_list = [speech]
                for word_list in single_list:
                    source_word = word_list[0]
                    frequency = word_list[-1]
                    goal_word_list = word_list[1]
                    goal_words = ''
                    for goal_word in goal_word_list:
                        goal_words += goal_word+','
                    try:
                        item = [source_word, goal_words,
                                f'{frequency*100:.2f}%']
                    except:
                        item = [source_word, goal_words, '无数据']
                    to_clean_list.append(item)
                translation_results.append(to_clean_list)
            except:
                pass

        if translation_results == [0]:  # 如果不是单词,则以句子的格式清洗
            try:
                pinyin = all_ret[0][1][-1]
                to_clean_list = [pinyin]
                for i in range(3):
                    try:
                        sentence = all_ret[5][0][2][i][0]
                        to_clean_list.append(sentence)
                    except:
                        pass
                translation_results = [1]
                translation_results.append(to_clean_list)
            except:
                translation_results = [-1, '没有查询到单词或者句子']

        return translation_results
        # [0]表示结果是单词(0)还是句子(1)还是未查询到(-1),
    # ----单词---
        # [1,2,3]表示翻译的结果 [1,2,3][0]是词性
        # [1,2,3][1][0]是原文
        # [1,2,3][1][1]是查询结果
     # -----句子-----
        # [1][0]拼音
        # [1][1,2,3] 句子


# t = Translation()
# r = t.translat("happy")
# print(len(r))
