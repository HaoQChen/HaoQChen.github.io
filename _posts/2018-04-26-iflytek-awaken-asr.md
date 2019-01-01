---
layout:     post
title:      科大讯飞实时语音唤醒+离线命令词识别在Linux及ROS下的应用
subtitle:   技术探索
date:       2018-04-26
author:     白夜行的狼
header-img: img/in_post/iflytek_awaken_asr/black.jpeg
catalog: true
tags:
    - 科大讯飞
    - 语音识别
    - ROS语音识别
    - 语音唤醒
    - 命令词识别
--- 

# 0. 写在最前面
本文持续更新地址：<https://haoqchen.site/2018/04/26/iflytek-awaken-asr/>

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

* github地址：<https://github.com/HaoQChen/iflytek_awaken_asr>（喜欢的话帮忙github点个赞呗～～～包含命令行和ROS两个分支，自行选择）
* 因为科大讯飞给的Demo中只有“录一段时间的音频然后命令词识别”、“对一段录音中是否有唤醒词进行判断”，不能够实现24小时不间断的进行命令词识别或者唤醒的Demo。所以我设计了程序实现24小时不间断录音，实时检测有无唤醒词出现，当有唤醒词出现时，切换到“一段时间的命令词识别”功能。（科大讯飞的文档中说，唤醒功能的QIVWSessionBegin可以修改一个参数实现唤醒+命令词识别，但是我试了很多次，不懂这里的bnf应该是什么格式的）
* **本文假设大家对于科大讯飞的语音识别开发平台有一定的了解，文中将不再介绍下载安装等事项，经常出现的一些不匹配或者构建语法失败也都是没认真申请或者替换相关语法资源造成的。另外经过这么长的时间，科大讯飞官方SDK应该也会有改动，本文仅供提供一个实现建议，请注意**
* 只在Linux平台下进行过试验，系统版本Ubuntu14.04（64bit）、ROS版本indigo，暂时没有发现bug。
* 包括录音、语音识别等代码主要参考科大讯飞的SDK，作者加上了命令解析的代码，并设计整个程序框架，对于作者部分的代码完全开源，不保留权利。至于科大讯飞部分代码，请联系科大讯飞公司。

# 1. 整体框架
```cpp
int main(int argc, char **argv)//这只是主体程序
{
//init iflytek
  int ret = 0 ;
  ret = MSPLogin(NULL, NULL, lgi_param);
  
  memset(&asr_data, 0, sizeof(UserData));
  ret = build_grammar(&asr_data);  //第一次使用某语法进行识别，需要先构建语法网络，获取语法ID，之后使用此语法进行识别，无需再次构建
  
  while (1)
  {
    run_ivw(NULL, ssb_param); 
    
    if(g_is_awaken_succeed){
      run_asr(&asr_data);
      g_is_awaken_succeed = FALSE;
    }
    
    if(g_is_order_publiced == FALSE){
      if(g_order==ORDER_BACK_TO_CHARGE){
        play_wav((char*)concat(PACKAGE_PATH, "audios/back_to_charge.wav"));        
      }
      if(g_order == ORDER_FACE_DETECTION){
        play_wav((char*)concat(PACKAGE_PATH, "audios/operating_face_rec.wav"));
      }
      g_is_order_publiced = TRUE;
   }
    
 }
exit:
  MSPLogout();
}
```
上面是main函数的主体部分

登录->构建语法->进入while(1)循环
# 2. 语音唤醒
在while(1)循环中，运行run_ivw(NULL, ssb_param); 开启录音，创建一个新的线程接收录音并上传至服务器等待唤醒结果。此时run_ivw处于阻塞状态，一直持续到收到唤醒结果，然后停止录音退出唤醒服务。
```cpp

void run_ivw(const char *grammar_list ,  const char* session_begin_params)//这只是主题
{
//start QIVW
    session_id=QIVWSessionBegin(grammar_list, session_begin_params, &err_code);
    err_code = QIVWRegisterNotify(session_id, cb_ivw_msg_proc,NULL);
//start record
    err_code = create_recorder(&recorder, iat_cb, (void*)session_id);
    err_code = open_recorder(recorder, get_default_input_dev(), &wavfmt);
    err_code = start_record(recorder);
    
    record_state = MSP_AUDIO_SAMPLE_FIRST;
 
    while(record_state != MSP_AUDIO_SAMPLE_LAST)
    {
        sleep_ms(200); //阻塞直到唤醒结果出现
        printf("waiting for awaken%d\n", record_state);
    }
    
exit:
    if (recorder) {
        if(!is_record_stopped(recorder))
            stop_record(recorder);
        close_recorder(recorder);
        destroy_recorder(recorder);
        recorder = NULL;
    }
    if (NULL != session_id)
    {
        QIVWSessionEnd(session_id, sse_hints);
    }
}
```
# 3. 离线命令词识别
只有当唤醒结果是成功的才运行run_asr(&asr_data)，该函数构建离线命令词识别参数，调用demo_mic函数。该函数的作用与run_ivw函数基本相似，初始化语音识别、开始识别、等待15秒或者识别完成之后关闭录音
```cpp

static void demo_mic(const char* session_begin_params)//这只是主体程序
{
    struct speech_rec_notifier recnotifier = {
        on_result,
        on_speech_begin,
        on_speech_end
    };
 
    errcode = sr_init(&iat, session_begin_params, SR_MIC, &recnotifier);
    errcode = sr_start_listening(&iat);
    /* demo 15 seconds recording */
    while(i++ < 15 && iat.session_id != NULL)
        sleep(1);
    errcode = sr_stop_listening(&iat);
    sr_uninit(&iat);
}
```
# 4. 识别结果
**语音唤醒的回调函数为：**
```cpp
int cb_ivw_msg_proc( const char *sessionID, int msg, int param1, int param2, const void *info, void *userData )//这只是主体部分程序
{
  if (MSP_IVW_MSG_ERROR == msg) //唤醒出错消息
  {
    g_is_awaken_succeed = FALSE;
    record_state = MSP_AUDIO_SAMPLE_LAST;
  }else if (MSP_IVW_MSG_WAKEUP == msg) //唤醒成功消息
  {
    g_is_awaken_succeed = TRUE;
    record_state = MSP_AUDIO_SAMPLE_LAST;
  }
  int ret = stop_record(recorder);  
  return 0;
}
```
该函数通过服务器返回的消息判断唤醒结果，这里我们通过全局变量向主函数以及录音线程传递结果，以及时做出该有的反应。  
**离线命令词识别的回调函数：**
```cpp
void on_result(const char *result, char is_last)
{
    if (result) {
    size_t left = g_buffersize - 1 - strlen(g_result);
    size_t size = strlen(result);
    if (left < size) {
        g_result = (char*)realloc(g_result, g_buffersize + BUFFER_SIZE);
        if (g_result)
        g_buffersize += BUFFER_SIZE;
        else {
        printf("mem alloc failed\n");
        return;
        }
    }
    strncat(g_result, result, size);
    show_result(g_result, is_last);
        g_order = get_order(g_result);
        if(g_order > ORDER_NONE){
            g_is_order_publiced = FALSE;
        }
    }
}
```
持续获取结果，然后调用get_order函数获取结果并返回到全局变量g_order中。这个get_order函数是我根据自己的语法特性编写的。各位看官可以根据自己的情况做更改。我的语法特性请看下图：
![order](/img/in_post/iflytek_awaken_asr/order.png)  
主要就是todo+order的形式，其中21300-21399是todo的id，21400-21499是order的id。这样就可以在获取结果时很明显地区分开todo和order，进而识别出语义。
# 5. ROS下的应用
这个语音唤醒与命令词识别一开始也主要想用在ROS系统进行机器人语音控制。这里给出了indigo版本的实现。

在这个包中，我定义了一个sr_order的msg，然后定义一个awaken_asr节点，当获取到识别结果时就发布消息。同时给出了一个listener接收消息的例子。熟悉ROS的朋友应该都知道我在说啥，就不细说了，具体看我github中ROS的分支程序。

# 参考
[科大讯飞开放平台](http://www.xfyun.cn/)  
SDK文档

# ∞写在最后
科大讯飞工作人员的态度真的很棒，之前调试发现了一个bug，向他们反馈，虽然还没解决，但是一直在积极跟进。  
![bug](/img/in_post/iflytek_awaken_asr/bug.png)  
另外希望科大讯飞可以降低起购量。学生党真的想用，但是不需要这么多的装机量。最后在他们官方群哭诉了挺久，他们的工作人员建议我实名制学生身份，然后向他们服务申请了几个学术用途的装机量。他们做支持的小姐姐不辞劳苦地忙了很久，最后终于给我申请到了。在此感谢科大讯飞给了我这个机会学习到这些知识。  

本文一开始发布在CSDN博客上，评论区探讨了一些问题，包括一个小bug以及怎么获取到装机量等，详情看[原博客](https://blog.csdn.net/u013834525/article/details/80097253)

<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
