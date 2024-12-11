import random
import matplotlib.pyplot as plt
from collections import Counter

def display_slots(slots):
    print("Current Slots:")
    print(" | ".join(str(slot) if slot is not None else "_" for slot in slots))

def is_valid_placement(slots, position, number):
    
    if slots[position] is not None:
        return False
    
    for i in range(position):
        if slots[i] is not None and number <= slots[i]:
            return False
 
    for i in range(position + 1, len(slots)):
        if slots[i] is not None and number > slots[i]:
            return False
    return True

def can_place_number(slots, number):
    
    for i in range(len(slots)):
        if is_valid_placement(slots, i, number):
            return True
    return False

def play_game(range_num=100, slots_num = 20):
    slots = [None] * slots_num  
    print("Welcome to the Ascending Order Game!")
    print("Your goal is to place numbers in the slots such that they remain in ascending order.")
    print("If you can't place a number, you lose. Good luck!\n")
    unique_numbers = random.sample(range(1, range_num + 1), range_num)
    print(unique_numbers)
    while None in slots:
        
        random_number = unique_numbers.pop()
        #random_number = random.randint(1, range)
        print(f"New number generated: {random_number}")
        display_slots(slots)
        # Check if the number can be placed
        if not can_place_number(slots, random_number):
            print(f"No valid positions for {random_number}. You lose!")
            break
        while True:  
            try:
                position = int(input(f"Enter the position (1-20) to place {random_number}: ")) - 1
                if position < 0 or position >= 20:
                    print("Invalid position. Please enter a number between 1 and 20.")
                    continue
                
                if not is_valid_placement(slots, position, random_number):
                    print("Invalid placement. The number must be greater than all previous slots and smaller than or equal to all following slots.")
                    continue
                
                slots[position] = random_number
                print(f"Placed {random_number} in position {position + 1}.\n")
                break 
            except ValueError:
                print("Please enter a valid number between 1 and 20.")
    
    #print("Congratulations! You successfully filled all slots in ascending order!")

def find_nearest_valid_slot(slots, start_position, number):
   
    for offset in range(len(slots)):
        for direction in [-1, 1]:  # Try both directions
            pos = start_position + offset * direction
            if 0 <= pos < len(slots) and is_valid_placement(slots, pos, number):
                return pos
    return None

def strategy(slots, random_number, number_range):
   
    num_slots = len(slots)
    calculated_slot = round((random_number / number_range) * num_slots) - 1  # -1 for 0-based index
    calculated_slot = max(0, min(calculated_slot, num_slots - 1))  # Ensure the index is within bounds

    if is_valid_placement(slots, calculated_slot, random_number):
        return calculated_slot

    # Find the nearest valid slot if the calculated one is occupied
    return find_nearest_valid_slot(slots, calculated_slot, random_number)
def maximize_gaps_strategy(slots, number, number_range):
    
    best_position = None
    largest_gap = -1
    last_filled_index = -1

    for i in range(len(slots) + 1): 
        
        prev = slots[last_filled_index] if last_filled_index >= 0 else float('-inf')
        next_ = slots[i] if i < len(slots) and slots[i] is not None else float('inf')

        if prev < number <= next_:
            gap = next_ - prev 
            if gap > largest_gap:
                largest_gap = gap
                best_position = i

   
        if i < len(slots) and slots[i] is not None:
            last_filled_index = i

    return best_position



def play_game_with_strategy(range_num = 100, strategy = strategy, slots_num = 20):
    slots = [None] * slots_num  
    
    #print("Automated Strategy: Playing the Ascending Order Game!")
    unique_numbers = random.sample(range(1, range_num + 1), 20)

    while None in slots:
        #random_number = random.randint(1, range_num)
        random_number = unique_numbers.pop()

        #print(f"New number generated: {random_number}")
        #display_slots(slots)

        
        position = strategy(slots, random_number, range_num)
        if position is None:
            #print(f"No valid positions for {random_number}. Strategy failed. You lose!")
            filled_slots = sum(1 for slot in slots if slot is not None)
            #print(f"Number of slots filled: {filled_slots}")
            return filled_slots

        
        slots[position] = random_number
        #print(f"Placed {random_number} in position {position + 1}.\n")

    #print("Strategy succeeded! All slots are filled in ascending order.")
    #display_slots(slots)
    filled_slots = sum(1 for slot in slots if slot is not None)
    #display_slots(slots)
    return filled_slots

if __name__ == "__main__":
    #play_game_with_strategy(range_num=200)
   
 

   
   results = [play_game_with_strategy(range_num=21) for _ in range(100000)]
   print(results.count(20))
   results_other = [play_game_with_strategy(range_num=22) for _ in range(100000)]
   print(results_other.count(20))
   results_also = [play_game_with_strategy(range_num=1000000) for _ in range(100000)]

fig, axes = plt.subplots(1, 3, figsize=(12, 5), sharey=True)


axes[0].hist(results, bins=range(0, 22), align='left', edgecolor='black')
axes[0].set_title('Number Range: 1-21')
axes[0].set_xlabel('Number of Slots Filled')
axes[0].set_ylabel('Frequency')
axes[0].set_xticks(range(0, 21))


axes[1].hist(results_other, bins=range(0, 22), align='left', edgecolor='black')
axes[1].set_title('Number Range: 1-22')
axes[1].set_xlabel('Number of Slots Filled')
axes[1].set_xticks(range(0, 21))

axes[2].hist(results_also, bins=range(0, 22), align='left', edgecolor='black')
axes[2].set_title('Number Range: 1-1000000')
axes[2].set_xlabel('Number of Slots Filled')
axes[2].set_xticks(range(0, 21))

plt.tight_layout()
plt.show()
    
 