# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> Path: tokenB->tokenA->tokenD->tokenC->tokenB, tokenB balance = 20.129889
> |Swap    |amountIn |amountOut |
> |----------|----------|-----------|
> |B -> A|5|5.655322|
> |A -> D|5.655322|2.458781|
> |D -> C|2.458781|5.088927|
> |C -> B|5.088927|20.129889
> 

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Slippage is the difference between the expected price and the real price of a trade. In Automated Market Makers (AMM) like Uniswap V2, slippage occurs due to the nature of the constant product formula x * y = k, where x and y represent the quantities of two different tokens in the liquidity pool, and k is a constant value. As the size of a trade increases relative to the pool's size, it significantly changes the x/y ratio, leading to a different price compared to when the transaction was initiated.
> 
> To mitigate this, Uniswap V2 provides mechanisms to specify the worst acceptable trade execution to ensure that users don't experience more slippage than they can tolerate. This is done via **"amountInMax"** or **"amountOutMin"**. A case  is the function **"swapExactTokensForTokens"**. This function will revert if the actual output is less than **"amountOutMin"**, ensuring that the user does not experience a higher slippage than is acceptable to them.

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> In Uniswap V2, when the first liquidity is provided to a new pair, a certain amount of liquidity tokens, specifically MINIMUM_LIQUIDITY which is usually set to 1000 tokens, is minted and then locked inside the contract. This is done by sending these tokens to the address(0), effectively removing them from circulation.
> 
> Rationale behind this design:
> 1. Prevent Division By Zero: AMM formulas require dividing by the liquidity in a pool. The MINIMUM_LIQUIDITY ensures that the pool never starts from zero, preventing division by zero in calculations.
> 2. Initial Price Setting: This minimum liquidity acts as a placeholder to establish the initial state and price of the liquidity pool without giving the first provider an oversized control over the pool's pricing.
> 3. Ownership Share: With this design, no single liquidity provider owns 100% of the pool at the onset. The 'burnt' tokens mean no one can be a single-point owner or claim complete early profits.
> 4. Early Pool Manipulation Protection: It prevents the first liquidity provider from manipulating the pool early on by being able to remove all liquidity at once.

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> When depositing tokens into a Uniswap V2 Pair for not the first time, the amount of liquidity (LP tokens) minted for the depositor is determined by the following formula: 
>
> $$ liquidity = min\{\frac{amount0}{reserve0}, \frac{amount1}{reserve1}\} * totalSupply $$
> The intention behind this formula is to ensure that the new liquidity is added to the pool at the current price ratio between the two assets. It prevents dilution or unfair advantage by ensuring that new liquidity providers can only obtain LP tokens proportional to the amount of liquidity they're adding to the pool relative to the pool's existing size. This ensures that the share of the pool a liquidity provider receives is fair, equitable, and corresponds to the value they add.
> 
> This formula maintains the relative value of all LP tokens by adding new liquidity at the current token price ratio. It safeguards the consistency of the value of each LP token, preserving the integrity of the pool by preventing disproportionate minting of LP tokens and avoiding the shift of the pool's price. This is essential for the trustless and automated nature of AMMs like Uniswap V2.


## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

> A sandwich attack is a type of front-running attack specific to decentralized exchange (DEX) environments. It occurs when a malicious actor spots a pending swap transaction from a user that will significantly affect the price of a trading pair due to slippage. The attacker executes two transactions, one before and one after the user's transaction, to profit from the price impact created by the user's swap.
> 
> **Impact on the User's Swap:**
> 1. **Worse Execution Price:** The user's swap is executed at a less favorable price due to the front-running transaction increasing the asset's price just before their buy order, or decreasing it just prior to their sell order.
> 2. **Increased Slippage:** The front-running transaction by the attacker can push the slippage higher than what the user might have anticipated, leading to an even worse rate and a higher cost for the trade.
> 3. **Reduced Returns:** If the user is selling, the backrunning transaction (the one the attacker performs after the user's swap) can push down the price, reducing the user's sale revenue.
> 
> **Example of a Sandwich Attack:**
> 
> 1. **Detection:** Attacker detects a user's pending transaction to buy a large amount of Token A with Token B.
> 2. **Front-Running:** Attacker buys Token A with Token B just before the user's transaction, increasing the price of Token A.
> 3. **User Swap:** The user's transaction goes through, buying Token A at the new, inflated price.
> 4. **Back-Running:** Attacker sells the recently purchased Token A back into Token B after the user's transaction, profiting from the now elevated price of Token A.
> 
> DEXes like Uniswap can mitigate the risk of sandwich attacks by allowing users to set maximum slippage tolerances. However, it remains a risk, especially for large trades on pairs with low liquidity. Users should remain aware of slippage settings and possibly use tools or services that protect against such exploits.

