from project import ResultValues
from id3 import ID3

res = ResultValues()

donnees=res.importData("test_cure.csv")
res.cure(donnees)
