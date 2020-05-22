# shopServer


使用说明
修改全局地址配置信息
1. shopServer/shopApp/mytool/__init__.py 中 global_domain 方法的返回值
2. shopServer/shopApp/static/myfile/login.html 中 window.my_global_host_url = '你的域名'
3. shopServer/templates/base.html 中 window.my_global_host_url = "你的域名"

如需完成及时通讯功能, 该项目采用的是环信第三方及时通信,
1. shopServer/shopApp/mytool/__init__.py 中 server_str 方法的返回值为 环信通信的客服端的id标示符
2. shopServer/shopApp/static/js/tool.js 中 var my_IM_server = '环信通信的客服端的id标示符'
3. shopServer/shopApp/static/js/webim.config.js 中 appkey: '环信第三方的appKey值'
4. shopServer/templates/base.html 中 window.huanxin_server_id = '环信通信的客服端的id标示符'

数据库配置信息在  shopServer/settings.py 文件中


微商城后台管理系统



希望大家按时完工 保证质量

已完成 bug1: 用户在删除的时候 应该将用户的头像和该用户的二维码 也从服务器中删除 -----张潇港

bug2： 用户注册成功 通过userid自动为该用户生成一个二维码图片 并将路径保存到数据库 ----黄景召

bug3： 用户在修改头像的时候 用户原理的头像图片应该从服务器中删除掉 ----王贺

bug4： 会员管理界面 查询按钮完成之后  应该将输入框中的东西清空掉 ----王泽华

bug5： 会员管理 编辑按钮功能界面 头像的编辑 应该是修改用户头像 要用文件提交的方式 ----陈云飞

已解决 bug6： 会员管理界面 添加会员的时候 会默认生成好多会员  ----- 不知道谁、  

bug7： 会员管理界面 分页功能  --- 刘斌

已完成bug8： 会员管理界面 当查询结果为空的时候  应该提示用户 --- 张潇港

bug9： 会员管理界面 查询功能 输入用户a的名字 输入用户b的电话号码 找不到内容  

bug10： 好友表 增 删 查 ----张静




bug11: 商品列表界面 序号后面 增加一个 商品id 并显示   and    序号字段要按照1 ， 2 ， 3.。。。来显示  ----胡亚洲

bug12： 商品列表界面 图文信息  只保留一个 “+” 按钮就行   --- 胡亚洲

bug13： 商品列表界面 整个界面数据的排序 应该按照添加时间来排序   ---- 胡亚洲

bug14： 编辑商品的时候 整个界面的标题应该提示城 编辑商品 而不是 商品添加  ---- 陈云飞

已完成bug15： 商品列表界面  商品查询完毕之后 应该增加相应的提示框来告诉用户提示信息  ---- 张潇港

bug16： 商品列表界面  增加一个按钮 可以方便用户快速实现 按时间降序 或 升序 功能来排列商品  ----- 胡亚洲 

bug17： 商品列表界面  查询完之后的分页显示和功能方面没有优化 -----  吕建伟

bug18： 轮播图界面  序号和顺序都是1  需要修改   ---- 刘斌

bug19： 轮播图假面 删除按钮实现了  但是编辑按钮不管用 需要实现  ---- 刘斌

bug20： 轮播图界面  需要增加批量删除功能 和 分页功能  ---- 刘斌  可以找吕建伟和胡亚洲帮忙实现

bug21： 商品列表界面  轮播图字典 有一个图片按钮 和 一个小铅笔按钮  需要将图片按钮改变成 “+” 按钮 ---- 刘斌

bug22： 购物车可以删除一条数据 但有没有批量删除的接口呢  如果没有  需要实现批量删除功能  ---张静

bug23： 订单管理界面 显示的字段为 “序号  订单号  用户id  价格  下单时间  状态 删除” ---- 王泽华

bug24： 广告管理界面 添加广告的时候  不应该让用户输入广告id  广告id是后台根据时间生成的随机字符串  ----王贺

bug25： 广告管理界面  增加一个批量删除的功能   ---王贺


（温馨提示： 自己任务太多的人  可以自行安排其他人来帮助实现）

