class Constants:
    SCREENSHOT = "adb exec-out screencap -p > " # 末尾需加上截屏地址
    TAP = "adb shell input tap " # 点击屏幕 x y
    SWIPE = "adb shell input swipe " # 滑动屏幕

    # -------------  采样坐标点 -------------#

    #other_position = (1143, 33)  # 为了推动剧情 需要在某个无害之地点击
    task_tag_position = (1050, 131)  # 任务小标签坐标 判断是否在剧情中
    task_tag_color = (222, 237, 183) # 任务标签颜色

    # "师门"文字坐标采点
    shimen_task_position_1 = (1045, 196)
    shimen_task_color_1 = (248, 239, 28)
    shimen_task_position_2 = (1053, 193)
    shimen_task_color_2 = (229, 220, 28)
    shimen_task_position_3 = (1074, 189)
    shimen_task_color_3 = (198, 192, 28)

    # 师门任务结束后弹窗坐标

    task_finish_position_0 = (1170, 170)
    task_finish_color_0 = (183, 41, 25)
    task_finish_position_1 = (1100, 557)
    task_finish_color_1 = (255, 103, 112)
    task_finish_position_2 = (275, 173)
    task_finish_color_2 = (236, 167, 115)

    talk_position_00 = (1080, 114)
    talk_color_00 = (244, 219, 190)
    talk_color_0 = (244, 221, 192)
    talk_position_0 = (1077, 180)
    talk_color_1 = (244, 219, 190)
    talk_position_1 = (1083, 250)   #第一个对话框坐标
    talk_color_2 = (244, 221, 192)
    talk_position_2 = (1083, 315)
    talk_color_3 = (244, 222, 192)
    talk_position_3 = (1083, 381)
    talk_color_4 = (244, 221, 192)
    talk_position_4 = (1083, 450)
    talk_color_person = (246, 210, 167)  # 对话框弹出时 用于判断是否存在人物，即是否在对话
    talk_position_persion = (290, 676) # 人物框坐标
    talk_color_person_left = (247, 211, 169)
    talk_position_persion_left = (95, 675)

    # 药店红叉
    drug_cancel_positon = (1143, 50)
    drug_cancel_color = (207, 0, 0)
    # 药店加号
    drug_add_position = (1103, 390)
    drug_add_color = (135, 88, 50)
    # 药店购买
    drug_buy_position = (969, 585)
    drug_buy_color = (239, 144, 67)

    # 商会红叉
    buss_cancel_position = (1103, 45)
    buss_cancel_color = (207, 0, 0)
    # 商会标题
    buss_title_position = (556, 40)
    buss_title_color = (199, 142, 62)
    # 商会购买
    buss_buy_position = (1005, 653)
    buss_buy_color = (236, 181, 85)
    buss_first_thing_position = (590, 200)

    # 物品使用
    thing_cancel_position = (1159, 395)
    thing_cancel_color = (192, 20, 0)
    thing_use_position = (1092, 573)
    thing_use_color = (238, 193, 98)
    thing_frame_position = (1090, 400)
    thing_frame_color = (233, 211, 183)

    # 宠物购买
    pet_cancel_positon = (1143, 50)
    pet_cancel_color = (207, 0, 0)
    pet_title_position = (573, 30)
    pet_title_color = (255, 255, 255)
    pet_buy_position = (1033, 645)
    pet_buy_color = (236, 180, 84)

    #宠物上交框
    pet_give_cancel_position = (934, 112)
    pet_give_cancel_color = (192, 21, 0)
    pet_give_frame_position = (880, 260)
    pet_give_frame_color = (223, 194, 160)
    pet_give_give_position = (848, 568)
    pet_give_give_color = (242, 202, 105)

    # 物品上交框
    thing_give_cancel_position = (1247, 115)
    thing_give_cancel_color = (192, 21, 0)
    thing_give_frame_position = (1220, 490)
    thing_give_frame_color = (223, 194, 159)
    thing_give_give_position = (1100, 580)
    thing_give_give_color = (238, 193, 98)