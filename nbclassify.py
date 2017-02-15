import string, math, sys, getopt
class ClassParams:
    'This class is reposnsible to maintain the data related to different types of classes like "Truthful", "Deceptive" etc.. '

    def __init__(self, class_params):
        self.no_of_reviews = int(class_params[0])
        self.no_of_words = int(class_params[1])
        self.prior_prob = float(class_params[2])

    def getWordCount(self):
        return self.no_of_words

    def getDocCount(self):
        return self.no_of_reviews

    def getPriorProb(self):
        return self.prior_prob

class Word:

    def __init__(self, word_params):

        self.p_occurrence = int(word_params[0])
        self.n_occurence = int(word_params[1])
        self.t_occurence = int(word_params[2])
        self.d_occurence = int(word_params[3])
        self.cond_probP = float(word_params[4])
        self.cond_probN = float(word_params[5])
        self.cond_probT = float(word_params[6])
        self.cond_probD = float(word_params[7])
        #print "the cond probs are:", self.cond_probP, self.cond_probN, self.cond_probT, self.cond_probD
        self.smoothened_probP = float(word_params[8])
        self.smoothened_probN = float(word_params[9])
        self.smoothened_probT = float(word_params[10])
        self.smoothened_probD = float(word_params[11])
        #print "the smoothened probs are:", self.smoothened_probP, self.smoothened_probN, self.smoothened_probT, self.smoothened_probD

    def getPCount(self):
        return self.p_occurrence

    def getNCount(self):
        return self.n_occurence

    def getTCount(self):
        return self.t_occurence

    def getDCount(self):
        return self.d_occurence

    def getCond_ProbT(self):
        return self.cond_probT

    def getCond_ProbD(self):
        return self.cond_probD

    def getCond_ProbP(self):
        return self.cond_probP

    def getCond_ProbN(self):
        return self.cond_probN

    def getSmoothened_ProbT(self):
        return self.smoothened_probT

    def getSmoothened_ProbD(self):
        return self.smoothened_probD

    def getSmoothened_ProbP(self):
        return self.smoothened_probP

    def getSmoothened_ProbN(self):
        return self.smoothened_probN

def main(argv):
    #read the input from the nbmodel.txt and then form the respective dictioanry to store the data for easy access in the later
    input_parameters = sys.argv[1:]
    model_fd = open("nbmodel.txt", "r")
    model_params = model_fd.read().split("******")
    prior_params = model_params[0]
    smoothened_params = model_params[1]
    prior_params_for_each_class = prior_params.split("\n")
    prior_values = {}
    for prior_data in prior_params_for_each_class:
        class_params = prior_data.strip(" ").split(" ")
        if len(class_params) == 4:
            prior_values[class_params[0]] = ClassParams(class_params[1:])
    words_info = {}
    word_params = smoothened_params.split("\n")
    for word_data in word_params:
        word_stat_list = word_data.strip("\n").strip(" ").split(",")
        if not len(word_stat_list) <=1:
            #print "the length of the word stat list for the word: ", word_stat_list[0], len(word_stat_list)
            words_info[word_stat_list[0]] = Word(word_stat_list[1:])
    #print "All the data for each word is stored successfully"
    #print len(words_info)
    #See if this line qorks fine for all cases.
    testing_fd = open(input_parameters[0], "r")
    output_fd = open("nboutput.txt", "w")
    input_reviews = testing_fd.read().split("\n")
    for review in input_reviews:
        review_words = review.strip(" ").split(" ")
        review_id = review_words[0].strip(" ")
        if not len(review_id) <= 2:
            sentimental_classification = ""
            valid_classification = ""
            #Initialize the classifier values to the prior probabilities of each class.
            classifier_p = math.log10(prior_values.get("positive").getPriorProb())
            classifier_n = math.log10(prior_values.get("negative").getPriorProb())
            classifier_t = math.log10(prior_values.get("truthful").getPriorProb())
            classifier_d = math.log10(prior_values.get("deceptive").getPriorProb())
            for word in review_words[1:]:
                word = word.translate(None, string.punctuation).strip(" ").lower()
                #Ignore if a word is not present in the training data.
                if word in words_info.keys():
                    words_stat = words_info.get(word)
                    classifier_p += math.log10(words_stat.getSmoothened_ProbP())
                    classifier_n += math.log10(words_stat.getSmoothened_ProbN())
                    classifier_t += math.log10(words_stat.getSmoothened_ProbT())
                    classifier_d += math.log10(words_stat.getSmoothened_ProbD())
            if (classifier_p >= classifier_n):
                sentimental_classification = "positive"
            else:
                sentimental_classification = "negative"
            if (classifier_t >= classifier_d):
                valid_classification = "truthful"
            else:
                valid_classification = "deceptive"
            output_fd.write(review_id + " " + valid_classification + " " + sentimental_classification + "\n")
if __name__ == "__main__": main(sys.argv)