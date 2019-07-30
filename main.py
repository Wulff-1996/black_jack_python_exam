from random import shuffle

# set up the cards
RANKS = [x for x in range(2, 11)] + ['JACK', 'QUEEN', 'KING', 'ACE']
COLORS = ['HEARTS', 'SPADES', 'DIAMONDS', 'CLUBS']

def create_deck():
    return [(rank, color) for rank in RANKS for color in COLORS]

def shuffle_deck(deck):
    shuffle(deck)

def get_user_type(is_player):
    try:
        user_input = int(input("Do you want to be the player or the dealer? \n1: player \n2: dealer "))
        if user_input == 1:
            is_player = True
        elif user_input == 2:
            is_player = False
        else:
            raise ValueError
    except ValueError:
        print('---INVALID INPUT---')
        get_user_type(is_player)

def calculate_hand(hand):
    amount_of_aces = 0
    sum = 0
    for card in hand:
        if card[0] in RANKS[0:-4]:
            sum += card[0]
        elif card[0] == 'ACE':
            sum += 11
            amount_of_aces += 1
        else:
            sum += 10
    if amount_of_aces > 0 and sum > 21:
        for _ in range(amount_of_aces):
            if sum > 21:
                sum -= 10
    return sum

def print_frame(player_role, player_sum, player_money, bet, player_hand, computer_role, computer_sum, computer_hand):
    print('---------------------------------------------------')
    print(f'|YOU: {player_role}')
    print(f'|cards total value: {player_sum}')
    print(f'|money: {player_money}')
    print(f'|bet: {bet}')
    print(f'|', [f'{x} of {y}' for (x, y) in player_hand])
    print('|                                                 |')
    print('|                                                 |')
    print('|                                                 |')
    print(f'|COMPUTER: {computer_role}')
    print(f'|cards total value: {computer_sum}')
    print(f'|', [f'{x} of {y}' for (x, y) in computer_hand])
    print('|                                                 |')
    print('|                                                 |')
    print('---------------------------------------------------')

def get_bet(player_mon):
    try:
        bet = int(input(f'Place bet, you have {player_mon}.'))
        if bet > 0:
            return bet
        else:
            print('bet must be over 0')
            get_bet(player_mon)
    except ValueError:
        print('---INVALID INPUT---')
        get_bet(player_mon)

def print_draw_exstra_card():
    print('------------------------------------------')
    print('|    do you want to draw exstra card?    |')
    print('|    1: YES                              |')
    print('|    2: NO                               |')
    print('------------------------------------------')

def get_input(print_func):
    print_func()
    try:
        data = int(input())
        if data == 1:
            return True
        elif data == 2:
            return False
        else:
            get_input(print_func)
    except ValueError:
        print('INVALID INPUT')
        get_input(print_func)



        
def game():
    player_money = 100
    bet = 0
    is_player = True
    player_role = 'PLAYER'
    computer_role = 'DEALER'
    player_hand = []
    computer_hand = []
    player_sum = 0
    computer_sum = 0

    deck = create_deck()
    shuffle_deck(deck)

    get_user_type(is_player)

    if is_player == False:
        player_role = 'DEALER'
        computer_role = 'PLAYER'

    bet = get_bet(player_money)
    player_money -= bet

    while player_money > 0:
        player_hand = [deck.pop(), deck.pop()]
        computer_hand = [deck.pop(), deck.pop()]
        
        player_sum = calculate_hand(player_hand)
        computer_sum = calculate_hand(computer_hand)

        print_frame(player_role, player_sum, player_money, bet, player_hand, computer_role, computer_sum, computer_hand)
        
        if player_role == 'PLAYER':
            while get_input(print_draw_exstra_card) == True:
                player_hand.append(deck.pop())
                player_sum = calculate_hand(player_hand)
                print_frame(player_role, player_sum, player_money, bet, player_hand, computer_role, computer_sum, computer_hand)
        break
        


game()