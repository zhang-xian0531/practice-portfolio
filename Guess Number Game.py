import random  # 引入亂數模組

player_record = []  # 用來儲存玩家的紀錄
def add_player_record(name, count):
    """將玩家的紀錄加入到 player_record 列表中"""
    player_record.append({"name": name, "count": count})
    print(f"\U0001F4D6 {name} 的紀錄已儲存！")
    
def guess_number_game():
    secret = random.randint(1, 100)  # 產生 1~100 的神秘數字
    count = 0

    print("\U0001F3AF 歡迎來到猜數字遊戲！（1～100）")
    name = input("請輸入玩家姓名：")
    round = 1
    while round <= 7:  # 最多猜 7 次
        print(f"\n第 {round} 輪，請猜一個數字：")
        round += 1
        guess = input("請輸入你的猜測：")

        if not guess.isdigit():
            print("\u26A0\uFE0F 請輸入有效的數字！")
            continue

        guess = int(guess)
        count += 1

        if guess > secret:
            print("太大囉～再小一點試試！")
        elif guess < secret:
            print("太小了～再大一點看看！")
        else:
            print(f"\U0001F389 恭喜你猜對了！答案是 {secret}")
            print(f"你總共猜了 {count} 次！")
            add_player_record(name, count)
            break

# 呼叫函式開始遊戲
while True:
    print("1. 開始遊戲")
    print("2. 查看玩家紀錄")
    print("3. 離開遊戲")
    choice = input("請選擇操作：")
    if choice == '1':
        guess_number_game()
    elif choice == '2':
        if player_record:
            print("\U0001F4C8 玩家紀錄：")
            for record in player_record:
                print(f"{record['name']} - {record['count']} 次")
        else:
            print("\U0001F4D6 暫無玩家紀錄！")
    elif choice == '3':
        print("\U0001F44B 感謝遊玩，再見！")
        break
    else:
        print("\u26A0\uFE0F 無效的選擇，請重新輸入！")
