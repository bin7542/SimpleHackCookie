# cookie利用
import requests
import browser_cookie3

# GET_COOKIE
def get_cookie(browser='edge', url='https://www.bilibili.com/'):
    """
    :param browser: 'edge' or 'chrome' or 'firefox'
    :return: {}
    """
    cj = None
    if browser == 'edge':
        try:
            cj = browser_cookie3.edge()
        except:
            return None
    elif browser == 'chrome':
        try:
            cj = browser_cookie3.chrome()
        except:
            return None
    elif browser == 'firefox':
        try:
            cj = browser_cookie3.firefox()
        except:
            return None
    try:
        r = requests.get(url, cookies=cj, headers={'User-Agent': 'Mozilla/5.0'})
    except:
        return None
    if not r.status_code == 200:
        return None
    res = {}
    for item in cj:
        res[item.name] = item.value
    return res


# 筛出bilibili请求所需的cookie
def get_cookie_filter(cookie_dict, website="bilibili"):
    cookie_str = ""
    if website == "bilibili":
        bilibili_key = [
            "buvid4",
            "b_nut",
            "b_lsid",
            "buvid3",
            "i-wanna-go-back",
            "_uuid",
            "FEED_LIVE_VERSION",
            "home_feed_column",
            "browser_resolution",
            "buvid_fp",
            "header_theme_version",
            "PVID",
            "SESSDATA",
            "bili_jct",
            "DedeUserID",
            "DedeUserID__ckMd5",
            "b_ut",
            "CURRENT_FNVAL",
            "sid",
            "rpdid"
        ]
        """
         
        """
        # print(cookie_dict)
        for key in bilibili_key:
            try:
                cookie_str += (key + "=" + cookie_dict[key] + ";")
            except:
                pass
    return cookie_str


# 公共变量
# 请求头
request_headers = {
    "UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37"
}


# BILIBILI
class BILIBILI():
    """
    :param browser: 'edge' or 'chrome' or 'firefox' or 'all'
    """
    def __init__(self) -> None:
        self.url = 'https://www.bilibili.com/'
        self.cookie = {} # cookie列表 一个cookie字典为一个元素
        self.users = [] # 用户列表
        self.init()

    def print_(self, flag):
        if flag['edge']:
            print("\033[32m edge \033[0m", end="")
        else:
            print("\033[31m edge \033[0m", end="")
        if flag['chrome']:
            print("\033[32m chrome \033[0m", end="")
        else:
            print("\033[31m chrome \033[0m", end="")
        if flag['firefox']:
            print("\033[32m firefox \033[0m")
        else:
            print("\033[31m firefox \033[0m")
        
    # 初始化
    def init(self):
        # 获取cookie
        self.cookie['edge'] = get_cookie('edge', self.url)
        self.cookie['chrome'] = get_cookie('chrome', self.url)
        self.cookie['firefox'] = get_cookie('firefox', self.url)
        # 如果都是None 则报错
        if not any(self.cookie.values()):
            raise Exception("\033[31mERROR>>\033[0m Get Cookie Failed! ALL BROWSER IS NONE! Maybe you need to login first!")
        
        user_flag = {
            'edge': False,
            'chrome': False,
            'firefox': False,
        }
        
        # 不换行
        print("\033[32mINFO>>\033[0m Get Cookie Success!" + " ", end="")
        if self.cookie['edge'] != None:
            user_flag['edge'] = True
        else:
            user_flag['edge'] = False
        if self.cookie['chrome'] != None:
            user_flag['chrome'] = True
        else:
            user_flag['chrome'] = False
        if self.cookie['firefox'] != None:
            user_flag['firefox'] = True
        else:
            user_flag['firefox'] = False
        
        self.print_(user_flag)
        # 获取用户
        for browser in self.cookie.keys():
            if self.cookie[browser] != None:
                user_info = {}
                try:
                    r = requests.get('https://api.bilibili.com/x/space/myinfo', headers=request_headers, cookies=self.cookie[browser])
                    r_json = r.json()['data']
                    user_info = {
                        'name': r_json['name'],
                        'sex': r_json['sex'],
                        'face': r_json['face'],
                        'sign': r_json['sign'],
                        'level': r_json['level'],
                        'coins': r_json['coins'],
                        'follower': r_json['follower'],
                    }
                    r.json()['data']
                except:
                    pass
                    
                try:
                    self.users.append({
                        'browser': browser,
                        'userID': self.cookie[browser]['DedeUserID'],
                        'userInfo': user_info,
                        'cookie': self.cookie[browser],
                    })
                except:
                    # 用户登陆过 但退出登录了
                    print(f"\033[33mWARNING>>\033[0m {browser} Cookie Success But No User! Maybe User Logout!")
                    user_flag[browser] = False
        print("\033[32mINFO>>\033[0m Verify Cookie Success!" + " ", end="")
        self.print_(user_flag)

    # B站 BV号转aid
    def bv2aid(self, bv):
        """
        B站 BV号转aid
        :param bv: BV号
        :return: aid
        """
        url = 'https://api.bilibili.com/x/web-interface/view'
        params = {
            "bvid": bv
        }
        try:
            r = requests.get(url, params=params)
        except:
            return None
        if r.status_code == 200:
            try:
                return r.json()["data"]["aid"]
            except:
                return None
        else:
            return None

    # 输出用户信息
    def print_user_info(self):
        for user in self.users:
            print(f"\033[34mUserInfo>>\033[0m Browser: {user['browser']} UserName: {user['userInfo']['name']} UserID: {user['userID']}")

    # 筛出bilibili请求所需的cookie
    def get_cookie_filter(self, cookie_dict):
        cookie_str = ""
        bilibili_key = [
            "buvid4",
            "b_nut",
            "b_lsid",
            "buvid3",
            "i-wanna-go-back",
            "_uuid",
            "FEED_LIVE_VERSION",
            "home_feed_column",
            "browser_resolution",
            "buvid_fp",
            "header_theme_version",
            "PVID",
            "SESSDATA",
            "bili_jct",
            "DedeUserID",
            "DedeUserID__ckMd5",
            "b_ut",
            "CURRENT_FNVAL",
            "sid",
            "rpdid"
        ]
        """
        buvid4=2879D279-8442-8C79-6E99-DECB7512786B03101-023052500-AlUNeUTKz0yQwMSOusFe5Q%3D%3D; b_nut=1685760399; b_lsid=2159BB109_1887F2656ED; buvid3=07601FC9-9720-FC0B-DD5B-CAF83FE50F7699593infoc; i-wanna-go-back=-1; _uuid=67EAA910C-669A-210F7-81031-6F9C1011048103699686infoc; FEED_LIVE_VERSION=V8; home_feed_column=5; browser_resolution=1920-511; buvid_fp=9e6b2a0a9f2ab5b3823c26e418e3bc4c; header_theme_version=CLOSE; PVID=1; SESSDATA=a384d195%2C1701312635%2Cad7de%2A61; bili_jct=79cb61886d507badd9fbc81b43535b46; DedeUserID=1870412606; DedeUserID__ckMd5=3f430f1f0a24f56b; b_ut=5; CURRENT_FNVAL=4048; sid=5m48wpir; rpdid=|(u))|YJ)R|~0J'uY)l~Y|YRl
        """
        # print(cookie_dict)
        for key in bilibili_key:
            try:
                cookie_str += (key + "=" + cookie_dict[key] + ";")
            except:
                pass
        return cookie_str

    # 点赞
    def like(self, bv):
        """
        :param bv: BV号
        """
        aid = self.bv2aid(bv)
        if not aid:
            print("\033[31mERROR>>\033[0m BV ERROR!")
            return
        
        for i in self.users:
            cookie_dict = i['cookie']
            url = 'https://api.bilibili.com/x/web-interface/archive/like'
            params = {
                "aid": aid,
                "like": 1,
                "csrf": cookie_dict["bili_jct"]
            }
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Cookie": self.get_cookie_filter(cookie_dict)
            }
            r = requests.post(url, params=params, headers=headers)
            if r.status_code == 200:
                print(f"userID: {cookie_dict['DedeUserID']} UserName: {i['userInfo']['name']} Like Success!")
            else:
                print("\033[31mERROR>>\033[0m UserID: {cookie_dict['DedeUserID']} UserName: {i['userInfo']['name']} Like Failed!")

    # 投币
    def coin(self, bv):
        aid = self.bv2aid(bv)
        if not aid:
            print("\033[31mERROR>>\033[0m BV ERROR!")
            return
        for i in self.users:
            cookie_dict = i['cookie']
            url = 'https://api.bilibili.com/x/web-interface/coin/add'
            params = {
                "aid": aid,
                "multiply": 2,
                "select_like": 1,
                "cross_domain": "true",
                "csrf": cookie_dict["bili_jct"]
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57",
                "referer": f"https://www.bilibili.com/video/BV1R24y1N7ja", # csrf验证必须要有referer
                "Cookie": get_cookie_filter(cookie_dict, "bilibili")
            }
            r = requests.post(url, data=params, headers=headers)
            if r.status_code == 200:
                print(f"userID: {cookie_dict['DedeUserID']} UserName: {i['userInfo']['name']} Coin Success!")
            else:
                print("\033[31mERROR>>\033[0m UserID: {cookie_dict['DedeUserID']} UserName: {i['userInfo']['name']} Coin Failed!")

    # 评论
    def comment(self, bv, msg):
        # 评论
        aid = self.bv2aid(bv)
        if not aid:
            print("\033[31mERROR>>\033[0m BV ERROR!")
            return
        for i in self.users:
            cookie_dict = i['cookie']
            url = 'https://api.bilibili.com/x/v2/reply/add'
            params = {
                "oid": aid,
                "type": 1,
                "message": msg,
                "plat": 1,
                "jsonp": "jsonp",
                "csrf": cookie_dict["bili_jct"]
            }
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Cookie": get_cookie_filter(cookie_dict, "bilibili")
            }
            r = requests.post(url, params=params, headers=headers)
            if r.status_code == 200:
                print(f"userID: {cookie_dict['DedeUserID']} UserName: {i['userInfo']['name']} Comment Success!")
            else:
                print("\033[31mERROR>>\033[0m UserID: {cookie_dict['DedeUserID']} UserName: {i['userInfo']['name']} Comment Failed!")

    # BAN号
    def ban(self):
        pass
