expenses = []

def add_expense():
    item = input("請輸入支出項目：")
    amount = input("請輸入金額：")
    if amount.isdigit():
        expenses.append((item, int(amount)))
        print("✅ 已新增支出！")
    else:
        print("⚠️ 金額輸入錯誤，請輸入數字")

def show_total():
    total = sum([amount for _, amount in expenses])
    print(f"💰 總支出為：{total} 元")

def list_expenses():
    if not expenses:
        print("目前沒有任何支出紀錄。")
    else:
        print("📋 支出清單：")
        for item, amount in expenses:
            print(f"- {item}: {amount} 元")

while True:
    print("\n======= 記帳小程式 =======")
    print("1. 新增支出")
    print("2. 顯示總支出")
    print("3. 查看所有支出")
    print("4. 離開")
    choice = input("請選擇操作（1-4）：")

    if choice == '1':
        add_expense()
    elif choice == '2':
        show_total()
    elif choice == '3':
        list_expenses()
    elif choice == '4':
        print("👋 再見囉！")
        break
    else:
        print("⚠️ 無效的選擇，請重新輸入")


       

