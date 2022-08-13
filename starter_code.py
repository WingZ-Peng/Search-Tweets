"""
Please use Python version 3.7+
"""

"""
Zhipeng Peng
Time costed: 
10hr from scratch and coding part. 
3-4hr debug and add more features to support more search parttern 
2hr to write down README.md
"""

from cgi import test
import csv
from readline import insert_text
from threading import local
from typing import List, Tuple
from unittest import result
from xmlrpc.client import Boolean


class TweetIndex:
    # Starter code--please override
    def __init__(self):
        self.list_of_tweets = [] 
        self.tweet_dict_forward = {} 
        self.tweet_dict_back = {}
        self.tweetTime_set = set()

    # Starter code--please override
    def process_tweets(self, list_of_timestamps_and_tweets: List[Tuple[str, int]]) -> None:
        """
        process_tweets processes a list of tweets and initializes any data structures needed for
        searching over them.

        :param list_of_timestamps_and_tweets: A list of tuples consisting of a timestamp and a tweet.
        """
        for row in list_of_timestamps_and_tweets:
            timestamp = int(row[0])
            tweet = str(row[1])
            self.list_of_tweets.append((tweet, timestamp))

        # calling the following two fucntions to init data
        self.dict_helper()
        self.union_all_timestamp()


    def dict_helper(self) -> None:
        """
        dict_helper performs a conversion process, which takes (tweets, timestamp) that existed in 
        the list_of_tweets to store them in the dictionary. Inside this function, I create two 
        dictionaries. The first one is a dictionary with a single word in the tweet as the key, 
        which can help me find the word corresponding timestamp quickly. And to facilitate the 
        operation later, I create a dictionary with timestamp as the key. For example, I need to 
        find the corresponding tweet once get the most recent time. (More details in README.md) 

        Benefit: Since the time complexity (search speed) of the dictionary is O(1), this will 
        greatly speed up the lookup.

        I extract elements directly from self.list_of_tweets and deal with the case insensitive 
        problem by storing in the dictionary of all lowercase letters, so I can use the lower 
        method to convert query to find words.
        """

        # dict1 = {'single word': {time1, time2}}
        for tweet, timestamp in self.list_of_tweets:
            word = tweet.split(" ")
            for w in word:
                # use lower() method to convert
                if w.lower() not in self.tweet_dict_forward:
                    #if word is not in dictionary, init a set that ready to store timestamps
                    self.tweet_dict_forward[w.lower()] = set()
                # store timestamp and avoid duplicate timestamp
                self.tweet_dict_forward[w.lower()].add(timestamp)

        # dict2 = {time: "tweet"}
        for tweet, timestamp in self.list_of_tweets:
            self.tweet_dict_back[timestamp] = tweet


    def union_all_timestamp(self) -> None:
        """
        Union all the timestamps to a set. 
        (More details for this function are in README.md)
        """
        # use the dictionary with the timestamp as key
        for i in self.tweet_dict_back.keys():
            self.tweetTime_set.add(i)
    

    def parentheses_validation(self, query: str) -> Boolean:
        """
        A function to check if the parentheses are valid. 
        Drawback: I assume that every parenthesis is correctly BEFORE or AFTER the letter.

        With this restriction, I only have three cases to check. If the length of the query is
        not longer than 3, then there is no need to check because only a '|' symbol can exist. 
        If it is greater than 3 and there is a left parenthesis then push into stack. if it 
        encounters a right parenthesis, there are two cases here, if stack is not empty then pop 
        out the left parenthesis, if not then it is fasle. Finally, check if there is a left 
        parenthesis inside stack when the '|' symbol is encountered, if not then false.

        param: string type (query)
        return: boolean value: check length of stack is 0 or not
        """
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

    # Starter code--please override
    def search(self, query: str) -> List[Tuple[str, int]]:
        """
        param: String type: query
        return: List[Tuple[str, int]]: result

        In general, I am using stack thinking, pushing each word or symbol as an element 
        into the stack. And only when the right parenthesis is encountered, the elements 
        inside the stack is popped out one by one and processed according to the situation.

        (More Details in README.md)
        """ 
        # return varible
        result : List[Tuple[str, int]] = []

        query_list = query.split(' ')

        # if we are into a or condition, turn on the flag
        or_include_flag = False
        # handle a expression condition when find a no_operator
        no_include_flag = False
        # handle case when word behind a expression
        and_include_flag = False
        # if exist operator 
        if_exist_op = False
        # if exist no_operator in short length (length < 3)
        exist_no_op = False

        # type: Stack. Push words into stack and wait there for calculation 
        # untill a right parenthesis is encountered.
        my_stack = []
        # type: Stack. Store the result of a expression words 
        my_listStack = []
        # type: List. Store words that we don't want ot exist in the final tweet
        no_include_list = []
        # type: Stack. Store words behind a expression
        and_include_stack = []

        # A number to remind the current number of operations in my_stack
        op_num = 0

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
                    # since we need all of words in return tweet, use intersection method to handle set
                    local_tweetTime_set= local_tweetTime_set.intersection(self.tweet_dict_forward[word.lower()])
                    local_flag = True

            if local_flag == True:
                # sort in descending order
                local_tweetTime_set = sorted(local_tweetTime_set, reverse=True)
                # get the top 5 recent tweet and return it
                for time in local_tweetTime_set:
                    if len(result) < 5:
                        result.append((self.tweet_dict_back.get(time), time))
            return result

        
        # search pattern: with operator 
        # first case: a valid query length greater than 3 
        if len(query_list) > 3 and self.parentheses_validation(query) == True and if_exist_op == True:
            # same here, get the union timestamp set
            local_tweetTime_set = self.tweetTime_set
            for word in query_list:
                # A temporary set for store the result of calculation of a word expression 
                # -> will append to my_listStack
                temp_set = set()

                # divide into two cases: or_calculation or and_calculation
                if word[0] == '(':
                    or_include_flag = True
                    and_include_flag = False
                
                # handle no_operator case
                if word[0] == '!':
                    # encounter a expression 
                    if word[1] == '(':
                        no_include_list.append(word[2:])
                        no_include_flag = True
                        continue
                    else:
                        no_include_list.append(word[1:])
                        continue
                
                # handle no_operator experssion case
                if no_include_flag == True:
                    if word == '|' or word == '&':
                        continue
                    else:
                        no_include_list.append(word[:-1])
                        # find two words in a expression and turn off flag 
                        no_include_flag = False
                        continue
                
                # and_operator case 
                if or_include_flag == False:
                    # encouter a case: single word is the last element in list
                    if word == '&':
                        if len(my_stack) == 0 or and_include_flag == True:
                            and_include_flag = True
                        else:
                            curr = my_stack.pop()
                            # find word in dict
                            if curr.lower() in self.tweet_dict_forward:
                                local_tweetTime_set = local_tweetTime_set.intersection(self.tweet_dict_forward[curr.lower()])
                    else:
                        if and_include_flag == True:
                            and_include_stack.append(word)
                        else:
                            my_stack.append(word)

                # into or_operation case now
                else:
                    # record number of parentheses in current word
                    parenthese_index = 0
                    for i in range(len(word)):
                        if word[i] == '(':
                            # retrieve and push to stack
                            my_stack.append('(')
                            parenthese_index += 1

                    # matching
                    if word[i] == '&':
                        my_stack.append('&')
                        # record operator
                        op_num += 1
                    
                    elif word[i] == '|':
                        my_stack.append('|')
                        # record operator
                        op_num += 1
                    
                    # encounter a right parenthesis, pop elements from stack and begin to handle
                    elif word[-1] == ')':
                        # the number of right parentheses in this word 
                        # depends on the number of operators inside my_stack
                        curr = word[:-op_num] # cut off right parentheses to push a complete word
                        # find cooresponding set
                        if curr.lower() in self.tweet_dict_forward:
                            temp_set = temp_set.union(self.tweet_dict_forward[curr.lower()])
                        
                        # pop operator and situational processing
                        operator = my_stack.pop()

                        # matching operator
                        if operator == '&':
                            # pop a word from stack (predecessor)
                            pred = my_stack.pop()
                            if pred.lower() in self.tweet_dict_forward:
                                temp_set = temp_set.intersection(self.tweet_dict_forward[pred.lower()])
                        
                        # there may exist a experssion with experssion case 
                        # or a word with expression case
                        elif operator == '|':
                            # first check length of my_listStack
                            # if not, which means in expression with expression case
                            if len(my_listStack) != 0:
                                curr_set = my_listStack.pop()
                                temp_set = temp_set.union(curr_set)
                            
                            else:
                                # pop a word from stack (predecessor)
                                pred = my_stack.pop()
                                if pred.lower() in self.tweet_dict_forward:
                                    temp_set = temp_set.union(self.tweet_dict_forward[pred.lower()])
                        
                        # append to list
                        my_listStack.append(temp_set)

                        # pop left parenthesis
                        my_stack.pop()
                        # one operator was calculated
                        op_num -= 1

                        # finish or_operator condition
                        if len(my_stack) == 0:
                            or_include_flag = False

                    # keep pushing elements into stack when no right bracket is encountered
                    else:
                        my_stack.append(word[parenthese_index:])

            # first want to check and_operator_stack is empty or not. If not, then intersect 
            while len(and_include_stack) != 0:
                curr = and_include_stack.pop()

                if curr.lower() in self.tweet_dict_forward:
                    local_tweetTime_set = local_tweetTime_set.intersection(self.tweet_dict_forward[curr.lower()])
            
            # then need to check stack is empty or not
            while len(my_stack) != 0:
                operator = my_stack.pop()
                pred = my_stack.pop()
                curr_set = my_listStack.pop()

                if pred == '(':
                    pred_set = my_listStack.pop()
                    curr_set = curr_set.union(pred_set)
                    my_listStack.append(curr_set)
                else:
                    if pred.lower() in self.tweet_dict_forward:
                        curr_set = curr_set.union(self.tweet_dict_forward[pred.lower()])
                    
                    my_listStack.append(curr_set)

                    #pop left parenthesis
                    my_stack.pop()

            # final step to check the result of expression calculation
            my_index = 0
            while my_index < len(my_listStack):
                local_tweetTime_set= local_tweetTime_set.intersection(my_listStack[my_index])
                my_index += 1

            
            # init a set and want to clear no_include_list word
            no_include_set = set()

            for word in no_include_list:
                if word.lower() in self.tweet_dict_forward:
                    no_include_set = no_include_set.union(self.tweet_dict_forward[word.lower()])
            
            # using difference method to clear words
            local_tweetTime_set = local_tweetTime_set.difference(no_include_set)
            # sorted in descending order
            local_tweetTime_set = sorted(local_tweetTime_set, reverse=True)

            # add to return variable
            for time in local_tweetTime_set:
                if (len(result)) < 5:
                    result.append((self.tweet_dict_back.get(time), time))

            return result if len(result) != 0 else []

        # search pattern: with operator but length less than 4. Special case: no parentheses
        elif len(query_list) <= 3 and if_exist_op == True:
            # there exist a no operator '!'
            if exist_no_op == True:
                local_tweetTime_set = self.tweetTime_set
                local_flag = False
                # same step as before
                while len(query_list) != 0:
                    cur = query_list.pop()
                    if cur[0] == '!':
                        curr = cur[1:]
                        if curr.lower() in self.tweet_dict_forward:
                            local_tweetTime_set = local_tweetTime_set.difference(self.tweet_dict_forward[curr.lower()])

                    elif cur == '|':
                        pred = query_list.pop()
                        if pred.lower() in self.tweet_dict_forward:
                            local_tweetTime_set = local_tweetTime_set.union(self.tweet_dict_forward[pred.lower()])
                            local_flag = True
                    else:
                        if cur.lower() in self.tweet_dict_forward:
                            local_tweetTime_set = local_tweetTime_set.intersection(self.tweet_dict_forward[cur.lower()])
                            local_flag = True
                # make sure the query exists some words that is in dictionary
                if local_flag == True:
                    local_tweetTime_set = sorted(local_tweetTime_set, reverse=True)
                    for time in local_tweetTime_set:
                        if len(result) < 5:
                            result.append((self.tweet_dict_back.get(time), time))

                return result

            # case without no operator
            else:
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
                # make sure the query exists some words that is in dictionary
                if local_flag == True:
                    local_tweetTime_set = sorted(local_tweetTime_set, reverse=True)
                    for time in local_tweetTime_set:
                        if len(result) < 5:
                            result.append((self.tweet_dict_back.get(time), time))

                return result
        
        print("There is a Invalid Query! Please check the format and re-enter.")
        return result
                

if __name__ == "__main__":
    # A full list of tweets is available in data/tweets.csv for your use.
    tweet_csv_filename = "../data/small.csv"
    list_of_tweets = []
    with open(tweet_csv_filename, "r") as f:
        csv_reader = csv.reader(f, delimiter=",")
        for i, row in enumerate(csv_reader):
            if i == 0:
                # header
                continue
            timestamp = int(row[0])
            tweet = str(row[1])
            list_of_tweets.append((timestamp, tweet))

    ti = TweetIndex()
    ti.process_tweets(list_of_tweets)
    l = ti.search('hello & neeva & ((needs & bob) | (this & is))') 
    l1 = ti.search('hello & neeva & (me | bob)')
    l2 = ti.search('(me | bob) & hello & neeva')
    l3 = ti.search('hello & neeva & (bob | (this & is))')
    l4 = ti.search('hello & neeva & ((this & is) | bob)')
    l5 = ti.search('hello & neeva & !this')
    l6 = ti.search('hello & neeva & !(this | bob)')
    l7 = ti.search('hello & bob')
    l8 = ti.search('hello & neeva & needs | bob')
    l9 = ti.search('hello bob')
    l10 = ti.search('Bob | this')
    l11 = ti.search('Iamnotbob')
    l12 = ti.search('ssss & vvv & (ffff | nnnn)')
    l13 = ti.search('sss | fff')
    l14 = ti.search('neeva & !hello')
    l15 = ti.search('neeva | !hello')

    print(l)
    print(l1)
    print(l2)
    print(l3)
    print(l4)
    print(l5)
    print(l6)
    print(l7)
    print(l8)
    print(l9)
    print(l10)
    print(l11)
    print(l12)
    print(l13)
    print(l14)
    print(l15)

        
