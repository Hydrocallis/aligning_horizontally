import random

def generate_values(selected_value, choice_list:list, num_values:int, random_frequency:float):
    values = [selected_value]

    for _ in range(1, num_values):
        if random.random() < random_frequency:
            values.append(random.choice(choice_list))
        else:
            values.append(selected_value)
            
    return values

# 使用例
# choice_list = ["apple", "pineapple", "banana", "orange", "grape", "kiwi", "mango", "pear", "peach", "plum", "watermelon", "cherry", "strawberry", "blueberry", "raspberry", "lemon", "lime", "coconut", "pomegranate", "fig"]
# selected_value = random.choice(choice_list)

# generated_values = generate_values(selected_value, choice_list,100, 0.2)
# print(generated_values)