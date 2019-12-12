# 师门挂机脚本
# 师门任务要点：
# 1. 右侧任务栏中向上滑动查找师门任务是否存在 不存在直接退出
# 2. 找到师门任务栏并点击
# 3. 如果弹出新窗口，则前往领取 否则 直接开始任务
# 4. （1）对话框选择 —— 选择最上面对话框
#    （2）物品购买 —— 找到并点击购买
#    （3）物品上交 —— 上到并点击上交
#    （4）物品使用 —— 在屏幕右下方可能出现物品的使用
#    （5）商会购买 —— 若干条件判断 并点击
# 5. 中途可能有弹窗弹出 暂时先不考虑弹窗问题
# 6. 不要随便到处乱点 如果发现有问题，宁可退出，也不要乱点

# 注意中间可能抛出异常的部分
# 截图使用完毕后记得删除图片文件

# 依赖引用
from appium import webdriver as app_web
from PIL import Image
from io import StringIO,BytesIO
import os
import time
import aircv as ac
from Utils import Utils
from Constants import Constants

# 全局变量定义
# desired_caps = {
#     'platformName': 'Android',
#     'udid':'127.0.0.1:62001',
#     'deviceName': 'deviceName',
#     'platformVersion':'5.1.1',
#     'unicodekeyboard':True
# }
taskPosition = tuple()
# 构建对象变量
util = Utils()

# 基本函数 启动session
# def startDriver():
#     driver = app_web.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
#     return driver

# 截屏获取图片 返回图片名称
def screenShot():
    scannTimsTamp = int(round(time.time() * 1000))
    path = "./shimen_image/" + str(scannTimsTamp)[6:] + "_shimen.png"
    util.get_screen_shot(path)
    time.sleep(3)
    return path

# 删除截图
def removeShot(fileName):
    os.remove(fileName)

# 对比图片返回相似度最高的位置坐标
def compareTwoImg(srcImg, objImg):
    imgSrc = ac.imread(srcImg)
    imgObj = ac.imread(objImg)
    return ac.find_template(imgSrc, imgObj)

# 对比图片返回所有匹配坐标
def compareTwoImgAll(srcImg,objImg):
    imgSrc = ac.imread(srcImg)
    imgObj = ac.imread(objImg)
    return ac.find_all_template(imgSrc, imgObj)

# 查找任务坐标
def swipeTaskBar():
    # 任务栏向上滑动
    util.swipe((1130, 220), (1130, 560), 200)



# 不能用比对的方式， 相似度太低了 还是要用像素颜色的方式
def findTask(image):
    pos_1 = util.comparePixelColor(image, Constants.shimen_task_color_1, Constants.shimen_task_position_1, 0.95)
    pos_2 = util.comparePixelColor(image, Constants.shimen_task_color_2, Constants.shimen_task_position_2, 0.95)
    pos_3 = util.comparePixelColor(image, Constants.shimen_task_color_3, Constants.shimen_task_position_3, 0.95)
    if pos_1 and pos_2 and pos_3:
        # 发现师门任务在第一栏
        # todo 师门任务可能在第二栏
        return (1113, 194)
    else:
        return -1


# 任务重新开始有弹窗 检查弹窗并点击
def checkTaskStart():
    fileName = screenShot()
    matchResult = compareTwoImg(fileName, "image/quwancheng.png")
    if matchResult is not None:
        util.tap(matchResult.get("result"))
        # 为了避免重复点击 任务造成弹窗反复弹出 延迟1s 再回到主流程
        removeShot(fileName)
        time.sleep(1)
        return 0
    else:
        removeShot(fileName)
        return -1

# 多对话框过滤函数，选择最上层的对话框坐标返回
def haveTaskFrame(image):
    if util.comparePixelColor(image, Constants.talk_color_person, Constants.talk_position_persion, 0.95) == False:
        return -1
    if util.comparePixelColor(image, Constants.talk_color_person_left, Constants.talk_position_persion_left, 0.95) == False:
        return -1
    if util.comparePixelColor(image, Constants.talk_color_00, Constants.talk_position_00, 0.95) == True:
        util.tap(Constants.talk_position_00)
        return 0
    if util.comparePixelColor(image, Constants.talk_color_0, Constants.talk_position_0, 0.95) == True:
        util.tap(Constants.talk_position_0)
        return 1
    if util.comparePixelColor(image, Constants.talk_color_1, Constants.talk_position_1, 0.95) == True:
        util.tap(Constants.talk_position_1)
        return 2
    if util.comparePixelColor(image, Constants.talk_color_2, Constants.talk_position_2, 0.95) == True:
        util.tap(Constants.talk_position_2)
        return 3
    if util.comparePixelColor(image, Constants.talk_color_3, Constants.talk_position_3, 0.95) == True:
        util.tap(Constants.talk_position_3)
        return 4
    if util.comparePixelColor(image, Constants.talk_color_4, Constants.talk_position_4, 0.95) == True:
        util.tap(Constants.talk_position_4)
        return 5
    # 有人物 无对话框 随便点击一个位置
    print("有人物 无对话框 点击任务位置 结束对话")
    util.tap(taskPosition)
    return -1

# 判断是否有对话框出现
# 对话框最后判断，因为对话框中需要反复截图
def checkTalkFrame(image, fileName):
    tag = -1
    startTime = time.time()
    while True:
        endTime = time.time()
        # 总共对话时间超过10s 强制退出
        # if endTime - startTime > 30:
        #     print("30秒时间到 强制结束对话!")
        #     return -1
        if tag == 0:
            # 对话已经推进 需要重新截屏
            fileName = screenShot()
            image = Image.open(fileName)
        # 匹配对话框 并点击
        result = haveTaskFrame(image)
        if result >= 0:
            print("发现对话 点击对话 " + str(result))
            tag = 0
            image.close()
            removeShot(fileName)
            # 不要马上截屏 画面更新可能有延迟
            time.sleep(2)
        elif tag == 0:
            # 把最新的截图返回 原本的已经被删了
            return (image, fileName)
        else:
            # 没对话框 直接返回 -1
            return -1

# 购买药品判断 有"+"按钮 并且有红叉
def checkBuyThing(image):
    cancel = util.comparePixelColor(image, Constants.drug_cancel_color, Constants.drug_cancel_positon, 0.9)
    add = util.comparePixelColor(image, Constants.drug_add_color, Constants.drug_add_position, 0.9)
    buy = util.comparePixelColor(image, Constants.drug_buy_color, Constants.drug_buy_position, 0.9)
    if cancel and add and buy:
        # 确认是药店购买
        util.tap(Constants.drug_buy_position)
        print("购买物品成功")
        time.sleep(1)
        return 0
    else:
        return -1

# 商会购买判断
def checkBussThing(image):
    cancel = util.comparePixelColor(image, Constants.buss_cancel_color, Constants.buss_cancel_position, 0.9)
    title = util.comparePixelColor(image, Constants.buss_title_color, Constants.buss_title_position, 0.9)
    buy = util.comparePixelColor(image, Constants.buss_buy_color, Constants.buss_buy_position, 0.9)
    if cancel and title and buy:
        # 确认是商会购买
        util.tap(Constants.buss_first_thing_position)
        time.sleep(0.3)
        util.tap(Constants.buss_buy_position)
        print("商会购买成功")
        time.sleep(1)
        return 0
    else:
        return -1

#使用物品判断
def checkUseThing(image):
    cancel = util.comparePixelColor(image, Constants.thing_cancel_color, Constants.thing_cancel_position, 0.9)
    frame = util.comparePixelColor(image, Constants.thing_frame_color, Constants.thing_frame_position, 0.9)
    use = util.comparePixelColor(image, Constants.thing_use_color, Constants.thing_use_position, 0.9)
    if cancel and frame and use:
        util.tap(Constants.thing_use_position)
        print("使用物品成功")
        time.sleep(1)
        return 0
    else:
        return -1

# 宠物购买判断
def checkPetBuy(image):
    cancel = util.comparePixelColor(image, Constants.pet_cancel_color, Constants.pet_cancel_positon, 0.9)
    frame = util.comparePixelColor(image, Constants.pet_title_color, Constants.pet_title_position, 0.9)
    use = util.comparePixelColor(image, Constants.pet_buy_color, Constants.pet_buy_position, 0.9)
    if cancel and frame and use:
        util.tap(Constants.pet_buy_position)
        print("宠物购买成功")
        time.sleep(1)
        return 0
    else:
        return -1

# 宠物上交判断 宠物上交界面在中间 不在右侧
def checkPetGive(image):
    cancel = util.comparePixelColor(image, Constants.pet_give_cancel_color, Constants.pet_give_cancel_position, 0.9)
    frame = util.comparePixelColor(image, Constants.pet_give_frame_color, Constants.pet_give_frame_position, 0.9)
    use = util.comparePixelColor(image, Constants.pet_give_give_color, Constants.pet_give_give_position, 0.9)
    if cancel and frame and use:
        print("上交宠物成功")
        util.tap(Constants.pet_give_give_position)
        time.sleep(1)
        return 0
    else:
        return -1

# 物品上交在右侧 不在中间
def checkThingGive(image):
    cancel = util.comparePixelColor(image, Constants.thing_give_cancel_color, Constants.thing_give_cancel_position, 0.9)
    frame = util.comparePixelColor(image, Constants.thing_give_frame_color, Constants.thing_give_frame_position, 0.9)
    use = util.comparePixelColor(image, Constants.thing_give_give_color, Constants.thing_give_give_position, 0.9)
    if cancel and frame and use:
        print("上交物品成功")
        util.tap(Constants.thing_give_give_position)
        time.sleep(1)
        return 0
    else:
        return -1

# 干脆这个函数就不用了 没必要这个函数
def checkTaskScene(image, fileName):
    state = util.comparePixelColor(image, Constants.task_tag_color, Constants.task_tag_position, 0.95)
    if state == False:
        # 剧情中 或者 战斗中 循环截取图片判断是否结束
        return 0
    else:
        return -1   # -1 表示任务标签存在 属于正常状态 没有做任何操作

def checkTaskStatus(image, fileName):
    # 有绿色小标签 并且找不到师门了 认为已经结束了
    # 先判断是否有对话框出现 老天鹅哟
    result = checkTalkFrame(image, fileName)
    if result != -1:
        image = result[0]
        fileName = result[1]
    tag = util.comparePixelColor(image, Constants.task_tag_color, Constants.task_tag_position, 0.95)
    if tag == True:
        if findTask(image) != -1:
            # 找到师门了
            return (image, fileName)
        else:
            clearImage(image, fileName)
            return -1
    else:
        return (image, fileName)

# 判断并关闭师门任务结束后弹出的界面框
def checkTaskFinishFrame(image):
    pos_1 = util.comparePixelColor(image, Constants.task_finish_color_0, Constants.task_finish_position_0, 0.95)
    pos_2 = util.comparePixelColor(image, Constants.task_finish_color_1, Constants.task_finish_position_1, 0.95)
    pos_3 = util.comparePixelColor(image, Constants.task_finish_color_2, Constants.task_finish_position_2, 0.95)
    if pos_1 and pos_2 and pos_3:
        # 界面弹出了
        util.tap((1156, 172))
        print("关闭任务结束弹窗")
        time.sleep(1)
        return 0
    else:
        return -1

def clearImage(image, fileName):
    image.close()
    removeShot(fileName)

# 任务结束判断 有任务标签存在 并且没有师门
# 任务是否结束判断 可能会因为对话框的出现遮挡文字颜色判断， 所以需要在判断条件中加入对话框的判断

# todo 商会购买时有可能已经被买走了，这时候每次判断前记得先点击“那个位置” 需要循环判断
if __name__ == "__main__":
    # fileName = screenShot()
    # image = Image.open(fileName)
    # print(util.getPixelColor(image, Constants.task_finish_position_0))
    # print(util.getPixelColor(image, Constants.task_finish_position_1))
    # print(util.getPixelColor(image, Constants.task_finish_position_2))
    # checkTaskFinishFrame(image)
    # image.close()
    # removeShot(fileName)


    # 判断对话框和 判断是否结束 一定要在判断结束后重新截屏
    print("启动脚本")
    # 滑动任务栏
    swipeTaskBar()
    print("开始预处理...")
    # 延迟3s
    time.sleep(3)
    # 查找师门任务
    fileName = screenShot()
    image = Image.open(fileName)
    tmp = findTask(image)
    image.close()
    removeShot(fileName)
    print("预处理结束")
    if tmp == -1:
        # 没找到师门任务 退出脚本
        print("未发现师门任务 脚本退出")
        exit(0)
    taskPosition = (tmp[0] + 100, tmp[1])
    util.tap(taskPosition)
    time.sleep(1)
    # 点击师门任务 任务开始
    print("发现师门任务 任务启动！")
    # 判断是否已经领取师门任务
    print("检查是否已经领取师门任务")
    time.sleep(3) # 给足够的时间弹出选择弹窗
    receive = checkTaskStart()
    if receive == 0:
        print("尚未领取师门任务 领取师门任务成功")
    else:
        print("已经领取师门任务 继续推动任务")
    runTime = 0
    while True:
        if runTime != 0:
            print("一轮判断运行时间为: " + str(time.time() - runTime))
        runTime = time.time()
        fileName = screenShot()
        image = Image.open(fileName)
        # 判断是否任务已经结束
        statusResult = checkTaskStatus(image, fileName)
        if statusResult == -1:
            break
        else:
            image = statusResult[0]
            fileName = statusResult[1]
        util.tap(taskPosition)
        # ---------------------------------------
        talk = checkTalkFrame(image, fileName)
        if talk != -1:
            # 有对话操作
            image = talk[0]
            fileName = talk[1]
        # task = checkTaskScene(image, fileName)
        # if task != -1:
        #     image = task[0]
        #     fileName = task[1]
        # ---------------------------------------
        if checkBuyThing(image) == 0:
            clearImage(image, fileName)
            continue
        if checkThingGive(image) == 0:
            clearImage(image, fileName)
            continue
        if checkBussThing(image) == 0:
            clearImage(image, fileName)
            continue
        if checkUseThing(image) == 0:
            clearImage(image, fileName)
            continue
        if checkPetBuy(image) == 0:
            clearImage(image, fileName)
            continue
        if checkPetGive(image) == 0:
            clearImage(image, fileName)
            continue
        checkTaskFinishFrame(image)
        clearImage(image, fileName)
        util.tap(taskPosition)
    print("脚本结束 感谢使用~")