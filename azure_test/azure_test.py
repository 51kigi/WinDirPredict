# The script MUST include the following function,
# which is the entry point for this module:
# Param<dataframe1>: a pandas.DataFrame
# Param<dataframe2>: a pandas.DataFrame
def azureml_main(dataframe1 = None, dataframe2 = None):
    # import required packages
    import pandas as pd
    import nltk
    import numpy as np
    # tokenize the review text and store the word corpus
    word_dict = {}
    token_list = []
    for text in dataframe1["Col2"]:
        tokens = nltk.word_tokenize(text.decode('utf8'))
        token_list.append(tokens)
        for word in tokens:
            word_dict[word] = 1
        # build sequence order for word corpus
    for index, word in enumerate(word_dict.keys()):
        word_dict[word] = index
        # build feature vector for all records
    feature_vector_list = []
    for index, item in enumerate(token_list):
        feature_vector = [0] * (len(word_dict) + 1)
        for word in item:
            feature_vector[word_dict[word]+1] = 1
        feature_vector[0] = dataframe1["Col1"][index]
        feature_vector_list.append(feature_vector)
      # convert feature vector to dataframe object
    dataframe_output = pd.DataFrame(np.array(feature_vector_list), columns=['rating']+word_dict.keys())
    return [dataframe_output]