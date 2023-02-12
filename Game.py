class Game:
    
    def __init__(self, filename):
        
        with open(filename) as f:
            lines = f.readlines()

        self.words = [a[0:5] for a in lines]
        self.filename = filename

        
    def play_full(self, algo_name):
        
        correctly_guessed = []
        wrongly_guessed = []
        self.algo_name = algo_name
        guesses = Parallel(n_jobs=NUM_CPUS)(delayed(self.play_one)(secret_word) for secret_word in self.words)
        correctly_guessed = [a for a,b in zip(self.words,guesses) if b]
        wrongly_guessed = [a for a,b in zip(self.words,guesses) if not b]
        accuracy = 100*len(correctly_guessed)/(len(guesses))
        
        return accuracy, correctly_guessed, wrongly_guessed

    
    def play_one(self, secret_word):
        
        A = self.algo_name(self.filename)
            
        for i in range(6):

            word = A.word_selection()
            correct, status = self.word_check(secret_word, word)

            if correct == 1:

                return 1

            A.word_result(word, status)

        return 0
            
            
    
    def word_check(self, secret_word, word):
        
        if secret_word == word:
            
            return 1, [1]*5
        
        else:
            
            status = [0]*5
            
            for i in range(5):
                
                if word[i] == secret_word[i]:
                    
                    status[i] = 1
                    
                elif word[i] in secret_word:
                    
                    status[i] = 2
                    
            return 0, status