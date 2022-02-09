# Split range r(x,y) by a threshold t
def split_range(r, t):
    x, y = r
    if t <= x:
        return (None, r)
    elif t > y:
        return (r, None)
    else:
        return ((x, t-1), (t,y))

a = split_range((11,23), 5)
b = split_range((11,23), 11)
c = split_range((11,23), 15)
d = split_range((11,23), 23)
e = split_range((11,23), 27)
print(a,b,c,d,e)