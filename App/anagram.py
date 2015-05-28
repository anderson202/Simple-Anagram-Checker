#**********************************************************
# Assignment2:
# UTOR user_name: ngho8
# First Name: Anderson Ho Yin
# Last Name: Ng
# Student # 1001544386
#
#
# Honour Code: I pledge that this program represents my own
# program code and that I have coded on my own. I received
# help from no one in designing and debugging my program.
# I have also read the plagiarism section in the course info sheet
# of CSC 148 and understand the consequences. #*********************************************************

import time
from letterManager import LetterManager
class InvalidAnagramLength(Exception):
    pass

class AnagramSolver:

    def __init__ (self, listOfWords):
        '''Constructor takes a list of words (dict.txt) and turns it into a python dictionary
        '''
        self.word_dic = {}
        for word in listOfWords:
                self.word_dic[word] = LetterManager(word)

    def generateSmallerDict(self, listOfList):
        '''method to generate and return a smaller dictionary
        '''
        smaller_dict = {}
        for lst in listOfList:
            smaller_dict[lst[0]] = lst[1]
        return smaller_dict

    def constructList(self, s, dict):
        '''method to generate and return a list of relevant words (ie words that can be subtracted by s)
        '''
        relevant = []
        s_manager = LetterManager(s)                        #LetterManager of the current string s
        for (word, manager) in sorted(dict.items()):          #takes all the strings that have length < length (s)
            if len(word) <= len(s):                         #subtract them, if they are relevant then return as
                if s_manager.Subtract(manager)!= None:      #list with new string s_current and word + manager of the
                    s_current = s_manager.Subtract(manager) #relevant word
                    relevant.append([word, manager, s_current])
        return relevant


    def generateAnagramsHelper (self, max, relevant_list):
        '''recursive method that generates anagrams one by one and then concatenates with higher level results
        '''
        if max < 0:
            raise InvalidAnagramLength("cannot have negative length anagram")

        all_anagrams = []
        smaller_dict = self.generateSmallerDict(relevant_list)  #computes for a smaller dictionary to look through
                                                                #for the next recursive call
        for relevant_info in relevant_list:
            if relevant_info[2].IsEmpty(): #BASE CASE  If all letters used up (ie LetterManager.Size() == 0)
                all_anagrams.append([relevant_info[0]])

            else:                          #RECURSIVE CASE If some letters used up (ie LetterManager.Size()>0)
                #recursive call, will a smaller dictionary
                temp_anagrams = self.generateAnagramsHelper(max, self.constructList(str(relevant_info[2]), smaller_dict))

                 #go through for loop and add each relevant word to each list inside the returned all_anagram
                for each_anagram in temp_anagrams:
                    if len([relevant_info[0]]+each_anagram)<= max or max == 0:
                        all_anagrams.append([relevant_info[0]]+each_anagram)

        return(all_anagrams)

    def generateAnagrams (self, s, max): #MAIN PROGRAM
        #create the first list with the whole dictionary
        relevant_list = self.constructList(s, self.word_dic)
        return self.generateAnagramsHelper(max, relevant_list)

if __name__ == "__main__":
    f = open("dict.txt")
    words = []
    for line in f:
        words.append(line.strip())

    count = 0
    a = AnagramSolver(words)
    userInput=input("Please enter a word to check for its anagrams: ")
    userMax=input("Please enter the max number of words used to form the anagram: ")
    print(a.generateAnagrams(userInput, int(userMax)))
