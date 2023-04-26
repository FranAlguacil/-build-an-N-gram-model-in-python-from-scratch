#Laplace
def prob(self, word, context):
      context_count = self.context_counts.get(context, 0)
      ngram = context + (word,)
      ngram_count = self.ngram_counts.get(ngram, 0)
      prob = (ngram_count + 1) / (context_count + len(self.vocab))  #Apply laplace adding +1
      return prob


# Absolute discounting
def prob(self, word, context):
      context_count = self.context_counts.get(context, 0)
      ngram = context + (word,)
      ngram_count = self.ngram_counts.get(ngram, 0)
      discount = self.discount * len(self.ngram_counts)
      if context_count == 0:
          prob = 1 / len(self.vocab)
      else:
          prob = max(ngram_count - self.discount, 0) / context_count + discount * self.prob(word, context[:-1])
      return prob