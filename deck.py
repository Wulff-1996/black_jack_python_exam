import random
import os
import sys

ranks = [x for x in range(2, 11)] + ['JACK', 'QUEEN', 'KING', 'ACE']
suits = ['DIAMONDS', 'SPADES', 'HEARTS', 'CLUBS']

class Card():
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f'{self.rank} 0f {self.suit}'

class Deck():

    def __init__(self):
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal_hand(self):
        return [self.cards.pop(), self.cards.pop()]

    def deal(self):
        return self.cards.pop()

    def clear(self):
        self.cards.clear()

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        deck_string = ''
        for card in self.cards:
            deck_string += f'\n{str(card)}'
        return deck_string

class Hand():

    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def clear(self):
        self.cards.clear()

    def __str__(self):
        hand_string = 'hand: '
        for card in self.cards:
            hand_string += f'{card}, '
        return hand_string
    
class Chips():

    def __init__(self, money):
        self.money = money
        self.bet = 0

    def win_bet(self):
        self.money += 2*self.bet

    def win_tie(self):
        self.money += self.bet

    def __str__(self):
        return f'money: {self.money}, bet: {self.bet}'


def take_bet(chips):
    try:
        chips.bet = int(input(f'place bet, you have {chips.money} avaliable.'))
    except ValueError:
        print('INVALID INPUT, must be an integer')
        take_bet(chips)
    else:
        if chips.bet > chips.money:
            print(f'You cannot bet {chips.bet}, when you only have {chips.money} money avaliable.')
            take_bet(chips)
        else:
            chips.money -= chips.bet

def hit(hand: Hand, deck: Deck):
    hand.add_card(deck.deal())
    calculate_hand(hand.cards)

def prompt_hit_stand(hand, deck):
    global is_playing
    try:
        user_inputa = int(input('Do you want to take another card? \n1: Hit \n2:Stand'))
    except ValueError:
        print('INVALID INPUT, must be a number')
        prompt_hit_stand(hand, deck)
    else:
        if user_inputa == 1:
            hit(hand, deck)
        elif user_inputa == 2:
            print('You stay, dealer is now playing')
            is_playing = False
        else:
            print('invalid number')
            prompt_hit_stand(hand, deck)


def calculate_hand(cards):
        total = 0
        aces = 0
        for card in cards:
            if card.rank in range(2, 11):
                total += card.rank
            elif card.rank == 'ACE':
                total += 11
                aces += 1
            else:
                total += 10
        if total > 21 and aces > 0:
            for ace in range(aces):
                if total > 21:
                    total -= 10
        return total

def calcultate_one_card(card):
    if card.rank in range(2, 11):
        return card.rank
    elif card.rank == 'ACE':
        return 11
    else:
        return 10


class Player():
    PLAYER = 'PLAYER'
    DEALER = 'DEALER'

    def __init__(self, role, hand, chips):
        self.chips = chips
        self.hand = hand
        self._role = role

    @property
    def role(self):
        if self._role == None:
            return 'undefined'
        else:
            return self._role
    
    @role.setter
    def role(self, role):
        if role != 'PLAYER' and role != 'DEALER':
            raise ValueError('role must be PLAYER or DEALER')
        else:
            self._role = role


def promt_player_dealer():
    try:
        user_inputq = int(input('Do you want to be the player or the dealer? \n1:player \n2:dealer'))
    except ValueError:
        print('input must be an integer')
        promt_player_dealer()
    else:
        if user_inputq == 1:
            return Player.PLAYER
        elif user_inputq == 2:
            return Player.DEALER
        else:
            print('INVALID INPUT, enter a valid input')
            promt_player_dealer()

def promt_money_amount():
    try:
        user_inputd = int(input('Enter players money'))
    except ValueError:
        print('input must be an integer')
        promt_money_amount()
    else:
        return user_inputd

def computer_take_bet(chips: Chips):
    if chips.money >= 100:
        chips.bet = 50
        chips.money -= 50
    elif chips.money >= 50 < 100:
        chips.bet = 25
        chips.money -= 25
    elif chips.money > 10 < 50:
        chips.bet = 5
        chips.money -= 5
    else:
        chips.bet = 1
        chips.money -= 1

def show_cards(player_hand: Hand, dealer_hand: Hand, is_dealer_hidden):
    print('player:')
    print('total: ' + str(calculate_hand(player_hand.cards)))
    print('players hand: ' + str([str(card) for card in player_hand.cards]))
    print()
    print()
    print('dealer:')
    if is_dealer_hidden:
        print('total: ' + str(calcultate_one_card(dealer_hand.cards[1])))
        print('dealer hand: <HIDDEN CARD>, ' + str(dealer_hand.cards[1]))
    else:
        print('total: ' + str(calculate_hand(dealer_hand.cards)))
        print('dealers hand: ' + str([str(card) for card in dealer_hand.cards]))

def you_lost(role, player):
    print('you lost')

    if role == Player.DEALER:
        player.chips.win_bet()

def you_won(role, player):
    print('you won')

    if role == Player.PLAYER:
        player.chips.win_bet()

def tie(player):
    print('tie')
    player.chips.win_tie()

def clear_terminal():
    os.system('cls')

def promt_to_contionue():
    global is_playing
    global is_continue
    if is_continue:
        try:
            user_input3 = int(input('Round over. \n1:continue \n2:new game \n9:quit'))
        except ValueError:
            print('input must be an integer')
            promt_to_contionue()
        else:
            if user_input3 == 1:
                print('user input 1 for continue')
                pass 
            elif user_input3 == 2:
                is_continue = False
            elif user_input3 == 9:
                print('good bye')
                sys.exit('Player exited the game')
            else:
                print('INVALID INPUT, enter a valid input')
                promt_to_contionue()
    else:
        try:
            user_input1 = int(input('Round over. \n2:new game \n9:quit'))
        except ValueError:
            print('input must be an integer')
            promt_to_contionue()
        else:
            if user_input1 == 2:
                is_continue = False
            elif user_input1 == 9:
                sys.exit('Player exited the game')
            else:
                print('INVALID INPUT, enter a valid input')
                promt_to_contionue()
        


# point for new game
is_playing = True
is_continue = True
while is_playing:
    is_continue = True
    print('new game started')
    role = promt_player_dealer()
    money = promt_money_amount()

    deck = Deck()
    deck.shuffle()

    player = Player(Player.PLAYER, Hand(), Chips(money))
    dealer = Player(Player.DEALER, Hand(), Chips(0))

    # point new round
    while is_continue:
        if role == Player.PLAYER:
            take_bet(player.chips)
        else:
            computer_take_bet(player.chips)

        player.hand.clear()
        dealer.hand.clear()

        player.hand.add_card(deck.deal())
        player.hand.add_card(deck.deal())
        dealer.hand.add_card(deck.deal())
        dealer.hand.add_card(deck.deal())

        show_cards(player.hand, dealer.hand, True)

        if role == Player.PLAYER:
            while is_playing == True and calculate_hand(player.hand.cards) < 21:
                prompt_hit_stand(player.hand, deck)
                clear_terminal()
                show_cards(player.hand, dealer.hand, True)
            
            player_total = calculate_hand(player.hand.cards)

            if player_total > 21:
                you_lost(role, player)
            else:
                # dealers turn
                while calculate_hand(dealer.hand.cards) < 17:
                    hit(dealer.hand, deck)
                
                show_cards(player.hand, dealer.hand, False)
                
                dealer_total = calculate_hand(dealer.hand.cards)

                if dealer_total > 21:
                    you_won(role, player)
                elif dealer_total < player_total:
                    you_won(role, player)
                elif dealer_total == player_total:
                    tie(player)
                else:
                    you_lost(role, player)
        else:
            dealer_total = calcultate_one_card(dealer.hand.cards[1])
            
            # logic for computer to hit
            computer_is_playing = True
            while computer_is_playing:
                player_total = calculate_hand(player.hand.cards)
                if player_total <= 11:
                    hit(player.hand, deck)
                elif dealer_total >= 10 and player_total <= 17:
                    hit(player.hand, deck)
                elif dealer_total < 10 and player_total <= 15:
                    hit(player.hand, deck)
                else:
                    break
            
            player_total = calculate_hand(player.hand.cards)

            if player_total > 21:
                you_won(role, player)
            else:
                # dealers turn
                while calculate_hand(dealer.hand.cards) < 17:
                    hit(dealer.hand, deck)
                
                show_cards(player.hand, dealer.hand, False)
                
                dealer_total = calculate_hand(dealer.hand.cards)

                if dealer_total > 21:
                    you_lost(role, player)
                elif dealer_total < player_total:
                    you_lost(role, player)
                elif dealer_total == player_total:
                    tie(player)
                else:
                    you_won(role, player)

        print('player money: ', player.chips.money)
        # promt for continue, new game or quit
        if player.chips.money <= 0:
            is_continue = False
        promt_to_contionue()







