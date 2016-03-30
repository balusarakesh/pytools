def collect_random(num=10):
    for i in range(num):
        yield (i, i+1, i+2)

output = list(collect_random(5))
a, b, c = [i[0] for i in output], [i[0] for i in output], [i[0] for i in output]
print a