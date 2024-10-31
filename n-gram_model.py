from collections import defaultdict
import numpy as np

class Ngrams:
    def __init__(self, text, n):
        """
        Init the class with the text and number of ngram that we want
        :param text: Text to generate the n-grams
        :param n: unigram, bigram, trigram
        """
        self.text = text.split()  # Divide el texto en una lista de palabras
        self.n = n  # Number of words
        self.ngrams_counts = defaultdict(int)
        self.total_ngrams = 0

    def generate_ngrams(self):
        """
        Generate and count text ngrams
        """
        for i in range(len(self.text) - self.n + 1):
            ngram = tuple(self.text[i:i + self.n])
            self.ngrams_counts[ngram] += 1
            self.total_ngrams += 1
        return list(self.ngrams_counts.items())

    def get_ngram_probability(self, ngram, smoothing='laplace', discount=0.75):
        """
        
        :param ngram: ngram probability 
        :param smoothing: smoothing laplace
        :param discount: value for absolute smoothing
        """
        if smoothing == 'laplace':
            # Laplace smoothing: P(ngram) = (count(ngram) + 1) / (total_ngrams + V)
            vocab_size = len(set(self.text))  # vocab size
            return (self.ngrams_counts[ngram] + 1) / (self.total_ngrams + vocab_size)
        
        elif smoothing == 'absolute_discount':
            # Absolute discounting: P(ngram) = max(count(ngram) - discount, 0) / total_ngrams
            count_ngram = max(self.ngrams_counts[ngram] - discount, 0)
            return count_ngram / self.total_ngrams
        else:
            raise ValueError("Smoothing type not recognized. Use 'laplace' or 'absolute_discount'.")

    def calculate_perplexity(self, test_text):
        """
        Calculate perplexity
        
        :param test_text: test text
        :return: perplexity
        """
        test_words = test_text.split()
        test_ngrams = [tuple(test_words[i:i + self.n]) for i in range(len(test_words) - self.n + 1)]
        log_prob_sum = 0

        for ngram in test_ngrams:
            prob = self.get_ngram_probability(ngram, smoothing='laplace')
            log_prob_sum += -np.log2(prob)

        return 2 ** (log_prob_sum / len(test_ngrams))

# usage
texto = "This is just an example."
ngrams_instance = Ngrams(texto, 2)  # Cambia el número para obtener unigramas, bigramas, trigramas, etc.

# Genereate and count n-grams
ngrams_instance.generate_ngrams()
print("N-grams frequences", ngrams_instance.ngrams_counts)

# Example with Laplace smoothing 
ngram = ("Ejemplo", "de", "texto")
print("Laplace smoothing de n-gram concreto:", ngrams_instance.get_ngram_probability(ngram, smoothing='laplace'))

# Perplexity calculation 
texto_prueba = "Este texto es un ejemplo"
print("Perplexity:", ngrams_instance.calculate_perplexity(texto_prueba))

#if perplexity is slow, better. 
