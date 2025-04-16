import datetime
"""数据层"""

# 钢材原始数据
Original_database = {
    # 结构钢 (键: 钢材牌号，值: (抗拉强度, 屈服强度, 伸长率, 密度, 价格))
    "Q235B": (410, 235, 26, 7.85, 3850),
    "Q345D": (530, 345, 22, 7.86, 4200),
    "HRB400E": (570, 400, 16, 7.85, 4350),
    # 美标钢材（含进口关税溢价）
    "ASTM A36": (550, 250, 23, 7.87, 5800),
    "ASTM A572-50": (690, 345, 18, 7.88, 6500),
    # 特殊材料
    "S30408": (590, 245, 40, 8.03, 15500),  # 不锈钢
    "6061-T6": (310, 275, 12, 2.70, 28500),  # 铝合金
    # 特殊规格（含加工溢价）
    "Q235B-XL": (435, 255, 24, 7.84, 4100),  # 加长型+5%
    "HRB400E-FG": (585, 420, 15, 7.83, 4600),  # 细晶粒+8%
    # 异常数据
    "TEST-ERROR": (0, 999, "N/A", 0.0, -1),  # 非法价格测试
}
# 钢材库存数据
inventory_data = {
    # 普通结构钢（多仓库分布）
    "Q235B": {
        "总库存(吨)": 685.3,
        "仓库分布": {
            "上海中心仓": {
                "数量(吨)": 420.5,
                "规格(mm)": ["Φ12", "Φ16", "板20×2000"],
                "入库批次": [
                    {
                        "批次号": "SH202406001",
                        "数量(吨)": 200.0,
                        "入库时间": "2024-06-05",
                    },
                    {
                        "批次号": "SH202406015",
                        "数量(吨)": 220.5,
                        "入库时间": "2024-06-18",
                    },
                ],
            },
            "武汉二仓": {
                "数量(吨)": 264.8,
                "规格(mm)": ["Φ20", "板25×1500"],
                "入库批次": [
                    {
                        "批次号": "WH202405123",
                        "数量(吨)": 264.8,
                        "入库时间": "2024-05-28",
                    }
                ],
            },
        },
        "安全库存": 300.0,
        "最近盘点时间": "2024-06-20",
    },
    # 高强度抗震钢筋（单仓存储）
    "HRB400E": {
        "总库存(吨)": 158.2,
        "仓库分布": {
            "成都抗震仓": {
                "数量(吨)": 158.2,
                "规格(mm)": ["Φ28", "Φ32"],
                "入库批次": [
                    {
                        "批次号": "CD202406045",
                        "数量(吨)": 80.0,
                        "入库时间": "2024-06-10",
                    },
                    {
                        "批次号": "CD202406097",
                        "数量(吨)": 78.2,
                        "入库时间": "2024-06-22",
                    },
                ],
            }
        },
        "安全库存": 100.0,
        "最近盘点时间": "2024-06-25",
    },
    # 美标钢材（保税仓存储）
    "ASTM A572-50": {
        "总库存(吨)": 82.6,
        "仓库分布": {
            "洋山保税仓": {
                "数量(吨)": 82.6,
                "规格(mm)": ["W21×50", "PL25×3000"],
                "入库批次": [
                    {
                        "批次号": "YS202406-US1",
                        "数量(吨)": 82.6,
                        "入库时间": "2024-06-15",
                    }
                ],
            }
        },
        "安全库存": 50.0,
        "最近盘点时间": "2024-06-18",
    },
    # 不锈钢（特种材料仓）
    "S30408": {
        "总库存(吨)": 35.8,
        "仓库分布": {
            "太钢特种仓": {
                "数量(吨)": 35.8,
                "规格(mm)": ["2B板0.5mm", "NO.1板6mm"],
                "入库批次": [
                    {
                        "批次号": "TG202406-SS1",
                        "数量(吨)": 35.8,
                        "入库时间": "2024-06-12",
                    }
                ],
            }
        },
        "安全库存": 20.0,
        "最近盘点时间": "2024-06-19",
    },
    # 铝合金（航空航天专用仓）
    "6061-T6": {
        "总库存(吨)": 12.5,
        "仓库分布": {
            "西飞特供仓": {
                "数量(吨)": 12.5,
                "规格(mm)": ["板2.0×1220×2440", "棒材Φ150"],
                "入库批次": [
                    {
                        "批次号": "XF202406-AL1",
                        "数量(吨)": 12.5,
                        "入库时间": "2024-06-05",
                    }
                ],
            }
        },
        "安全库存": 5.0,
        "最近盘点时间": "2024-06-08",
    },
    # 加长型钢材（项目专用库存）
    "Q235B-XL": {
        "总库存(吨)": 45.0,
        "仓库分布": {
            "港珠澳项目仓": {
                "数量(吨)": 45.0,
                "规格(mm)": ["Φ36×12m", "Φ40×12m"],
                "入库批次": [
                    {
                        "批次号": "GZA202406-XL1",
                        "数量(吨)": 45.0,
                        "入库时间": "2024-06-01",
                    }
                ],
            }
        },
        "安全库存": 10.0,
        "最近盘点时间": "2024-06-02",
    },
    # 细晶粒钢筋（高铁项目库存）
    "HRB400E-FG": {
        "总库存(吨)": 220.0,
        "仓库分布": {
            "京沪高铁材料仓": {
                "数量(吨)": 220.0,
                "规格(mm)": ["Φ12", "Φ16", "Φ20"],
                "入库批次": [
                    {
                        "批次号": "JHGT202406-01",
                        "数量(吨)": 120.0,
                        "入库时间": "2024-06-10",
                    },
                    {
                        "批次号": "JHGT202406-02",
                        "数量(吨)": 100.0,
                        "入库时间": "2024-06-25",
                    },
                ],
            }
        },
        "安全库存": 150.0,
        "最近盘点时间": "2024-06-26",
    },
    # 美标普通钢材（跨境电商仓）
    "ASTM A36": {
        "总库存(吨)": 150.0,
        "仓库分布": {
            "深圳跨境仓": {
                "数量(吨)": 150.0,
                "规格(mm)": ["W10×12", "C10×20"],
                "入库批次": [
                    {
                        "批次号": "SZ202406-US2",
                        "数量(吨)": 150.0,
                        "入库时间": "2024-06-20",
                    }
                ],
            }
        },
        "安全库存": 80.0,
        "最近盘点时间": "2024-06-21",
    },
    # 边界测试用例（异常库存）
    #    "TEST-ERROR": {
    #        "总库存(吨)": -100.0,
    #        "仓库分布": {
    #            "虚拟测试仓": {
    #                "数量(吨)": "invalid",
    #                "规格(mm)": [],
    #                "入库批次": [
    #                   {"批次号": "TEST0001", "数量(吨)": "abc", "入库时间": "9999-99-99"}
    #                ]
    #            }
    #       },
    #       "安全库存": "N/A",
    #       "最近盘点时间": "无效日期"
    #   }
}

# 钢材模型数据Original_database导入钢材数据库steel_database
steel_database = {
    trademark: {
        "抗拉强度(MPa)": value[0],
        "屈服强度(MPa)": value[1],
        "伸长率(%)": value[2],
        "密度(g/cm³)": value[3],
        "价格(元/吨)": value[4],
    }
    for trademark, value in Original_database.items()
}
# 导入库存数据inventory_data到钢材数据库steel_database
steel_database = {
    k: {**v, **{"库存数据": inventory_data.get(k, {})}}
    for k, v in steel_database.items()
}

"""核心功能模块层"""


# 钢材牌号智能检索
def steel_screen(lower_tensile_limit, higher_expense_limit):
    return [
        f"{k} ¥{v['价格(元/吨)']}"
        for k, v in steel_database.items()
        if v["抗拉强度(MPa)"] >= lower_tensile_limit
           and 0 < v["价格(元/吨)"] <= higher_expense_limit # 排除测试数据
    ]


# 库存管理器
class inventory_manager:

    # 库存查询
    def inventory_check(trademark, stash=None):
        inventory = steel_database.get(trademark, {}).get("库存数据", {})
        if not stash:
            return inventory.get("总库存(吨)", 0)
        return inventory["仓库分布"].get(stash, {})

    # 库存更新
    def inventory_update(trademark, stash, operation, quantity, type):
        current_time = datetime.date.today()
        number = {"上海中心仓":'SH',"武汉二仓":'WH',"成都抗震仓":'CD',"洋山保税仓":'YS',"太钢特种仓":'TG',"西飞特供仓":'XF', "港珠澳项目仓":'GZA' ,"京沪高铁材料仓":'JH',"深圳跨境仓":'SZ'}
        if operation == 'IN':
            steel_database[trademark]['库存数据']["总库存(吨)"] += quantity
            steel_database[trademark]['库存数据']['仓库分布'][stash]["入库批次"].add({
                        "批次号": f"{number[stash]}{current_time}{type}",
                        "数量(吨)": {quantity},
                        "入库时间": f"{current_time}",
                    })
            steel_database[trademark]['库存数据']["最近盘点时间"] = str(current_time)
            print("更新成功")
        elif operation == 'OUT':
            steel_database[trademark]['库存数据']["总库存(吨)"] -= quantity
            steel_database[trademark]['库存数据']["最近盘点时间"] = str(current_time)
        else:
            print('ERROR INPUT')
# 安全库存警告
    def inventory_warning(self):
        return [
            k
            for k, v in steel_database.items()
            if v.get("库存数据", {}).get("总库存(吨)", 0)
            < v.get("库存数据", {}).get("安全库存", 0)
        ]


"""操作系统层"""

# 模式选择
identify = input("请选择身份：【A】工程师 【B】工人 【Ｃ】设计院")
# 身份：工程师
if identify == "A":
    # 原始数据获取
    original_data = input("请输入筛选条件：{强度下限} {价格上限}，用空格分割数据")
    tensile_limit, expense_limit = original_data.split()
    tensile_limit = float(tensile_limit)
    expense_limit = float(expense_limit)
    # 筛选材料并打印
    print(steel_screen(tensile_limit, expense_limit))
# 身份：工人
elif identify == "B":
    # 多功能获取
    function = input(
        "请输入功能【Ａ】库存查询【B】库存更新 【C】库存检查 【D】物料调度"
    )
    # 功能：库存查询
    if function == "A":
        original_data = input("请输入查询信息：{钢材牌号}{查询仓库}")
        mark_input, stash_input = original_data.split()
        # 查询库存并打印
        print(inventory_manager.inventory_check(mark_input, stash_input))
    # 功能：库存更新
    elif function == "B":
        original_data = input('''请输入更新信息：{牌号}{仓库}{操作}{数量}{规格}
            操作：IN or OUT''')
        trademark_input,stash_input , operation_input,quantity_input,type_input = original_data.split()
        quantity_input = float(quantity_input)
        inventory_manager.inventory_update(trademark_input,stash_input,operation_input,quantity_input,type_input)
    # 功能：库存检查
    elif function == "C":
        # 拷贝列表
        i = inventory_manager.inventory_warning()
        if i:  # 存在
            print(i)
        else:  # 不存在
            print("NO WARNING")
    # 功能：物料调度
    elif function == "D":
        # 获取原始数据
        original_data = input('请输入需求{"牌号","规格", "需求数量"')
        mark_input, type_input, quantity_input = original_data.split()
        quantity_input = int(quantity_input)
        # 生成库存分布列表
        inventory_recommence = [
            stash_name
            for stash_name, stash_value in steel_database[mark_input]["库存数据"][
                "仓库分布"
            ].items()
            if type_input in stash_value["规格(mm)"]
            and stash_value["数量(吨)"] >= quantity_input
        ]
        if inventory_recommence:
            print(f"建议从{inventory_recommence[0]}调拨")
        else:
            print("库存空，推荐供应商：宝武集团")
    else:
        print("ERROR INPUT")
# 身份：设计院
elif identify == "C":
    pass
else:
    print("ERROR INPUT")
