"""shopServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url , include
from django.contrib import admin
from shopApp.views import *


urlpatterns = [

    url(r'^admin/', admin.site.urls),


    # 用户搜索记录
    url(r'^searchList/$' , searchList),

    url(r'^test/$' , test),
    url(r'^test111/$' , test111),

    # 测试方法
    url(r'^ceshi/$' , ceshi),

    # 获取城市列表数据
    url(r'^get_chinese_address/$' , get_chinese_address),

    url(r'^wxjssdk/$' , wxjssdk),
    url(r'^clearAccess_tokenAndJsapi_ticket/$' , clearAccess_tokenAndJsapi_ticket),
    url(r'^wxService/$' , wxService),
    # url(r'^getOpenidByCode/$' , getOpenidByCode),
    url(r'^getOpenidByCode_new_fn/$' , getOpenidByCode_new_fn),
    url(r'^get_detail_user_info/$' , get_detail_user_info),

    
    

    url(r'^uploadImage/$' , uploadImage), # 上传图片到服务器接口

    url(r'^home/$' , home),
    url(r'^goodsManage/$' , goodsManage),
    url(r'^adPage/$' , adPage),
    url(r'^cartsManage/$' , cartsManage),#购物车界面
    url(r'^jifenGoods/$' , jifenGoods),# 积分商城界面
    url(r'^exportGoods/$' , exportGoods),# 积分商城界面
    
    url(r'^userManage/$' , userManage),
    url(r'^orderManage/$' , orderManage),
    url(r'^adManage/$' , adManage),
    url(r'^changePic/$' , changePic),#改变轮播图界面
    url(r'^changeLunbo/$' , changeLunbo),# 添加轮播图界面
    url(r'^login/$' , login),#登录界面
    url(r'^loginApi/$' , loginApi),  # 登录接口 
    url(r'^register/$' , userManageJsonAdd), # 添加用户接口 
    # url(r'^uploadHeadImg/$' , uploadHeadImg), # 上传头像接口
    url(r'^drawManage/$',drawManage), #抽奖余额界面
    url(r'^recomendGoods/$',recomendGoods), # 推荐商品界面


    url(r'^saveOneImageToServer/$' , saveOneImageToServer),  # 添加一张图片到服务器 不和数据库产生联系

    url(r'^userManageJsonAdd/$' , userManageJsonAdd), # 添加用户接口
    url(r'^addUserAcountMoney/$' , addUserAcountMoney), # 用户充值
    
    url(r'^userManageJsonSelect/$' , userManageJsonSelect), # 查询用户接口
    url(r'^userManageJsonDelete/$' , userManageJsonDelete), #删除用户接口
    url(r'^userManageJsonUpdate/$' , userManageJsonUpdate), #更新用户接口
    url(r'^getUserQrcode/$' , getUserQrcode), # 获取用户的二维码
    url(r'^favoriteAndLookTableManageJsonAdd/$' , favoriteAndLookTableManageJsonAdd),# 搜藏 浏览记录添加接口
    url(r'^favoriteAndLookTableManageJsonSelect/$' , favoriteAndLookTableManageJsonSelect),# 收藏 浏览记录 查询接口
    url(r'^activeManage/$' , activeManage),
    
    url(r'^addGoodsLunbo/$' , addGoodsLunbo),
    url(r'^addLunboImages/$' , addLunboImages), # 多张轮播图添加 新方法
    


    url(r'^fenleiListPage/$' , fenleiListPage), # 分类属性列表界面
    url(r'^editFenleiAttrPage/$' , editFenleiAttrPage), # 编辑分类属性列表界面

    url(r'^appHomePageData/$' , appHomePageData), # app首页数据



    

    url(r'^addUserShangxiaji/$' , addUserShangxiaji), # xxxx
    url(r'^getUserShangxiaji/$' , getUserShangxiaji), # xxxx

    url(r'^addUserShangjiNewFn/$' , addUserShangjiNewFn), # xxxx

    


    # 获取所有商品的小分类
    url(r'^getAllXiaoFenlei/$' , getAllXiaoFenlei), # xxxx
    url(r'^addFenleiAttr/$' , addFenleiAttr), # 给小分类添加属性列表
    url(r'^getFenleiAttr/$' , getFenleiAttr), # 获取小分类属性列表
    url(r'^modifyFenleiAttr/$' , modifyFenleiAttr), # 修改小分类属性
    url(r'^deleteFenleiAttr/$' , deleteFenleiAttr), # 删除小分类的某一个属性列表


    
    
    
    

    url(r'^adManageJsonAdd/$' , adManageJsonAdd), # 广告添加的接口
    url(r'^adManageJsonSelect/$' , adManageJsonSelect), # 广告列表的接口 兼 广告查询接口
    url(r'^adManageJsonDelete/$' , adManageJsonDelete), # 广告删除的接口
    url(r'^adManageJsonUpdate/$' , adManageJsonUpdate), # 修改广告位置的接口


    url(r'^goodsManageJsonAdd/$' , goodsManageJsonAdd),  # 商品添加接口
    url(r'^goodsManageJsonSelect/$' , goodsManageJsonSelect),  # 商品查询接口   
    url(r'^addGoods/$' , addGoods),  # 添加商品接口


    url(r'^rebateTableAdd/$' , rebateTableAdd),  # 返利添加接口
    url(r'^rebateTableQuery/$' , rebateTableQuery),  # 返利查询接口
    


    url(r'^getGoodsListByQueryString/$' , getGoodsListByQueryString),  # 在搜索框列表上选中之后的的查询方法
    url(r'^getGoodsBySomething/$' , getGoodsBySomething),  # 商品模糊查询 供移动端使用
    url(r'^getGoodsByMinfenleiId/$' , getGoodsByMinfenleiId),  # 根据小分类id查询所有的商品
    url(r'^getGoodsByManyGoodsid/$' , getGoodsByManyGoodsid), # 根据多个商品id获取多个商品信息
    
    url(r'^getGoodsByClassify/$' , getGoodsByClassify),  # 根据分类 查询商品 
    url(r'^goodsManageJsonUpdata/$' , goodsManageJsonUpdata), # 商品列表修改接口
    url(r'^goodsManageJsonDelete/$' , goodsManageJsonDelete),  # 商品列表删除接口

    url(r'^goodsSelectByidNew/$' , goodsSelectByidNew), # 根据商品id查找商品
    
    url(r'^commodityQuery/$' , commodityQuery), # 商品模糊查询接口查找商品
    url(r'^goodsNameSelect/$' , goodsNameSelect), # 商品名模糊查询接口
    url(r'^goodsNameOneSelect/$' , goodsNameOneSelect), # 商品名准确查询接口
    
    
    url(r'^activetableManageJsonAdd/$' , activetableManageJsonAdd),  # 活动添加接口
    url(r'^activeManageJsonSelect/$' , activeManageJsonSelect), # 活动列表接口
    
    url(r'^activetableManageJsonDelete/$' , activetableManageJsonDelete), # 活动删除接口接口
    url(r'^activesManageJsonDelete/$', activesManageJsonDelete),# 活动批量删除接口
    url(r'^activetableManageJsonchange/$' , activetableManageJsonchange),  # 活动改变接口
    url(r'^redpack/$',redpack),#红包页面
    url(r'^redpackApi/$',redpackApi),#红包查询
    url(r'^redpackAdd/$',redpackAdd),#红包添加
    url(r'^redpackDelete/$',redpackDelete),#红包删除
    



    url(r'^addTransportId/$' , addTransportId), # 给商品添加运单号接口
    url(r'^ordertableManageJsonAdd/$' , ordertableManageJsonAdd), # 订单添加接口
    url(r'^ordertableListJson/$' , ordertableListJson), # 订单查询接口
    url(r'^ordertableDelete/$' , ordertableDelete), # 订单删除接口
    url(r'^modify_order_status/$' , modify_order_status), # 修改订单状态
    

    url(r'cartstableManageJsonAdd/$' , cartstableManageJsonAdd), #购物车添加接口
    url(r'cartstableManageJsonDelete/$' , cartstableManageJsonDelete), #购物车删除接口
    url(r'cartstableManageJsonUpdate/$' , cartstableManageJsonUpdate), #购物车修改接口
    url(r'cartstableManageJsonSelect/$' , cartstableManageJsonSelect), #购物车查询接口

    
    url(r'^audioToStr/$' , audioToStr), #语音查询页面
    # url(r'^audioToStrApi/$' , audioToStrApi), #语音查询页面


    url(r'^drawJsonAdd/$',drawJsonAdd),   #添加抽奖余额接口
    url(r'^drawJsonDel/$',drawJsonDel),   #删除抽奖余额接口
    url(r'^drawJsonUpdate/$',drawJsonUpdate),   #更新抽奖余额接口
    url(r'^drawJsonQuery/$',drawJsonQuery),   #查找抽奖余额接口



    url(r'luckyManage/$' , luckyManage), #福袋管理界面
    url(r'luckyManageJsonQuery/$' , luckyManageJsonQuery), #福袋模糊查询接口(分页)
    url(r'luckyManageJsonDelete/$' , luckyManageJsonDelete), #福袋删除接口
    url(r'luckyManageJsonAdd/$' , luckyManageJsonAdd), #福袋添加接口
    url(r'luckyManageJsonUpdata/$' , luckyManageJsonUpdata), #福袋修改接口
    url(r'selectLuckyJsonByGoodsId/$' , selectLuckyJsonByGoodsId), #通过商品号查询福袋

           
    url(r'commentJsonQuery/$' , commentJsonQuery), #评论查询接口(分页)    
    url(r'commentJsonDelete/$' , commentJsonDelete), #评论删除接口
    url(r'commentJsonAdd/$' , commentJsonAdd), #评论添加接口


    # 将某一个地址设置为默认地址,其他地址修改为非默认地址
    url(r'^change_one_add_to_moren/$',change_one_add_to_moren), 
    url(r'^addAddress/$',addAddress),   #添加地址接口
    url(r'^delAddress/$',delAddress),   #删除地址接口
    url(r'^updateAddress/$',updateAddress),   #修改地址接口
    url(r'^findAddress/$',findAddress),   #查找地址接口


    url(r'^addShare/$',addShare),   #添加分享记录接口
    url(r'^delShare/$',delShare),   #删除分享记录接口
    url(r'^findShare/$',findShare),   #查找分享记录接口

    url(r'^leaveMessage/$',leaveMessage), #查询用户留言接口
    url(r'^addLeaveMessage/$',addLeaveMessage), ##增加用户留言接口
    url(r'^deleLeaveMessage/$',deleLeaveMessage), ##删除用户留言接口
    url(r'^leavingMessage/$',leavingMessage), #留言查询接口 POST请求
    url(r'^read_all_msg_by_wxid/$',read_all_msg_by_wxid), #根据wxid 标记已读消息
    url(r'^get_message_by_wxid/$',get_message_by_wxid), #根据wxid 获取消息


    url(r'^buyhistoryAdd/$',buyhistoryAdd), #购买历史添加接口
    url(r'^buyhistorySelect/$',buyhistorySelect), #购买历史删除接口 POST请求
    url(r'^buyhistoryDelete/$',buyhistoryDelete), #购买历史查询接口 POST请求

    
    url(r'^secondkillManageJsonAdd/$' , secondkillManageJsonAdd),#秒杀活动添加     
    url(r'^secondkillManageJsonSelect/$' , secondkillManageJsonSelect),#秒杀活动查询
    url(r'^notInMiaoshaGoods/$' , notInMiaoshaGoods),#秒杀活动查询
    
    url(r'^secondkillManageJsonDelete/$' , secondkillManageJsonDelete),#秒杀活动删除
    url(r'^secondkillManageJsonUpdata/$' , secondkillManageJsonUpdata),#秒杀活动更新
    url(r'^addAlreadyMiaoShaNumber/$' , addAlreadyMiaoShaNumber),# 增加商品的已秒杀数量

    url(r'^getdatatime/$' , getdatatime),# 获取服务器时间

    
    url(r'^secondkillManageJsonstock/$' , secondkillManageJsonstock),#查询库存
    url(r'^adsecondkill/$' , adsecondkill), # 秒杀
    url(r'^secondkillManage' , secondkillManage), # 秒杀
    url(r'^secondkillAddgoodsidintogoods/$' , secondkillAddgoodsidintogoods),
    url(r'^liuyan_and_dingdan/$',liuyan_and_dingdan), # base页面 留言列表和订单列表

    url(r'^getDingdanByDingdanid/$' , getDingdanByDingdanid),

    url(r'^express/$',express),#测试用查询快递接口        
    url(r'^shortMsgFromName/$',shortMsgFromName),#测试用发送短信接口
    url(r'^shortMsgFromPhone/$',shortMsgFromPhone),#测试用发送短信接口  
    url(r'^secondkillcommodityQuery/$',secondkillcommodityQuery),

    url(r'^getSession/$',getSession), #请求session数据的接口
    url(r'^setSession/$',setSession), #设置session数据的接口
    
    url(r'cartstableManageJsonOneDelete/$' , cartstableManageJsonOneDelete), #购物车删除接口


    url(r'getBigClassify/$' , getBigClassify), # 商品大分类获取接口
    url(r'addBigClassify/$' , addBigClassify), # 商品大分类添加接口
    url(r'deleteBigClassify/$' , deleteBigClassify), # 商品大分类删除接口

    url(r'getMinClassify/$' , getMinClassify), # 商品小分类获取接口
    url(r'addMinClassify/$' , addMinClassify), # 商品小分类添加接口
    url(r'deleteMinClassify/$' , deleteMinClassify), # 商品小分类删除接口
    url(r'uploadMinCllasifyImg/$' , uploadMinCllasifyImg), # 商品小分类添加图片接口


    url(r'notInRecommendGoods/$' , notInRecommendGoods), # 不在推荐表中的所有商品
    url(r'getRecommendGoods/$' , getRecommendGoods), # 推荐商品获取接口
    url(r'addRecommendGoods/$' , addRecommendGoods), # 推荐商品添加接口
    url(r'delRecommendGoods/$' , delRecommendGoods), # 推荐商品删除接口

    url(r'modifyUserQianDaoTime/$' , modifyUserQianDaoTime), # 修改用户签到时间接口



    
    url(r'getWxPayid/$' , getWxPayid), # 服务器向微信下订单的接口
    url(r'weixinNotify_url/$' , weixinNotify_url), # 微信字符结果的通知地址

    url(r'getAccess_token_api/$' , getAccess_token_api), # 获取token值

    url(r'ceshiTupiandizhi/$' , ceshiTupiandizhi), # 微信字符结果的通知地址



    url(r'MP_verify_OEMcT0UWO4grSYBg.txt$' , getTxt), # 微信网页授权文件获取的接口

    url(r'MP_verify_gxBhgLWOaaVeJ6fr.txt$' , getJSSDKTxt), # 微信JS-SDK文件获取的接口

    url(r'MP_verify_X8Xygw0Hvfgy0UZq.txt$' , rundongWangyeTxt), # 润东网页授权txt

    url(r'MP_verify_XkZ6EA7ucXFAwE0P.txt$' , mingchuanWangyeTxt), # 明川的网页授权txt





   
   url(r'weixinPayFn/$' , weixinPayFn), # 微信支付接口
   url(r'xunichongzhi/$' , xunichongzhi), # 微信虚拟充值接口

   url(r'jifenToAccount/$' , jifenToAccount), # 用户积分兑换余额接口

   url(r'addUserSomeNumber/$' , addUserSomeNumber), # 添加用户的积分 等接口
   url(r'useUserNumber/$' , useUserNumber), # 用户消费 积分 账户余额 返利等字段的 接口

   url(r'getUserInfoByWxid/$' , getUserInfoByWxid), # 根据 微信id 获取用户信息
   url(r'modifyGoodsSomeNumber/$' , modifyGoodsSomeNumber), # 修改商品的一些参数

   url(r'getOneRandomFudai/$' , getOneRandomFudai), # 随机获取一个福袋的接口

   url(r'jifenListJson/$' , jifenListJson), # 积分商城列表接口
   url(r'deleteManyJifenprice/$' , deleteManyJifenprice), # 积分批量删除接口

   url(r'getShangjiaGoodsList/$' , getShangjiaGoodsList), # 查询已上架的商品列表 供移动端使用

   # 商品新的测试接口
   # 添加大分类接口
   url(r'addBigFenlei/$' , addBigFenlei), 
   # 大分类删除接口
   url(r'deleteBigFenlei/$' , deleteBigFenlei), 
   # 大分类接口列表
   url(r'allBigFenlei/$' , allBigFenlei), 

   # 根据大分类获取下面的所有分类数据 供移动端使用
   url(r'getAllFenleiByDafenleiId/$' , getAllFenleiByDafenleiId),

   # 添二级分类的接口
   url(r'addTwoFenlei/$' , addTwoFenlei), 
   # 根据大分类 获取二级分类
   url(r'getMinFenleiByBigFenlei/$' , getMinFenleiByBigFenlei), 
   # 删除二级分类接口
   url(r'deleteErjiFenlei/$' , deleteErjiFenlei),

   # 三级分类数据的接口
   url(r'getSanjifenleiData/$' , getSanjifenleiData), 
   # 三级分类添加接口
   url(r'addSanjiFenlei/$' , addSanjiFenlei), 
   # 三级分类删除接口
   url(r'deleteSanjiFenlie/$' , deleteSanjiFenlie), 

   # 三级分类上传图片接口
   url(r'sanjiFenleiAddImage/$' , sanjiFenleiAddImage), 

   # 上传csv文件接口
   url(r'uploadCSVFile/$' , uploadCSVFile),

   # 根据商品id获取轮播图
   url(r'getLunboList/$' , getLunboList),

   # 轮播图删除接口
   url(r'deleteOneLunboById/$' , deleteOneLunboById),
   # 轮播图删多张除接口
   url(r'deleteManyLunboImage/$' , deleteManyLunboImage),

   # 确认收货某一件商品
   url(r'querenshouhuoApi/$' , querenshouhuoApi),

   

   # 添加商品原始图 图片 缩略图
   url(r'addGoodsSomeImage/$' , addGoodsSomeImage),


   # serversetting 添加接口
   url(r'insertServerSetting/$' , insertServerSetting),
   # 获取设置信息
   url(r'getServerSetting/$' , getServerSetting),


   url(r'lihangjiekou/$' , lihangjiekou),
   url(r'tianxiaopengjiekou/$' , tianxiaopengjiekou),
   url(r'fcyjiekou/$' , fcyjiekou),
   url(r'yanjiushengjiekou/$' , yanjiushengjiekou),
   url(r'xiongdajiekou/$' , xiongdajiekou),
   url(r'lianxiyangjiekou/$' , lianxiyangjiekou),
   url(r'lxyjiekou/$' , lxyjiekou),
   url(r'getcodeDemo/$' , getcodeDemo),
   url(r'wxjsqianmingFn/$' , wxjsqianmingFn),

   url(r'lihanghtml/$' , lihanghtml),
   url(r'chenhaijiaohtml/$' , chenhaijiaohtml),
   url(r'fcyhtml/$' , fcyhtml),
   url(r'tianxiaopenghtml/$' , tianxiaopenghtml),
   url(r'songchenfeihtml/$' , songchenfeihtml),
   url(r'xiongdahtml/$' , xiongdahtml),
   url(r'lianxiyanghtml/$' , lianxiyanghtml),



    # 订单所有者 防止他人恶意修改订单

    # 订单库存数量的问题
    # update product set available_amount = available_amount - #{buyAmount} where product_id = #{id} and available_amount - #{buyAmount} >= 0

    # 不要相信前段 在后台计算业务逻辑 前端值传过来商品id就行

# 商品列表中显示该商品是否有积分

# 添加商品时候 更新按钮
# 修改分类图片的时候 要吧之前的删除掉 

# 看看秒杀界面的商品有没有图片

# 秒杀数量问题

# 添加商品时候  商品的分类问题


# 删除商品的时候 要把轮播图中的图片给删掉

# 商品图片提交的时候 要把之前的图片给清除掉

# 购买记录添加接口

# 返回商品的时候 要返回商品的类别

# 添加商品的时候  可以添加商品图片


# 删除商品 proprice prostart proend 这个字段

# 删除之前的商品分类数据表

# 删除商品的时候  删除推荐表中的信息

# 添加推荐  查询 按钮 绑定回车事件
# 推荐列表界面 增加 商品名字登

# 订单界面

# 根据小分类 查询商品 默认按照 手机端已上架的商品去查询 ， 但是服务器段还没有加上这个参数



# 商城 项目
# 搜索界面 筛选功能

# 搜藏列表 取消搜藏
# cartstableManageJsonDelete 
    # POST
    # 参数：
    # tablename:favorite
    # ids:["搜藏id"]


# 分类属性列表 增加 第 11 条的 时候  自动分页成2页







    

#    url(r'getJSSDKConfigPackage' , getJSSDKConfigPackage), # js-SKD 签名包 的生成
#    url(r'getcode/$' , getcode), # 微信字符结果的通知地址
   url(r'^$' , login),
   url(r'^.' , error),






]
