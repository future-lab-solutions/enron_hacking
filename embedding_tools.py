import spacy
from scipy import spatial

#classification: https://spacy.io/usage/training#textcat

class NlpTool(object):
    """This tool uses spacy to produce NLP functions that tackle commonly needed functionality. 

    In many cases these functions purely offer a shorthand, more readable version of spacy functionality. 

    Attributes:
        nlp: The spacy nlp object
        total_words: creates easier access to self.nlp.vocab.length
    """
    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')
        self.total_words = self.nlp.vocab.length
    

    def GetEmbeddingsForText(self, tokens, remove_no_vectors=True):
        """"Returns a list of vectors for the tokens.
        Args:
            tokens: spacy Doc object containing tokens
            remove_no_vectors: if True, splits the tokens that don't have a vector from those that do.
        Returns:
            token_vectors: A list containing the vectors of each token (will contain the 0-vector if token doesn't have a vector and remove_no_vectors==False)
            no_vectors: A list containing the tokens which don't have vectors (empty list if remove_no_vectors==False)
        """
        token_vectors = []
        no_vectors = []

        if(remove_no_vectors):
            for token in tokens:
                if(token.has_vector):
                    token_vectors.append(token.vector)
                else:
                    no_vectors.append(token)
        else:
            token_vectors = [token.vector for token in tokens]

        return token_vectors, no_vectors
    

    def GetNoVectorList(self, tokens):
        """"Returns a list of the input tokens which don't have vectors.
        Args:
            tokens: spacy Doc object containing tokens
        Returns:
            A list containing the tokens which don't have vectors.
        """
        return [token for token in tokens if not token.has_vector]


    def FindSimilarWords(self, word_vector):
        """"Returns a sorted list of words from the vocab that are sorted by their similarity to the input word vector.
        Args:
            word_vector: A vector from the word embedding space.
        Returns:
            computed_similarities: 
        """
        print(self.MostSimilarWordToVector(word_vector))
        word = self.WordKeyToWord(self.MostSimilarWordToVector(word_vector)[0])
        by_similarity = sorted(word.vocab, key=lambda w: word.similarity(w), reverse=True)
        return [w.orth_ for w in by_similarity[:10]]

        cosine_similarity = lambda x, y: 1 - spatial.distance.cosine(x, y)
        
        computed_similarities = []
        
        
        print("Total Words: "+str(self.total_words))
        word_check_count = 0
        for word in self.nlp.vocab:
            word_check_count += 1
            if(word_check_count % 1000 == 0):
                print("Checking Word: "+ str(word_check_count))
            # Ignore words without vectors
            if not word.has_vector:
                continue
        
            similarity = cosine_similarity(word_vector, word.vector)
            computed_similarities.append((word, similarity))

            computed_similarities = sorted(computed_similarities, key=lambda item: -item[1])
        
        return computed_similarities


    def MostSimilarWordToVector(self, vector):
        return self.nlp.vocab.vectors.most_similar(vector.reshape(1,vector.shape[0]))


    def GetVectorForWord(self, word_string):
        vector = None
        if(word_string in self.nlp.vocab):
            token = self.nlp.vocab[word_string]
            if token.has_vector:
                vector = token.vector
        return vector

    
    def WordKeyToWord(self,word_key):
        return self.nlp.vocab[word_key]


if __name__ == "__main__":
    nlp_tool = NlpTool()

    nin_vec = nlp_tool.GetVectorForWord("nintendo")
    print(nin_vec)
    
    nintendo_word = nlp_tool.MostSimilarWordToVector(nin_vec)
    print(nintendo_word)

    similar_words = nlp_tool.FindSimilarWords(nin_vec)

    print(nintendo_word)
    print(similar_words)




