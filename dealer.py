from random import shuffle
from card import Card

# デッキのカードを生成
suits = ["♡", "♢", "♠", "♣"]
values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
deck = [Card(suit, value) for suit in suits for value in values]
# デッキをシャッフル
shuffle(deck)

round = 1  # ゲームのラウンド数。Deckの残りが少なくなったらデッキをシャッフルする。その際、ラウンド数をリセットする。

def turn_end():
    global deck, round
    if len(deck) < 52*penetration: # デッキの残りが4枚以下になったらデッキを作り直してシャッフルする
        deck = [Card(suit, value) for suit in suits for value in values]
        print("デッキをシャッフルします。")
        shuffle(deck)
        round = 1
    round += 1 # ラウンド数を1増やす
    print("次のラウンドを開始します。")

# ペネトレーション率を設定
penetration=0.5

# BlackjackPlayer クラスをインポート
from player import BlackjackPlayer

# ゲームの初期設定
player_hand = []  # プレイヤーの初期手札
dealer_hand = []  # ディーラーの初期手札
initial_balance = 1000  # プレイヤーの初期残高

# プレイヤーとディーラーを作成
player = BlackjackPlayer(initial_balance)
player_balance = initial_balance # player_balanceはプレイヤーの残高を表す変数。ディーラー側でも管理する。


# プレイヤーのターン
while True:
    player_hand = [] # プレイヤーの手札をリセット
    dealer_hand = [] # ディーラーの手札をリセット
    is_burst = False # プレイヤーがバーストしたかどうかを表す変数

    player.start_turn(round) # プレイヤーのターンを開始
    # プレイヤーの賭け金を設定
    bet_amount = player.place_bet(player_balance)
    if 0 < bet_amount <= player_balance: # プレイヤーの賭け金が有効ならば
        print(f"プレイヤーの掛け金は ${bet_amount}")
    else:
        if bet_amount == 0:
            print(f"プレイヤーの残高は ${player_balance}です。ゲームを終了します。") # プレイヤーの残高を表示
            exit()
        print("掛け金が無効です。ゲームを終了します。")
        exit()

    # カードをプレイヤーとディーラーに配る
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())

    # プレイヤーの手札とディーラーの1枚目のカードを表示
    print("ディーラーの表のカード:", str(dealer_hand[0]))

    # プレイヤーの手札の合計を表示
    print("プレイヤーの手:", [str(card) for card in player_hand])
    player.receive_hand(player_hand) # プレイヤーに手札を渡す
    print("プレイヤーの点数:", Card.sum(player_hand))


    player.look_dealer_hand(dealer_hand[0]) # プレイヤーにディーラーの1枚目のカードを見せる

    # プレイヤーの手札の合計が21以下の場合はヒットかスタンドを選択
    while True:
        player_choice = player.input("hit or stand？: ")
        if player_choice == "hit":
            print("プレイヤーがカードを引きます。")
            player_hand.append(deck.pop())
            player.receive_hand(player_hand)
            print("プレイヤーの手:", [str(card) for card in player_hand])
            player.receive_hand(player_hand) # プレイヤーに手札を渡す
            print("プレイヤーの点数:", Card.sum(player_hand))
                # プレイヤーの手札の合計が21を超えたらバースト
            if Card.sum(player_hand) > 21:
                print("バースト！")
                player_balance -= bet_amount # プレイヤーの残高から賭け金を差し引く
                player.notify_result("lose", bet_amount) # プレイヤーに結果を通知
                is_burst = True
                break
            continue
        elif player_choice == "stand":
            break
        else:
            print("無効な入力です。")
            continue


    # プレイヤーがスタンドを選択した場合はディーラーのターンに移る
    print("ディーラーがカードを表にします。")
    print("ディーラーの手:", [str(card) for card in dealer_hand])
    print("ディーラーの点数:", Card.sum(dealer_hand))
    # ディーラーは合計が17点以上になるまでヒットを続ける
    while True:
        # ただし、ソフト17の時はヒットする
        if Card.sum(dealer_hand) == 17 and Card.is_soft(dealer_hand):
            dealer_hand.append(deck.pop())
            print("ディーラーがカードを引きました。")
            print("ディーラーの手:", [str(card) for card in dealer_hand])
            print("ディーラーの点数:", Card.sum(dealer_hand))
        else:
            if Card.sum(dealer_hand) < 17:
                dealer_hand.append(deck.pop())
                print("ディーラーがカードを引きました。")
                print("ディーラーの手:", [str(card) for card in dealer_hand])
                print("ディーラーの点数:",Card.sum(dealer_hand))
            else:
                break

    player.finish_dealer_hand(dealer_hand) # プレイヤーにディーラーの手札を見せる

    # ディーラーの手札の合計が21を超えたらバースト
    if Card.sum(dealer_hand) > 21:        
        print("ディーラーがバーストしました。")
        if not is_burst:
            player_balance += bet_amount # プレイヤーの残高に賭け金を加算
            player.notify_result("win", bet_amount) # プレイヤーに結果を通知
            continue

    if is_burst:
        if player_balance <= 0:
            print("残高がゼロになりました。ゲームを終了します。")
            break
        else:
            turn_end()
            continue

    # プレイヤーとディーラーの手札の合計を比較して勝敗を決定
    if Card.sum(player_hand) > Card.sum(dealer_hand):
        if Card.is_blackjack(player_hand):
            print("ブラックジャック！")
            player_balance += int(bet_amount * 1.5) # プレイヤーの残高に賭け金の1.5倍を加算
            player.notify_result("win", int(bet_amount*1.5))
        else:
            print(f"プレイヤーの勝ち！ ${bet_amount}を獲得しました。")
            player_balance += bet_amount # プレイヤーの残高に賭け金を加算
            player.notify_result("win", bet_amount) # プレイヤーに結果を通知
    elif Card.sum(player_hand) < Card.sum(dealer_hand):
        print(f"プレイヤーの負け！ ${bet_amount}を失いました。")
        player_balance -= bet_amount # プレイヤーの残高から賭け金を差し引く
        player.notify_result("lose", bet_amount) # プレイヤーに結果を通知
    else: # プレイヤーとディーラーの手札の合計が同じ場合は引き分け
        if Card.is_blackjack(player_hand): # ただし、プレイヤーがブラックジャックの場合はプレイヤーの勝ち
            if Card.is_blackjack(dealer_hand): # プレイヤーとディーラーがブラックジャックの場合は引き分け
                print("引き分け！")
                player.notify_result("push", bet_amount)
            else:
                print("ブラックジャック！")
                player_balance += int(bet_amount * 1.5)
                player.notify_result("win", int(bet_amount*1.5))
        else:
            print("引き分け！")
            player.notify_result("push", bet_amount) # プレイヤーに結果を通知(引き分け)

    if player_balance <= 0:
        print("残高がゼロになりました。ゲームを終了します。")
        break
    else:
        print(f"残高: ${player_balance}")

    turn_end()
