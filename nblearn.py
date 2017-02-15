import string, sys

class ClassParams:
    'This class is reposnsible to maintain the data related to different types of classes like "Truthful", "Deceptive" etc.. '

    def __init__(self):
        self.no_of_reviews = 0
        self.no_of_words = 0
        self.prior_prob = 0.0

    def increaseWordCount(self, number_of_words):
        self.no_of_words += number_of_words

    def increaseDocCount(self):
        self.no_of_reviews += 1

    def getWordCount(self):
        return self.no_of_words

    def getDocCount(self):
        return self.no_of_reviews

    def setPriorProb(self, prior_prob):
        self.prior_prob = prior_prob

    def getPriorProb(self):
        return self.prior_prob

class Word:

    def __init__(self):
        self.p_occurrence = 0
        self.n_occurence = 0
        self.t_occurence = 0
        self.d_occurence = 0
        self.cond_probP = 0.0
        self.cond_probN = 0.0
        self.cond_probT = 0.0
        self.cond_probD = 0.0
        self.smoothened_probP = 0.0
        self.smoothened_probN = 0.0
        self.smoothened_probT = 0.0
        self.smoothened_probD = 0.0


    def increaseRespectiveCount(self, truthfulness, positiveness):
        if positiveness == True:
            self.p_occurrence += 1
        else:
            self.n_occurence += 1
        if truthfulness == True:
            self.t_occurence += 1
        else:
            self.d_occurence += 1

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

    def setCond_ProbT(self, prob):
        self.cond_probT = prob

    def setCond_ProbD(self, prob):
        self.cond_probD = prob

    def setCond_ProbP(self, prob):
        self.cond_probP = prob

    def setCond_ProbN(self, prob):
        self.cond_probN = prob



    def getSmoothened_ProbT(self):
        return self.smoothened_probT

    def getSmoothened_ProbD(self):
        return self.smoothened_probD

    def getSmoothened_ProbP(self):
        return self.smoothened_probP

    def getSmoothened_ProbN(self):
        return self.smoothened_probN

    def setSmoothened_ProbT(self, prob):
        self.smoothened_probT = prob

    def setSmoothened_ProbD(self, prob):
        self.smoothened_probD= prob

    def setSmoothened_ProbP(self, prob):
        self.smoothened_probP = prob

    def setSmoothened_ProbN(self, prob):
        self.smoothened_probN = prob



class Label:
    'This class constructs objects which are passed as values to the global dictionary review_labels'

    def __init__(self, review_params):
        global review_labels
        self.truthfulness = True
        self.positiveness = True
        if len(review_params) == 3:
            if review_params[1] == "truthful":
                #print "Setting up the value to True for truthfulness"
                self.truthfulness = True
            else:
                self.truthfulness = False
            if review_params[2] == "positive":
                self.positiveness = True
            else:
                self.positiveness = False
        review_labels[review_params[0]] = self

    #Returns the truthfuness of the review whose reference is passed as the argument
    def getTruthfulness(self):
        return self.truthfulness

    #Returns the positiveness of the review whose reference is passed as the argument.
    def getPositiveness(self):
        return self.positiveness

def main(argv):
  #review_label which is global and contains "review_id" key and it's classes as values. Can be accessed through the program
  # and contains the crucial data for the model parameters.
  global review_labels
  global total_no_of_reviews
  # dict used to maintain the data such as number of docs that are classified as positive in the training data.
  global classes_data
  global words_in_reviews
  review_labels = {}
  input_parameters = sys.argv[1:]
  train_text = input_parameters[0]
  train_label = input_parameters[1]
  fd_labels =  open(train_label, "r")
  label_data = fd_labels.read().split("\n")
  for review_info in label_data:
      review_params = review_info.strip().split(" ")
      Label(review_params)
  '''for review_id in review_labels.keys():
      print "key is:" +review_id + " the value is :",  str(review_labels.get(review_id, None).getTruthfulness())'''

  #Maintain a dictionary which maps to a string and ClassParams object.
  # The dictiory may help us to retrive the values and modify them.
  classes_data = {}
  class_types = ["positive", "negative", "truthful", "deceptive"]
  for c in  class_types:
      classes_data[c] = ClassParams()
  #print len(classes_data)

  #Now split the reviews into a list.
  fd_reviews = open(train_text, "r")
  reviews_collection = fd_reviews.read().split("\n")
  total_no_of_reviews = len(reviews_collection)
  global word_data
  word_data = {}
  # Need to start pardsing the review one after the other. This is the most important feature of the application.
  #Need to be careful while parsing the review.
  for review in  reviews_collection:
      #stripped first.
      review = review.strip(" ")
      #know just get the review_id
      review_id_length = review.find(" ")
      review_id = review[0:review_id_length]
      #print "reviewid retrieved is: " + review_id
      #print ( review_labels.has_key(review_id) )
      isReviewTruthful = review_labels.get(review_id).getTruthfulness()
      isReviewPositive = review_labels.get(review_id).getPositiveness()
      words_in_review = review.split(" ")
      number_of_words_in_review = 0
      for word in words_in_review[1:]:
          #Remove punctuations and convert it into lower case
          word = word.translate(None, string.punctuation).strip(" ").lower()
          #You can add for a stop word condition here.
          if not word == "":
              number_of_words_in_review += 1
              if( word_data.has_key(word) ):
                  # Increase the word count in each of the classes linked to this word, for that we need the truthfulness and positiveness
                  # of the current review.
                word_data.get(word).increaseRespectiveCount(isReviewTruthful, isReviewPositive)
              else:
                  word_data.setdefault(word, Word())
                  word_data.get(word).increaseRespectiveCount(isReviewTruthful, isReviewPositive)
      #Perform operations on the class data, change the number of documents classified to this class and also no.of words occurred.
      if isReviewPositive == True:
          operational_class = classes_data.get("positive")
          operational_class.increaseWordCount(number_of_words_in_review)
          operational_class.increaseDocCount()
      else:
          operational_class = classes_data.get("negative")
          operational_class.increaseWordCount(number_of_words_in_review)
          operational_class.increaseDocCount()
      if isReviewTruthful == True:
          operational_class = classes_data.get("truthful")
          operational_class.increaseWordCount(number_of_words_in_review)
          operational_class.increaseDocCount()
      else:
          operational_class = classes_data.get("deceptive")
          operational_class.increaseWordCount(number_of_words_in_review)
          operational_class.increaseDocCount()

  #Need to print the model parameters into a nbmodel.txt file.
  output_file = open("nbmodel.txt", "w")
  #output_file.write("******\n")
  #output_file.write("This could be the sample output in the feature from the nbclassify\n")

  # Need to print the class data, number of documents classified into that category.
  #print "Class Info:\n"
  for cls in class_types:
      class_info = classes_data.get(cls)
      #print cls + " " + str(class_info.getDocCount()) + " " + str(class_info.getWordCount()) + " " + str(total_no_of_reviews)
      # setting up the prior probabilities for each class. storing them back in the instance.
      prior_prob = float(class_info.getDocCount()) / total_no_of_reviews
      #print "prior probability for class %s is %f", cls, prior_prob
      class_info.setPriorProb(prior_prob)
      output_file.write(cls + " " + str(class_info.getDocCount()) +" "+ str(class_info.getWordCount()) +" "+ str(prior_prob) +"\n")
  output_file.write("******\n")


  #Just print the word data just to make sure that everything is working fine.
  total_unique_words = len(word_data)
  for word in word_data.keys():
      word_info = word_data.get(word)
      #Now, calculate the before and after smoothening values for each word.
      for class_type in  class_types:
          class_info = classes_data.get(class_type)
          count_denom = class_info.getWordCount()
          if class_type == "positive":
              count_numerator = word_info.getPCount()
              cond_prob = float( count_numerator) / count_denom
              word_info.setCond_ProbP(cond_prob)
              smoothened_prob = float( (count_numerator + 1)) / (count_denom + total_unique_words)
              word_info.setSmoothened_ProbP(smoothened_prob)
          elif class_type == "negative":
              count_numerator = word_info.getNCount()
              cond_prob = float(count_numerator) / count_denom
              word_info.setCond_ProbN(cond_prob)
              smoothened_prob = float((count_numerator + 1)) / (count_denom + total_unique_words)
              word_info.setSmoothened_ProbN(smoothened_prob)

          elif class_type == "truthful":
              count_numerator = word_info.getTCount()
              cond_prob = float(count_numerator) / count_denom
              word_info.setCond_ProbT(cond_prob)
              smoothened_prob = float( (count_numerator + 1)) / (count_denom + total_unique_words)
              word_info.setSmoothened_ProbT(smoothened_prob)
          else:
              count_numerator = word_info.getDCount()
              cond_prob = float(count_numerator) / count_denom
              word_info.setCond_ProbD(cond_prob)
              smoothened_prob = float((count_numerator + 1)) / (count_denom + total_unique_words)
              word_info.setSmoothened_ProbD(smoothened_prob)
      #print data into the output file, for each word.

      output_file.write( word + "," + str(word_info.getPCount()) + "," + str(word_info.getNCount()) + "," + str(word_info.getTCount()) + "," + str(word_info.getDCount()) + ","
                        + str(word_info.getCond_ProbP()) + "," + str(word_info.getCond_ProbN()) + "," + str(word_info.getCond_ProbT()) + ","
                        + str(word_info.getCond_ProbD()) + "," + str(word_info.getSmoothened_ProbP()) + "," + str(word_info.getSmoothened_ProbN()) + ","
                       + str(word_info.getSmoothened_ProbT()) + "," + str(word_info.getSmoothened_ProbD()) + "\n")

  #print "Total Number of unique words: %d", len(word_data)
  #Print all the parameters we built into an text file.

if __name__ == "__main__" :main(sys.argv)
