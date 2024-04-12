import random

liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

tokens = ['tokenB', 'tokenA', 'tokenC', 'tokenD', 'tokenE']

def reset_liquidity():
    return {
        ("tokenA", "tokenB"): (17, 10),
        ("tokenA", "tokenC"): (11, 7),
        ("tokenA", "tokenD"): (15, 9),
        ("tokenA", "tokenE"): (21, 5),
        ("tokenB", "tokenC"): (36, 4),
        ("tokenB", "tokenD"): (13, 6),
        ("tokenB", "tokenE"): (25, 3),
        ("tokenC", "tokenD"): (30, 12),
        ("tokenC", "tokenE"): (10, 8),
        ("tokenD", "tokenE"): (60, 25),
    }

def arb_path(liquidity, path, verbose=False):
    amount = 5
    amount_track = [amount]
    for i in range(len(path)-1):
        t_in, t_out = path[i], path[i+1]
        
        if (tokens[t_in], tokens[t_out]) in liquidity:
            key = (tokens[t_in], tokens[t_out])
            reverse = False
        else:
            key = (tokens[t_out], tokens[t_in])
            reverse = True
        
        reserve_in, reserve_out = liquidity[key] if not reverse else liquidity[key][::-1]
        
        amount_in_with_fee = amount * 0.997
        amount_out = (amount_in_with_fee * reserve_out) / (reserve_in + amount_in_with_fee)

        if not reverse:
            liquidity[key] = (reserve_in + amount / 1E18, reserve_out - amount_out / 1E18)
        else:
            liquidity[key] = (reserve_out - amount_out / 1E18, reserve_in + amount / 1E18)
        
        amount = amount_out
        amount_track.append(amount)
        

    if(verbose and amount > b_final_expected):
        print(f"Token balance before each swap: {amount_track}")

    return amount


b_final_expected = 20
found = False

while(not found): 
    liquidity_current = reset_liquidity()

    path = [0] + random.sample([1, 2, 3, 4], 3) + [0]
    tokenB_final = arb_path(liquidity_current, path)

    if tokenB_final > b_final_expected:
        path_str = '->'.join(tokens[i] for i in path)
        print(f"Path: {path_str}, tokenB balance = {tokenB_final:6f}")
        found = True
        break