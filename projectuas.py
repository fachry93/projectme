import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
from skimage.feature import hog

def load_images_from_folder(folder):
    images = []
    labels = []
    for subdir in os.listdir(folder):
        subpath = os.path.join(folder, subdir)
        if os.path.isdir(subpath):
            label = subdir  # Use the folder name as the label
            for filename in os.listdir(subpath):
                img_path = os.path.join(subpath, filename)
                if os.path.isfile(img_path) and img_path.endswith(('png', 'jpg', 'jpeg')):
                    img = cv2.imread(img_path)
                    img = cv2.resize(img, (128, 128))
                    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    hog_features, _ = hog(img_gray, block_norm='L2-Hys', pixels_per_cell=(16, 16), visualize=True)
                    images.append(hog_features)
                    labels.append(label)
    return np.array(images), np.array(labels)

# Load dataset
dataset_folder = r"C:\Users\fachr\Downloads\jagung"
X, y = load_images_from_folder(dataset_folder)

# Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the SVM model with cross-validation for better parameter tuning
param_grid = {'C': [0.1, 1, 10, 100], 'kernel': ['linear', 'rbf']}
svm_model = GridSearchCV(SVC(), param_grid, cv=5)
svm_model.fit(X_train_scaled, y_train)

# Evaluate the model
y_pred = svm_model.predict(X_test_scaled)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Dynamically determine the unique classes in the test set
unique_classes = np.unique(y_test)
target_names = label_encoder.inverse_transform(unique_classes)

print("Classification Report:\n", classification_report(y_test, y_pred, target_names=target_names))

# Function to predict and display image with health status
def predict_image(image_path, model, scaler, label_encoder):
    img = cv2.imread(image_path)
    img_resized = cv2.resize(img, (128, 128))
    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    hog_features, _ = hog(img_gray, block_norm='L2-Hys', pixels_per_cell=(16, 16), visualize=True)
    img_scaled = scaler.transform([hog_features])
    prediction = model.predict(img_scaled)
    label = label_encoder.inverse_transform(prediction)[0]
    
    # Display the image with the predicted label using matplotlib
    plt.imshow(cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB))
    plt.title(f'Prediction: {label}')
    plt.axis('off')
    plt.show()
    
    return label

# Example usage
new_image_path = r"C:\Users\fachr\Downloads\daunsakit.jpg"
result = predict_image(new_image_path, svm_model, scaler, label_encoder)
print("The plant is:", result)
