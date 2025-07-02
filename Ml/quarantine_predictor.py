from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

df = df.dropna(subset=['quarantine_days', 'age', 'gender'])
df['gender_encoded'] = df['gender'].map({'Male': 0, 'Female': 1})

X = df[['age', 'gender_encoded']]
y = df['quarantine_days']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LinearRegression().fit(X_train, y_train)
