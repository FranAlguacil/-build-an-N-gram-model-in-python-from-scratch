# -*- coding: utf-8 -*-
"""syntax.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tJ6AmT9JJCc0K7JJlqmxt5iKse4XD_GZ

# BUILD A N-GRAM MODEL

This code defines a function called preprocess_corpus that takes a path to a text corpus file as input. The function reads in the corpus file, converts all the text to lowercase, removes punctuations from the text, splits the text into sentences, removes any empty sentences, and tokenizes each sentence into a list of words. Finally, the function returns a list of lists, where each inner list represents a tokenized sentence from the original text corpus.
"""    
import nltk       #useful to treat with language model
import numpy as np   #operations with logs

nltk.download('brown')
corpus = nltk.corpus.brown
sentences = corpus.sents(categories='news')
tokenized_sentences = [[w.lower() for w in sent] for sent in sentences]


class NgramModel:
    def __init__(self, n, smoothing=0.01):      #Try to use MLE and Vocabulary from nltk.lm but didn't work 
        self.n = n
        self.vocab = set()
        self.ngram_counts = {}
        self.context_counts = {}
        self.smoothing = smoothing  
       
    def train(self, sentences):  #Define and train an N-gram
        for sent in sentences:
            padded_sent = ['<s>'] * self.n + sent + ['</s>']
            for i in range(self.n, len(padded_sent)):
                ngram = tuple(padded_sent[i - self.n:i])
                context = tuple(padded_sent[i - self.n:i - 1])  #fixed the error: : 'list' object has no attribute 'lookup' solucionalo
                self.vocab.add(padded_sent[i])
                if ngram in self.ngram_counts:
                    self.ngram_counts[ngram] += 1
                else:
                    self.ngram_counts[ngram] = 1
                if context in self.context_counts:
                    self.context_counts[context] += 1
                else:
                    self.context_counts[context] = 1

    def prob(self, word, context):
        context_count = self.context_counts.get(context, 0)
        ngram = context + (word,)
        ngram_count = self.ngram_counts.get(ngram, 0)
        prob = (ngram_count + self.smoothing) / (context_count + self.smoothing * len(self.vocab))
        return prob

    def sentence_logP_score(self, sentence):
        padded_sent = ['<s>'] * self.n + sentence + ['</s>']
        logP = 0
        for i in range(self.n, len(padded_sent)):
            ngram = tuple(padded_sent[i - self.n:i])
            context = tuple(padded_sent[i - self.n:i - 1])
            logP += np.log2(self.prob(padded_sent[i], context))
        return logP

    def generate(self, n_words=10):
        sentence = ['<s>'] * self.n
        for i in range(n_words):
            context = tuple(sentence[-self.n + 1:])    #Fixed: generate() got an unexpected keyword argument 'context'
            words = list(self.vocab)
            probs = [self.prob(w, context) for w in words]
            max_prob = max(probs)
            candidates = [word for word, prob in zip(words, probs) if prob == max_prob]
            sentence.append(candidates[0])
        return sentence[self.n:]

    def perplexity(self, sentence):  #Evaluation
        prob_sentence = self.sentence_logP_score(sentence)
        num_words = len(sentence)
        perplexity = 2 ** (-prob_sentence / num_words)
        return perplexity

    def sentence_interpolated_logP(S, vocab, uni_counts, bi_counts, tri_counts, lambdas=[0.5, 0.3, 0.2], alpha=1):
      tokens = ['*', '*'] + S + ['STOP']
      prob = 0
      for u, v, w in nltk.ngrams(tokens, 3):
        uni_prob = np.log(uni_counts[u] / sum(uni_counts.values()))
        bi_prob = np.log(bi_counts[(u, v)] / uni_counts[u])
        tri_prob = np.log(tri_counts[(u, v, w)] / bi_counts[(u, v)])
        prob += lambdas[0] * tri_prob + lambdas[1] * bi_prob + lambdas[2] * uni_prob
        return prob
