# Searching Tweets

### Before start to add additional features

There is a bug in the prototype about using **assert** to do test. The problem is that the search function returns a **List Interface**, but the code in the other side of the equal sign is a **Tuple Interface**, which leads to an AssertionError. The solution is to add **[ ]** to the test code to complete the output of success, or we can change **search function** to Tuple Interface.

### My first approach to this project

After reading the pdf document at first glance. For the three different requirements:
  - The first requirement will involve the use of data structures and the design of the program. And I think the first one will be done while I work on and optimize the other two rquirements. 

  - Skip the first one and I begin my second requirement directly, my first thought was that the output was most closely related to time, so I could first sort the data from the CVS file by time as key, which would allow me to quickly find the most prioritized tweet. In the subsequent optimization process, I think the dictionary data structure fits well here since it makes my query speed up to O(1), which is more efficient than the previous method. And this decision has made it easier for me to complete the third step.

  - The most complex and difficult step is to handle or_operator in this requirment. The reason could be that the combinations of words and operation symbols would be too flexible and diverse, as well as the need to verify validity and search. I thought stack might be a good helper, it can effectively help me to calculate when I get the operation symbols. And I have designed the search pattern as two patterns: one without operators and one with operators. There are some case may in the first one without operators:
    1. **'hello bob'**
    2. **'a-non-existent-word'**
    3. **'hello bob a-non-existent-word'**

   For second pattern, I started with the situation as described in the doc. Here we want to split the case into two because I think query of length 3 or less does not need parentheses, while length greater than 3 requires valid parentheses. In other words, a length 3 or less can direct return True.

    1. For queries of length less than or equal to 3, there may be two cases here:
        1). **'Noovi | Neeva'** or **'sss | fff'** #(non-existent-words)
        2). **'Noovi | !Neeva'** or **'Noovi & !Neeva'** #(or_operator is in the same word as Neeva)

    2. Following is the queries of length that are greater than 3, and here we may want to more focus on word or expression. Drawback: I assume the OR operator is between a single word/expression. Here is word | word format
        1). **'Noovi & is & (fast | quick)'**
        2). **'(fast | quick) & Noovi & is'**
        3). **'Noovi & is & !(fast | quick)'** #(or_operator case)
        4). **'ssss & vvv & (ffff | nnnn)'** #(non-existent-words)

    3. word with expression
        1). **'Noovi & is & (fast | (very & quick))'**
        2). **'Noovi & is & ((very & quick) | fast)'**
        3). **'(fast | (very & quick)) & Noovi & is'**

    4. expression with expression
        1). **'hello & neeva & ((needs & bob) | (this & is))'**
    
    5. for no valid combination: I through the validation function to check if it's going to be processed

    6. Commom case
        1). **'hello & neeva & !this'**

  I roughly divided this step into these small problems, sorted out the relationship between them and then started coding.

### Run Program
Same as before ```sh python starter_code.py ```

### First Step: Return the top 5 most recent (time integer is the greatest) tweets instead of a single tweet

1.  My first thought is to construct a list to store 5 tweets and return it. Then it occurred to me that the order of the tweets might affect the speed of the search.

2.  I plan to change the order of tweets in the storage since we always want to search the top 5 most recent tweets faster

    - **(only focus on highest time)** To reverse `list_of_tweets` directly. **Concerns**: there may be some out-of-order timeStamp. For example, timeStamp 0 after timeStamp 3 in small.cvs. In order to solve it, I decide to sort it first.

      ```python
      # sort timeStamp in descending order by using bubbleSort
      n = len(list_of_tweets)

      for i in range(n):
          for j in range(n - i - 1):
              if (list_of_tweets[j][1] < list_of_tweets[j + 1][1]):
                  list_of_tweets[j], list_of_tweets[j + 1]
                        = list_of_tweets[j + 1], list_of_tweets[j]
      ```

      Then add a condition to Search funciton if the length of return list is less than 5 and tweet_contains_query is true, we will keep append tweet into return list.

      ```python
       storeTemp = []
       if tweet_contains_query and len(storeTemp) < 5:
          storeTemp.append((tweet, timestamp))
      ```

      However, this is not a good idea to do it because the **time complexity is still O(n)** for searching.

    - I realize that using dict is a good way since the **time complexity will be O(1)**. So we can inital **dict = {'each word in tweet' : [timeStamp1, timeStamp2...]}**.
      **Concerns**: we may store duplicate values in list. For example, (9, hello hello) in small.cvs will produce {'hello': [9, 9]}
      Since every timeStamp is uniquely number and we only want to check if the word exists in the tweet corresponding to the timeStamp. A good way to solve it is by using **Set**, it is also relatively easy to use the intersection method to find a common timeStamp.

      So I plan to solve it in this way:

      ```python
        tweet_dict = dict()

        for tweet, timestamp in list_of_tweets:
            word = tweet.split(" ")
            for w in word:
                if w not in tweet_dict:
                    tweet_dict[w] = set()

                tweet_dict[w].add(timestamp)

        print(tweet_dict)

        # output: {'hello': {1, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15}, 'this': {4, 6, 10, 11, 15}, 'is': {4, 6, 10, 11, 15}, 'also': {15}, 'neeva': {4, 5, 7, 10, 11, 15}, 'not': {14}, 'me': {5, 13, 14, 6}, 'stuff': {12}, 'bob': {11}, 'world': {8}, 'bye': {3}, 'some': {2}, 'tweet': {2}, 'yay': {0}}

      ```

      Then we can arrive the intersectin part. Since we are using intersection math concept, I inital it by adding all of timeStamps. However, to make it easier to add and subsequently find tweets by timestamp, we can create a new dict: **dict2 = {timestamp, tweet}**

      ```python
      tweet_dict2 = dict()

      for tweet, timestamp in list_of_tweets:
         tweet_dict2[timestamp] = tweet

      print(tweet_dict)

      # output: {15: 'hello this is also neeva', 14: 'hello not me', 13: 'hello me', 12: 'hello stuff', 11: 'hello neeva this is bob', 10: 'hello neeva this is neeva', 9: 'hello hello', 8: 'hello world', 7: 'neeva', 6: 'hello this is me', 5: 'hello neeva me', 4: 'hello this is neeva', 3: 'hello bye', 2: 'some tweet', 1: 'hello', 0: 'yay'}

      # inital the set
      tweetTime_set = set()
      # adding
      for i in tweet_dict2.keys():
         tweetTime_set.add(i)

      print(tweetTime_set) # output: {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}

      # intersection all of words occurrence in query with tweetTime_set
      for word in list_of_words:
         if word in tweet_dict:
             tweetTime_set = tweetTime_set.intersection(tweet_dict[word])

      print(tweetTime_set) # output: {4, 5, 10, 11, 15}
      ```

      Finally, we use a similar procedure, first sort and then append to the final return list.

      ```python
      tweetTime_set = sorted(tweetTime_set, reverse=True)

      for time in tweetTime_set:
          if (len(storeTemp) < 5):
              storeTemp.append([tweet_dict2.get(time), time])

      # sample ouput of (['hello', 'neeva']): [['hello this is also neeva', 15], ['hello neeva this is bob', 11], ['hello neeva this is neeva', 10], ['hello neeva me', 5], ['hello this is neeva', 4]]
      ```

### Second step: handle seach operator

1. For the implementation of the feature without operators, I first traversed the query, and if I found '&' or '｜' in it, I would turn on a switch, which would lead to another search pattern. Meanwhile, if I find out '!' which means I have to be prepared for a query input of length less than or equal to 3 (**'Noovi & !Neeva'**), following is the code for this section.

```python
# search if exist operator
for i in range (len(query)):
    if query[i] == '&' or query[i] == '|':
        if_exist_op = True
    elif query[i] == '!':
        exist_no_op = True
        
# search pattern: without operator
 if if_exist_op == False:
    # check word if exist in dictionary
    local_flag = False
    # get the union timestamp set
    local_tweetTime_set = self.tweetTime_set
    # begin for-loop to iterate each word in query 
    for word in query_list:
        if word.lower() in self.tweet_dict_forward:
            # since we need all of words in return tweet, 
            # use intersection method to handle set
            local_tweetTime_set= local_tweetTime_set.intersection(
                self.tweet_dict_forward[word.lower()])
            local_flag = True
```

2. For query inputs of length less than or equal to 3, I have divided them into two cases, if we are not found '!' in last step. And known the format is 'word operator word', we will simply pop the elements from the stack and use word as key to search it if it in the dictionary. Then when we find the symbols, we design the computation pattern as a first step and then pop another word with the result of the previous step to continue the computation. Until the length of the stack is 0, we stop the loop, part of the codes is as follow:
```python
local_flag = False
local_tweetTime_set = self.tweetTime_set
# no need to check no operator, need to check the only one operator
while len(query_list) != 0:
    curr = query_list.pop()
    if curr.lower() in self.tweet_dict_forward:
        local_tweetTime_set = local_tweetTime_set.intersection(self.tweet_dict_forward[curr.lower()])
        local_flag = True

    elif curr == '|':
        pred = query_list.pop()
        if pred.lower() in self.tweet_dict_forward:
            local_tweetTime_set = local_tweetTime_set.union(self.tweet_dict_forward[pred.lower()])
            local_flag = True
```

In the other case, our switch is turned on. In this way we use set difference method with its corresponding timestamps to the set of all timestamp
```python
# there exist a no operator '!'
if exist_no_op == True:
    local_tweetTime_set = self.tweetTime_set
    local_flag = False

    while len(query_list) != 0:
        cur = query_list.pop()
        if cur[0] == '!':
            curr = cur[1:]
            if curr.lower() in self.tweet_dict_forward:
                local_tweetTime_set = local_tweetTime_set.difference(self.tweet_dict_forward[curr.lower()])
```

3. Here is about (word with word) and (word with expression) cases. In the first case, when we encounter a left parenthesis, we flip a switch to the or-operator case, where we use a temp_set to first store the result inside the parenthesis, and then append it to a list until the final operation. After processing all the other results of this query, the results of the list are extracted for the final computation. Also, if we encounter the not-operator case, we will turn on another switch. This way we force the corresponding word or expression to be stored in a list and then perform the final computation. In the second case, sub-first case is that there is still a word and an operation symbol and a left parenthesis inside the stack, the sub-second case there is still an operation symbol and a left parenthesis, and in the sub-third case there is only a left parenthesis left.The reason these three happen is because I use the stack thinking, processing a query from back to front, and in an expression after a word, we finish processing the expression and store it in temp_set and wait for the union with the previous result. But the loop has ended and the stack is not empty, so we will pop the elements of the stack again for calculation. If it is an expression in front of a word, so the stack of peek will be a operation symbol, so we have to go to store the previous expression results inside the list_stack, pop out the results for calculation and then in append to wait to calculate with all the timestamp. The last is a case where after processing all the OR operations go back to the normal AND operation so that the operator will be in front of the word, e.g. **& word1 & word2**. Here we will convert to the normal front-to-back order for processing. # Since the code for handling this part is too long, please go back to the start-code to check out it.

4. I run the logic of the last step that is the expression before the word to handle this relationship, the drawback is that unpredictable bugs occur when handling multiple expressions. e.g. (expression | expression | expression...)

5. Regarding verifying that the query is valid, I do it by going to verify that it matches the brackets correctly.
```python
def parentheses_validation(self, query: str) -> Boolean:
    # type Stack
    parentheses_checker_stack = []

    if len(query) <= 3:
            return True
    else:
        for i in range (len(query)):
            # push directly
            if query[i] == '(':
                parentheses_checker_stack.append(query[i])
            # second case: two cases here to wait for check
            elif query[i] == ')':
                # length is not equal to 0, pop()
                if len(parentheses_checker_stack) != 0:
                    parentheses_checker_stack.pop()
                # empty stack, cannot pop return false
                else:
                    return False
            # third case
            elif query[i] == '|':
                if '(' not in parentheses_checker_stack:
                    return False
    
    # check the length if equals to 0
    return len(parentheses_checker_stack) == 0
```

6. This step is what happens if find a word with '!', store the word in a list the same as pervious steps, and after processing the other words, process it finally with difference method.


### Further goal
This project brought me a great experience. Although my work is not yet very dynamic to support more flexible and decentralized patterns, I feel the passion and motivation from it, and the desire to learn about this search engine aspect.