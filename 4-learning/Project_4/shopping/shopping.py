import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    evidence = []
    labels = []

    months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    with open(filename, mode='r') as file:
        csv_reader = csv.reader(file)

        next(csv_reader) # skip over header

        for row in csv_reader:
            evidence.append([
                int(row[0]),   # Administrative, an integer
                float(row[1]), # Administrative_Duration, a floating point number
                int(row[2]),   # Informational, an integer
                float(row[3]), # Informational_Duration, a floating point number
                int(row[4]),   # ProductRelated, an integer
                float(row[5]), # ProductRelated_Duration, a floating point number
                float(row[6]), # BounceRates, a floating point number
                float(row[7]), # ExitRates, a floating point number
                float(row[8]), # PageValues, a floating point number
                float(row[9]), # SpecialDay, a floating point number
                months.index(row[10]),  # Month, an index from 0 (January) to 11 (December)
                int(row[11]),  # OperatingSystems, an integer
                int(row[12]),  # Browser, an integer
                int(row[13]),  # Region, an integer
                int(row[14]),  # TrafficType, an integer
                1 if row[15] == 'Returning_Visitor' else 0, # VisitorType, an integer 0 (not returning) or 1 (returning)
                1 if row[16] == 'TRUE' else 0, # Weekend, an integer 0 (if false) or 1 (if true)
            ])

            labels.append(1 if row[17] == 'TRUE' else 0)

    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    model = KNeighborsClassifier(n_neighbors=1)

    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    TP, TN, FP, FN = 0, 0, 0, 0

    for label, prediction in zip(labels, predictions):
        if prediction and label:
            TP += 1
        elif prediction and not label:
            FP += 1 
        elif not prediction and not label:
            TN += 1 
        elif not prediction and label:
            FN += 1
    
    sens = TP/(TP+FN)
    spec = TN/(TN+FP)

    return sens, spec


if __name__ == "__main__":
    main()
