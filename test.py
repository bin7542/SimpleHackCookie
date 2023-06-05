from SimpleHackCookie.CookieHack import BILIBILI # cookie利用类

if __name__ == '__main__':
    bilibili = BILIBILI() # 实例化 实例化的时候会自动获取所有浏览器的cookie
    # bilibili.print_user_info() # 用户信息
    # bilibili.init() # 从新初始化

    bilibili.like('BV1fe4y1k7UD') # 点赞
    bilibili.comment('BV1fe4y1k7UD', '233333') # 评论

    