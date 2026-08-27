month=6
day = "sun"
match day:
    case "sun" if month==6:
        print("mon")
    case 2:
        print("tue")
    case 3:
        print("wed")
    case 4:
                print("thu")
    case 5:
                print("fri")
    case 6:
            print("sat")
    case 7:
            print("sun")
    case 8 | 9 | 10:
              print("lesthan 8")
    case _:
              print("wrong input")