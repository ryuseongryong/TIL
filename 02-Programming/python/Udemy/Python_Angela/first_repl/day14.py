from lib.higher_lower_art import logo, vs
from lib.higher_lower_data import data
import random

def select_A():
    selected = data.pop(random.randint(0, len(data) - 1))
    return selected

def select_B():
    selected = data.pop(random.randint(0, len(data) - 1))
    return selected

def invoke_data(selected_data):
    name = selected_data["name"]
    description = selected_data["description"]
    country = selected_data["country"]
    def check_a_or_an(t):
        first_l = t[0].lower
        if first_l == 'a' or first_l == 'e' or first_l == 'i' or first_l == 'o' or first_l == 'u':
            return 'an'
        else:
            return 'a'
    a_or_an = check_a_or_an(description)
    
    return f"{name}, {a_or_an} {description}, from {country}."
  
def invoke_follower(selected_data):
    follower = selected_data["follower_count"]
    return follower

def compare(A, B):
    if invoke_follower(A) > invoke_follower(B):
        return "A"
    elif  invoke_follower(A) < invoke_follower(B):
        return "B"
    else: 
        return "Draw"
      
def check_score(A, B, answer, score):
    
    return score
    
      
print(logo)

data = data
end_game = False
score = 0
while not end_game:
    A = select_A()
    B = select_B()

    print("Compare A:", invoke_data(A))
    print(vs)
    print("Against B:", invoke_data(B))
    answer = input("Who has more followers? Type 'A' or 'B': ").upper()
    if compare(A, B) == answer:
        score += 1
        print(f"You're right! Current score: {score}.")
    elif compare(A, B) == "Draw":
        print(f"Sorry, It's Draw. Please next version.")
        end_game = True
    else:
        print(f"Sorry, that's wrong. Final score: {score}")
        end_game = True
