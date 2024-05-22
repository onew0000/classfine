import json
import os

DATA_FILE = "fines_data.json"

fines_data = {}

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as file:
        fines_data = json.load(file)

def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(fines_data, file, indent=4)

def add_fine():
    name = input("이름을 입력하세요: ")
    amount = float(input("벌금 금액을 입력하세요: "))
    reason = input("벌금 사유를 입력하세요: ")
    if name in fines_data:
        fines_data[name].append({"amount": amount, "reason": reason})
    else:
        fines_data[name] = [{"amount": amount, "reason": reason}]
    print(f"{name}님의 벌금이 추가되었습니다.")
    save_data()

def remove_fine():
    name = input("이름을 입력하세요: ")
    if name in fines_data:
        print(f"{name}님의 벌금 목록:")
        for idx, fine in enumerate(fines_data[name], start=1):
            print(f"{idx}. {fine['amount']}원 - {fine['reason']}")
        idx_to_remove = int(input("제거할 벌금 번호를 입력하세요: ")) - 1
        if 0 <= idx_to_remove < len(fines_data[name]):
            removed_fine = fines_data[name].pop(idx_to_remove)
            if not fines_data[name]:
                del fines_data[name]
            print(f"{name}님의 {removed_fine['amount']}원 벌금이 제거되었습니다.")
            save_data()
        else:
            print("잘못된 번호입니다.")
    else:
        print("해당 이름이 존재하지 않습니다.")

def view_fines():
    if not fines_data:
        print("등록된 벌금이 없습니다.")
    else:
        for name, fines in fines_data.items():
            print(f"{name}님의 벌금 목록:")
            for fine in fines:
                print(f"  - {fine['amount']}원: {fine['reason']}")

def main():
    while True:
        print("\n벌금 관리 프로그램")
        print("1. 벌금 추가")
        print("2. 벌금 제거")
        print("3. 벌금 조회")
        print("4. 종료")
        choice = input("선택하세요: ")

        if choice == "1":
            add_fine()
        elif choice == "2":
            remove_fine()
        elif choice == "3":
            view_fines()
        elif choice == "4":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")

if __name__ == "__main__":
    main()
