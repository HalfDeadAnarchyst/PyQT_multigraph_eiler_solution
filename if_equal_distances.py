city_1 = 'city_1'
city_2 = 'city_2'
city_3 = 'city_3'
city_4 = 'city_4'
city_5 = 'city_5'

megalist = [[city_1, city_1, 0], [city_1, city_2, 220.31550517225926], [city_1, city_3, 74.52745173871898],
            [city_1, city_4, 116.69460729477476], [city_1, city_5, 96.68867724148338],
            [city_2, city_1, 220.31550517225926], [city_2, city_2, 0], [city_2, city_3, 151.70594836306765],
            [city_2, city_4, 199.23856161514527], [city_2, city_5, 132.17079948901957],
            [city_3, city_1, 74.52745173871898], [city_3, city_2, 151.70594836306765], [city_3, city_3, 0],
            [city_3, city_4, 83.23264810803704], [city_3, city_5, 22.16972047708083],
            [city_4, city_1, 116.69460729477476], [city_4, city_2, 199.23856161514527],
            [city_4, city_3, 83.23264810803704], [city_4, city_4, 0], [city_4, city_5, 84.83672671534902],
            [city_5, city_1, 96.68867724148338], [city_5, city_2, 132.17079948901957],
            [city_5, city_3, 22.16972047708083], [city_5, city_4, 84.83672671534902], [city_5, city_5, 0]]


def calc_route(route):
    distance = 0
    for n in range(len(route) - 1):
        for elem in megalist:
            if route[n] == elem[0] and route[n+1] == elem[1]:
                distance += elem[2]
    return distance


var1 = [9, [city_2, city_1, city_2, city_1, city_4, city_2, city_5, city_4, city_5]]
var2 = [9, [city_2, city_1, city_2, city_1, city_4, city_5, city_4, city_2, city_3]]
var3 = [9, [city_2, city_1, city_2, city_1, city_4, city_5, city_4, city_2, city_5]]
var4 = [9, [city_2, city_1, city_4, city_2, city_1, city_2, city_5, city_4, city_5]]
var5 = [9, [city_2, city_1, city_4, city_5, city_4, city_2, city_1, city_2, city_5]]
var6 = [9, [city_2, city_1, city_2, city_1, city_4, city_2, city_5, city_4, city_5]]
var7 = [9, [city_2, city_1, city_2, city_1, city_4, city_5, city_4, city_2, city_5]]
var8 = [9, [city_2, city_1, city_2, city_1, city_4, city_5, city_4, city_2, city_5]]
var9 = [9, [city_2, city_1, city_4, city_2, city_1, city_2, city_5, city_4, city_5]]
var10 = [9, [city_2, city_1, city_4, city_5, city_4, city_2, city_1, city_2, city_3]]
var11 = [9, [city_2, city_1, city_4, city_5, city_4, city_2, city_1, city_2, city_5]]
var12 = [9, [city_2, city_5, city_4, city_2, city_1, city_2, city_1, city_4, city_5]]
var13 = [9, [city_2, city_5, city_4, city_2, city_1, city_2, city_1, city_4, city_5]]

print(calc_route(var1[1]))
print(calc_route(var2[1]))
print(calc_route(var3[1]))
print(calc_route(var4[1]))
print(calc_route(var5[1]))
print(calc_route(var6[1]))
print(calc_route(var7[1]))
print(calc_route(var8[1]))
print(calc_route(var9[1]))
print(calc_route(var10[1]))
print(calc_route(var11[1]))
print(calc_route(var12[1]))
print(calc_route(var13[1]))
