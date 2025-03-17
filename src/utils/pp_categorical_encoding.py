#Suite of functions for handling the encoding of categorical columns
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

#Apply one hot encoding on a given column
def apply_onehot(df, categorical_cols):
    #Derrive continuous columns
    all_cols = list(df.columns)
    continuous_cols = [x for x in all_cols if x not in categorical_cols]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(drop=None, sparse_output=False), categorical_cols),
            ("num", "passthrough", continuous_cols)
        ]
    )

    data_encoded = preprocessor.fit_transform(df)

    encoded_feature_names = preprocessor.get_feature_names_out()
    df_encoded = pd.DataFrame(data_encoded, columns=encoded_feature_names)

    return df_encoded

#Transform the feature data before applying one-hot encoding
def format_cat_features(df, config_custom, train=True):
    df_enc = df.copy()
    
    #Apply custom functions to specified features
    for col in config_custom.keys():
        pass

    return df_enc