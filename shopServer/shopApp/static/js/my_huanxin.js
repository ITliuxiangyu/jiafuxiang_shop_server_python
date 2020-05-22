if (conn) {
    conn.close()
}

var conn = new WebIM.connection({
    isMultiLoginSessions: WebIM.config.isMultiLoginSessions,
    https: typeof WebIM.config.https === 'boolean' ? WebIM.config.https : location.protocol === 'https:',
    url: WebIM.config.xmppURL,
    heartBeatWait: WebIM.config.heartBeatWait,
    autoReconnectNumMax: WebIM.config.autoReconnectNumMax,
    autoReconnectInterval: WebIM.config.autoReconnectInterval,
    apiUrl: WebIM.config.apiURL,
    isAutoLogin: true
});

conn.listen({
    onOpened: function(message) { //连接成功回调
        // 如果isAutoLogin设置为false，那么必须手动设置上线，否则无法收消息
        // 手动上线指的是调用conn.setPresence(); 如果conn初始化时已将isAutoLogin设置为true
        // 则无需调用conn.setPresence();     
        console.log('连接成功回调')
        console.log(message)
    },
    onClosed: function(message) {
        console.log('连接关闭回调')
        console.log(message)
    },
    onTextMessage: function(message) {
        var cur_time = getServerDate()
        for (var i = 0; i < base_liuyan_list.length; i++) {
            if (base_liuyan_list[i].user_info.wxid.toLowerCase() == message.from) {
                var temp_dic = {
                    content: message.data,
                    receiveId: message.to,
                    senderId: message.from,
                    status: 1,
                    time: cur_time
                }
                base_liuyan_list[i].msg_list.push(temp_dic)
                break
            }
        }
        
        if (window.location.href.indexOf(HomeUrl + "leavingMessage/") != -1) {
            if ($('.chart_modal').css('display') == 'block' && $('.chart_modal').attr('chat_id').toLowerCase() == message.from) {
                var temp_chart_ele = '<div class="direct-chat-msg"><div class="direct-chat-info clearfix"><span class="direct-chat-name pull-left">' + curr_chat_user.nickName + '</span><span class="direct-chat-timestamp pull-right">' + cur_time + '</span></div><img class="direct-chat-img" src="' + curr_chat_user.headimg + '" alt="用户头像"><div class="direct-chat-text">' + message.data + '</div></div>'
                $(".direct-chat-messages").append($(temp_chart_ele))
                var scrollHeight = $('.direct-chat-messages').prop("scrollHeight");      
                $('.direct-chat-messages').scrollTop(scrollHeight, 1000);
            } else {
                $(".msg_number").text(($(".msg_number").text()) - 0 + 1)
                $('.user_chart_table tr').each(function (index , ele) {
                    if ($(ele).attr('wxid').toLowerCase() == message.from) {
                        var cur_num = $(ele).find('.badge-danger').text() - 0 + 1
                        $(ele).find('.badge-danger').text(cur_num)
                    }
                })
            }
        } else {
            $(".msg_number").text(($(".msg_number").text()) - 0 + 1)
        }
        
    },
    onCmdMessage: function(message) {
        console.log('//收到命令消息')
        console.log(message)
    },
    onFileMessage: function(message) {
        console.log('//收到文件消息')
        console.log(message)
    },
    onRoster: function(message) {
        console.log('//处理好友申请')
        console.log(message)
    },
    onOnline: function(message) {
        console.log('//本机网络连接成功')
        console.log(message)
    },
    onOffline: function(message) {
        console.log('//本机网络掉线')
        console.log(message)
    },
    onError: function(message) {
        console.log('//失败回调')
        console.log(message)
    },
    onReceivedMessage: function(message) {
        console.log('收到消息送达服务器回执')
        console.log(message)
    },
    onDeliveredMessage: function(message) {
        console.log('收到消息送达客户端回执')
        console.log(message)
    },
});

var options = {
    apiUrl: WebIM.config.apiURL,
    user: my_IM_server,
    accessToken: "YWMtqT6_JDhIEemQgqEk_0wV-fXpHvAjEhHphGAxZIrOEKTJf2jgOEUR6YOjJaD2WtJ-AwMAAAFpIB4MOQBPGgB-8y6_EzgxuGtgLGLZoPGGXFF2x8lKWCC9-e8bifigrg",
    appKey: WebIM.config.appkey,
    success: function(message) {
        console.log('登录成功')
        console.log(message)
    },
    error: function(message) {
        console.log('登录失败')
        console.log(message)
    }
};
conn.open(options);


// var options = {
//     username: my_IM + my_IM_server,
//     password: '123456',
//     nickname: my_IM + my_IM_nick + my_IM_server,
//     appKey: WebIM.config.appkey,
//     success: function(message) {
//         console.log('注册成功')
//         console.log(message)
//     },
//     error: function(message) {
//         console.log('注册失败')
//         console.log(message)
//     },
//     apiUrl: WebIM.config.apiURL
// };
// conn.registerUser(options);