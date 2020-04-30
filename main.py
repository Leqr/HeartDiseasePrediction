from project import ResultValues
from id3 import ID3

res = ResultValues()

arbre=res.task1()

classification1=arbre.classifie({
    'age': 3, 'sex': 0,
    'cp': 3, 'trestbps': 1,
    'chol': 2, 'fbs': 0,
    'restecg': 2, 'thalach': 0,
    'exang': 4, 'oldpeak': 0,
    'slope': 3, 'ca': 0,
    'thal': 1})

print(res.only_class(classification1))
