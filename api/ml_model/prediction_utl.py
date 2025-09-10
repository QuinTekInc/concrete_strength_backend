

from sklearn.preprocessing import LabelEncoder


def processAge(cement_age: int):
    if cement_age == 7:
        return 'early'
    elif cement_age == 14:
        return 'mid'
    else:
        return 'late'


def vectorize(**kwargs):
    return []
