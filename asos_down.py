from ASOS_DAY import ASOS

std = [90, 93, 95, 98, 99, 100, 101, 102, 104, 105, 106, 108, 112, 114, 115, 119, 121, 127, 129, 130, 131, 133, 135, 136, 137, 138, 140, 143, 146, 152, 155, 156, 159, 162, 165, 168, 169, 170, 172, 174, 177, 184, 185, 188, 189, 192, 201, 202, 203, 211, 212, 216, 217, 221, 226, 232, 235, 236, 238, 239, 243, 244, 245, 247, 248, 251, 252, 253, 254, 255, 257, 258, 259, 260, 261, 262, 263, 264, 266, 268, 271, 272, 273, 276, 277, 278, 279, 281, 283, 284, 285, 288, 289, 294, 295]

# encoding key
with open('./Keys/key.txt', 'r') as f:
    keys = f.read().rstrip().split('/n')

asos = ASOS(std,'1990','2020')
for key in keys:
    asos.add_keys(key) # 키 추가하고싶은 만큼 반복
asos.Crwal()
