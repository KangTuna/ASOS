from ASOS_DAY import ASOS

# std = [90, 93, 95, 98, 99, 100, 101, 102, 104, 105, 106, 108, 112, 114, 115, 119, 121, 127, 129, 130, 131, 133, 135, 136, 137, 138, 140, 143, 146, 152, 155, 156, 159, 162, 165, 168, 169, 170, 172, 174, 177, 184, 185, 188, 
# std = [189, 192, 201, 202, 203, 211, 212, 216, 217, 221, 226, 232, 235, 236, 238, 239, 243, 244, 245, 247, 248, 251, 252, 253, 254, 255, 257, 258, 259, 260, 261, 262, 263, 264, 266, 268, 271, 272, 273, 276, 277, 278, 279, 281, 283, 284, 285, 288, 
std = [289, 294, 295]

# encoding key
keys = ['a2LwYITn8j9Paj1xLhYjdAmMbRK1PDptEBapPLJ16aVLi1tt3d0sVhXTQSDJ3WOwuG75gEKytgSxJnnCiAZueA%3D%3D', # 김민서
       'XXnOF0E0naCqpp8xhgqEOnW%2Bwh5HIojQfhLeWOXy%2BzSOFCsJkX5rwxfKj8YNuwpX4xcqjS0bezInXwTnPmQB4g%3D%3D', # 유현수
       '0sZqTNtvkH3IKaiOWZVQnaAPbVzwwdjBmQpsFFByyGzhxYvMTHQTfHengAnJNjN9dJ3xSZBv%2BZG%2B%2BYmlUdM6nA%3D%3D', # 강우협
       'FEB%2F%2BBuoI%2FJayMJ2EN8v3fJ8GYWQACYzRBa82K8V2bu5Uqm9aOLR8BLCqDmKpIEMPtu8eFawvDTWi0P97DuuEw%3D%3D' # 김표승
       ]

asos = ASOS(std,'1990','2020')
for key in keys:
    asos.add_keys(key) # 키 추가하고싶은 만큼 반복
asos.Crwal()
