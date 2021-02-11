def add_to_csv(name, score,pre_path=""):
    folder = open(pre_path+"/high_scores.csv", "a+")
    folder.write(name + "," + str(score) + "\n")
    folder.close()


def read_csv(pre_path=""):
    folder = open(f"{pre_path}/high_scores.csv", "r")


    information = folder.read()

    folder.close()
    # print('I',information)
    return information


def parse_csv(pre_path=""):
    # Parsing the csv file that was saved:
    info = read_csv(pre_path=pre_path).split("\n")
    updated = []
    if len(info)<=1:
        return []
    for i in range(len(info) - 1):
        try:
            a = info[i].split(",")
            updated.append([a[0], int(a[1])])   
        except:
            pass
    return updated


def insert_person(csv_array, person):
    index = len(csv_array) - 1
    for i in range(len(csv_array)):
        if csv_array[i][1] < person[1]:
            # The person is greater than the array at this index, we do not need to look at anything else
            index = i
            break

    inserted = []
    for i in range(len(csv_array)):
        if i == index:
            inserted.append(person)
        inserted.append(csv_array[i])

    return inserted


def automate_insertion(person,pre_path=""):
    info = parse_csv(pre_path=pre_path)
    inserted_array = insert_person(info, person)
    if inserted_array == []:
        inserted_array = [person]

    folder = open(f"{pre_path}/high_scores.csv", "w")
    for name in inserted_array:
        folder.write(name[0] + "," + str(name[1]) + "\n")
    folder.close()

if __name__ == "main":
    print(parse_csv())
