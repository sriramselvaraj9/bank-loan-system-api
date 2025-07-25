def combine_lists(list1, list2):
    combined = list1 + list2
    combined.sort(key=lambda x: x["positions"][0])

    result = []
    for item in combined:
        if not result:
            result.append(item)
        else:
            last = result[-1]
            l1, r1 = last["positions"]
            l2, r2 = item["positions"]

            len2 = r2 - l2
            overlap = min(r1, r2) - max(l1, l2)

            if overlap > len2 / 2:
                last["values"] += item["values"]
                last["positions"][1] = max(r1, r2)
            else:
                result.append(item)

    return result

list1 = [{"positions": [0, 5], "values": [1, 2]}]
list2 = [{"positions": [3, 6], "values": [3]}]

print(combine_lists(list1, list2))