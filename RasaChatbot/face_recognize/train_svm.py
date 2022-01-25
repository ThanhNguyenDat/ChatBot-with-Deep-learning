import pickle
from sklearn import svm

# load data from 2 file pkl
file = open("face_data/landmarks.pkl", "rb")
landmark_list = pickle.load(file)
file.close()

file = open("face_data/labels.pkl", "rb")
label_list = pickle.load(file)
file.close()

svm = svm.SVC(kernel='linear')
svm.fit(landmark_list, label_list)  # train

result = svm.predict([landmark_list[0]])
print("Result: {} Label: {}".format(result, label_list[0]))

model_file = "../face_models/model.sav"
file = open(model_file, 'wb')
pickle.dump(svm, file)
file.close()
# train model SVM
