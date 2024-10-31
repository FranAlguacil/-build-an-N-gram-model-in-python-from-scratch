class Ngrams:
    def __init__(self, text, n):
        """
        :param text: Texto a partir del cual se generarán los n-gramas.
        :param n: Número de palabras por n-grama (1 para unigramas, 2 para bigramas, etc.).
        """
        self.text = text.split()  # text for split
        self.n = n  # N count 

    def generate_ngrams(self):
        """
        Genera y retorna una lista de n-gramas.
        """
        ngrams_list = []
        for i in range(len(self.text) - self.n + 1):
            ngram = tuple(self.text[i:i + self.n])  
            ngrams_list.append(ngram)
        return ngrams_list

    def get_frequent_ngrams(self, top=10):
        """
        Calcula y retorna los n-gramas más frecuentes en el texto.

        :param top: Número de n-gramas más frecuentes a devolver.
        """
        ngrams_list = self.generate_ngrams()
        frequency = {}

        # count frequence
        for ngram in ngrams_list:
            if ngram in frequency:
                frequency[ngram] += 1
            else:
                frequency[ngram] = 1

        # Sorted n-grams by frequence 
        sorted_ngrams = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        return sorted_ngrams[:top]

# Ejemplo de uso
texto = "Este es un ejemplo de texto para generar n-gramas y contar su frecuencia"
ngrams_instance = Ngrams(texto, 2)  # Cambia el número para obtener unigramas, bigramas, trigramas, etc.

# Generar y mostrar los n-gramas y los más frecuentes
print("N-gramas generados:", ngrams_instance.generate_ngrams()[:5])  # Muestra los primeros 5 n-gramas como ejemplo
print("N-gramas más frecuentes:", ngrams_instance.get_frequent_ngrams(top=5))
