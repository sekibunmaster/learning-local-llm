def get_input():
    height = int(input("身長は:"))
    weight = int(input("体重は:"))
    return height, weight

def calc_bmi(height, weight):
    height_m = height / 100
    bmi = weight / height_m**2
    return bmi

def display_result(bmi):
    if bmi < 18.5:
        print("低体重")
    elif 18.5 <= bmi < 25:
        print("普通体重")
    else:
        print("肥満")


height, weight = get_input()
bmi = calc_bmi(height, weight)
result = display_result(bmi)