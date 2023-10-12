# Card クラスを定義

vals = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10, "A":11}

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.suit}{self.value}"

    @staticmethod
    def sum(cards):
        '''カードの合計を計算する。ただし、Aは11として計算し、合計が21を超えている場合はAを1として計算する
        '''
        total = sum([vals[card.value] for card in cards]) # カードの合計を計算
        num_aces = sum(1 for card in cards if card.value == "A") # 手札に含まれるAの枚数を数える

        while total > 21 and num_aces: # num_acesが0でない間、totalが21を超えている場合はAを1として計算する
            total -= 10
            num_aces -= 1

        return total
    
    @staticmethod
    def is_blackjack(cards):
        '''手札がブラックジャックかどうかを判定する
        '''
        return Card.sum(cards) == 21 and len(cards) == 2 and "A" in [card.value for card in cards]

    @staticmethod
    def is_soft(cards):
        '''手札がソフトかどうかを判定する。判定方法は、手札にAが含まれていて、Aを11として計算できる場合はソフトとする
        '''
        total = sum([vals[card.value] for card in cards]) # カードの合計を計算
        num_aces = sum(1 for card in cards if card.value == "A") # 手札に含まれるAの枚数を数える

        while total > 21 and num_aces: # num_acesが0でない間、totalが21を超えている場合はAを1として計算する
            total -= 10
            num_aces -= 1
        
        if num_aces > 0 and total <= 21:
            return True
        else:
            return False
