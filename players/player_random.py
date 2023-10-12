from card import Card
import random as rnd

stop_balance = 1100
hit_threshold = 16

class BlackjackPlayer:
    '''ブラックジャックのプレイヤーを表すクラス

    Attributes:
    ----------
    balance: int
        プレイヤーの残高
    hand: list
        プレイヤーの手札
    dealer_card: Card
        ディーラーの1枚目のカード
    last_dealer_hand: [Card]
        ディーラーが開いた手のリスト
    round: int
        デッキがシャッフルされてからのラウンド数
    
    Methods:
    -------
    place_bet(balance)
        残高の範囲で賭け金を指定する。0を指定するとゲームを終了する
    start_turn(round)
        プレイヤーのターンを開始する。roundはデッキがシャッフルされてからのラウンド数
    receive_hand(hand)
        プレイヤーの手札を記録する
    look_dealer_hand(card)
        ディーラーの1枚目のカードを記録する
    finish_dealer_hand(card)
        ディーラーが開いたカードを記録する
    input(message)
        プレイヤーがヒットかスタンドかの選択をする
    notify_result(result, bet_amount)
        通知された結果に応じてプレイヤーの残高を更新する
    '''

    def __init__(self, balance, stop_balance=stop_balance):
        '''
        Parameters:
        ----------
        balance: int
            プレイヤーの残高
        '''
        self.balance = balance
        self.stop_balance = stop_balance
        self.hand = []

    def __str__(self):
        '''手札と合計を文字列として返す

        Returns:
        -------
        str
            手札と合計を表す文字列
        '''
        return f"手札: {self.hand} 合計: {Card.sum(self.hand)}" # プレイヤーの手札と合計を文字列として返す
    
    def place_bet(self, balance):
        '''プレイヤーの賭け金をランダムに設定する。残高が2000を超えるときは0を指定して終了とする。

        Parameters:
        ----------
        balance: int
            プレイヤーの残高

        Returns:
        -------
        bet_amount: int
            プレイヤーが賭けた金額
        '''
        self.balance = balance
        if balance > self.stop_balance: # 残高がstop_balanceを超えるときは0を指定して終了とする
            return 0
        else:
            bet_amount = rnd.randint(1, balance)
            return bet_amount
            
    def start_turn(self, round):
        '''ターンを開始する。シャッフルされてからのラウンド数を受け取って記録する。
        手札はリセットする。

        Parameters:
        ----------
        round: int
            デッキがシャッフルされてからのラウンド数

        '''
        self.round = round
        self.hand = [] # プレイヤーの手札をリセット

    def receive_hand(self, hand):
        '''配られた手札を記録する

        Parameters:
        ----------
        hand: list
            手札を表すCardクラスのインスタンスのリスト
        '''
        self.hand = hand # プレイヤーの手札を記録

    def look_dealer_hand(self, card):
        '''ディーラーの1枚目のカードを記録する

        Parameters:
        ----------
        card: Card
            ディーラーの1枚目のカードを表すCardクラスのインスタンス
        '''
        self.dealer_card = card # ディーラーの1枚目のカードを記録

    def finish_dealer_hand(self, hand):
        '''ディーラーが開いたカードを記録する

        Parameters:
        ----------
        card: Card
            ディーラーが開いたカードを表すCardクラスのインスタンス
        '''
        self.last_dealer_hand = hand.copy() # ディーラーが開いたカードを記録

    def input(self, message):
        ''' プレイヤーにヒットかスタンドを選択させる

        Parameters:
        ----------
        message: str
            プレイヤーに表示するメッセージ
        
        Returns:
        -------
        choice: str
            プレイヤーが選択した行動 hitかstand
        '''
        choice = rnd.choice(["hit", "stand"])
        return choice
    
    def notify_result(self, result, bet_amount):
        '''プレイヤーの残高を結果によって更新する。結果は以下のいずれか
        - win: プレイヤーが勝利した場合
        - lose: プレイヤーが敗北した場合
        - push: 引き分けの場合
        - それ以外: 無効な結果の場合

        Parameters:
        ----------
        result: str
            結果を表す文字列
        bet_amount: int
            プレイヤーが賭けた金額

        '''
        if result == "win":
            self.balance += bet_amount
        elif result == "lose":
            self.balance -= bet_amount
        elif result == "push":
            pass
        else:
            print("無効な結果です。")
    
