from project import ResultValues
from id3 import ID3

res = ResultValues()

donnees=res.importData("test_public_bin.csv")

precision=res.precision(donnees)

print(precision)
