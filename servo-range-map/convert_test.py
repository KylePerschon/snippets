# %%

min_in = 0
max_in = 255
min_servo = 0
max_servo = 180
stop_servo = max_servo/2

def map_range(x, in_min, in_max, out_min, out_max):
  return int((x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min)


def get_speed(val: int):
    set_speed = None
    print(f"Setting speed to {val}.")
    if val == 0:
        set_speed = stop_servo
    if dir == "back":
        set_speed = map_range(val, min_in, max_in, stop_servo, min_servo)
    if dir == "forward":
        set_speed = map_range(val, min_in, max_in, stop_servo, max_servo)
    print(f"Out speed: {set_speed}")
    print('\n')

dirs = [
    'back',
    'forward'
]

for dir in dirs:
    print(f'Setting direction to: {dir}')
    for i in range(min_in, max_in+1):
        get_speed(i)
# %%
