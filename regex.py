import re

def swap_circle_coordinates(text):
    pattern = r'circle\{\((\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)\)\}'

    result = re.sub(pattern, r'circle{(\2,\1)}', text)

    return result

text = """
circle{(5,10)}
circle{(3.5, 7.2)}
circle{(0,0)}
circle{(100, 200)}
"""

result = swap_circle_coordinates(text)
print(result)
