import json
import keras
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import tokenizer_from_json

vocab_length = 10000
max_seq_length = 902
# Load models
with open('./Binaries/tokenizer.json') as f:
  data = json.load(f)
  tokenizer = tokenizer_from_json(data)
  
ie_model = keras.models.load_model("./Binaries/IE_model.keras")
ns_model = keras.models.load_model("./Binaries/NS_model.keras")
tf_model = keras.models.load_model("./Binaries/TF_model.keras")
jp_model = keras.models.load_model("./Binaries/JP_model.keras")

# Function to classify MBTI type

def predict_mbti_type(text,):
  """
  Preprocesses the provided text and uses the trained model to predict the MBTI type.

  Args:
    text: A string containing the text to be classified.

  Returns:
    A string representing the predicted MBTI type.
  """
  pred=""
  # Preprocess the text
  stop_words = stopwords.words('english')
  text = text.lower()
  text = text.split()
  text = [word.strip() for word in text]
  text = [word for word in text if word not in stop_words]

  # Tokenize the text
  text = tokenizer.texts_to_sequences([text])

  # Pad the sequence
  text = pad_sequences(text, maxlen=max_seq_length, padding='post')
  print(text)

  # Make the prediction
  prediction = ie_model.predict(text)
  print(prediction)
  if prediction < 0.5:
    pred+= 'I'
  else:
    pred+= 'E'

  prediction = ns_model.predict(text)
  print(prediction)
  if prediction < 0.5:
    pred+= 'N'
  else:
    pred+= 'S'

  prediction = tf_model.predict(text)
  print(prediction)
  if prediction < 0.5:
    pred+= 'T'
  else:
    pred+= 'F'

  prediction = jp_model.predict(text)
  print(prediction)
  if prediction < 0.5:
    pred+= 'J'
  else:
    pred+= 'P'

  return pred
# Example usage
text = "Fair enough.|||If you feel you can make a plan that will let you and the future child thrive (and no, this doesn't mean white picket fence, a BMW in the driveway and private school education), then by all means...|||No, it's based on getting you to think it through rather than spoon feeding you the answers.  So, what's you answer to my question?    No, that would be you, as pointed out above.  But yes,...|||When people are in a relationship (a healthy one at any rate) there is emotional give and take that flows both ways.  A text message not only completely, irrevocably and callously cuts off that flow....|||Seriously?  You can't figure out WHY a two second text message would piss someone off?  1) it's quick, impersonal and dismissive.  2) it's impersonal"
predicted_mbti_type = predict_mbti_type(text)
print(f"Predicted MBTI type: {predicted_mbti_type}")