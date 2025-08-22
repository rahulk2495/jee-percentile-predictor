import streamlit as st
import pandas as pd


# Sample dummy data
sample_data = {
    "female": [1, 0, 1, 0],
    "tenth_math_final": [95, 88, 76, 82],
    "tenth_sci_final": [92, 85, 79, 88],
    "pcm": [1, 1, 0, 1],
    "general": [0, 1, 0, 0],
    "obc": [1, 0, 0, 0],
    "sc": [0, 0, 1, 0],
    "st": [0, 0, 0, 1]
}
df_sample = pd.DataFrame(sample_data)



# ======== Replace these with your Stata regression results =========
coef = {
    "const": 196.1998,   # intercept from regression
    "female": -6.343773,
    "tenth_math_final": -2.527548,
    "tenth_math_final_sq": .0201622,
    "tenth_sci_final": -2.540661,
    "tenth_sci_final_sq": .0197534,
    "pcm": 3.020236,
    "general": -.3160913,
    "obc": -.8654527,
    "sc": -.6053456,
    "st": 0.0    # base category (reference group)
}
# ===================================================================

def predict(df):
    """Apply regression equation to dataframe"""
    df = df.copy()
    df["math_sq"] = df["tenth_math_final"]**2
    df["sci_sq"] = df["tenth_sci_final"]**2
    df["predicted_percentile"] = (
        coef["const"]
        + coef["female"]*df["female"]
        + coef["tenth_math_final"]*df["tenth_math_final"]
        + coef["tenth_math_final_sq"]*df["math_sq"]
        + coef["tenth_sci_final"]*df["tenth_sci_final"]
        + coef["tenth_sci_final_sq"]*df["sci_sq"]
        + coef["pcm"]*df["pcm"]
        + coef["obc"]*df["obc"]
        + coef["sc"]*df["sc"]
        + coef["st"]*df["st"]
        + coef["general"]*df["general"]
    )
    return df

# ------------------ STREAMLIT APP ------------------
st.title("📊 JEE Mains Percentile Predictor (Demo)")

# -------------------
# Model description
# -------------------
st.markdown("""

### 📖 What Regression Means  
Regression is a statistical method used to understand the relationship between one **outcome variable** (here: JEE Mains Percentile) and a set of **predictor variables** (like gender, class 10 math/science marks, PCM VS PCMB, and social categories).  
In simple terms:  
> Regression finds the **best-fitting equation** that can predict JEE Mains Percentiles from a student’s background and academic data.
                       
            
### 📘 About This Model
This model predicts **JEE Mains Percentiles** using:
- Gender
- Class 10th Math & Science scores (with quadratic terms)
- PCM stream indicator (PCM VS PCMB)
- Social category (General, OBC, SC, ST)


            
            
            
            
            
### 📘 Regression Equation for Predicted Percentile

        
Predicted Percentile = 196.20  - 6.34 × Female  - 2.53 × Math + 0.0202 × Math²  - 2.54 × Science + 0.0198 × Science²  + 3.02 × PCM  - 0.32 × General  - 0.87 × OBC  - 0.61 × SC



### ✅ Accuracy (from regression)
- R² = **0.428** About 43% of variation in JEE Mains Percentiles is explained by this model 
- Adj R² = **0.368**  
- Root MSE = **19.0** ((average prediction error is ~19 percentile))
            
### ✅ Accuracy (from Prediction)
- **Accuracy = 80.2%**  
  > Percentage of all students correctly predicted (both qualified & not qualified).  
- **Sensitivity (Recall for Qualified) = 48.0%**  
  > Of all students who actually qualified, how many were correctly predicted as qualified.  
- **Specificity (Recall for Not Qualified) = 92.9%** 
  > Of all students who did not qualify, how many were correctly predicted as not qualified.
- **Sensitivity (true positives / qualified detected)**: 72.6%

            

### 📂 Data Requirements
Upload an **Excel file (.xlsx)** with columns (Make sure the columns are named as follows):
- `female` (0 for female and 1 for male)  
- `tenth_math_final` (10th CBSE Mathematics score out of 100)  
- `tenth_sci_final`  (10th CBSE Science score out of 100)
- `pcm` (1 for PCM and 0 for PCMB)
- `general` (1 for general student and 0 otherwise)
- `obc` (1 for OBC and 0 otherwise)
- `sc`  (1 for SC and 0 otherwise)
- `st`  (1 for ST and 0 otherwise)            
""")














st.write("Upload your Excel file with student data and get predicted JEE Mains Percentiles.")





# File upload
use_sample = st.checkbox("Use sample data instead of uploading Excel?")

if use_sample:
    df = df_sample.copy()
    st.write("Using sample data:")
    st.dataframe(df)
    
    # Predict
    df_pred = predict(df)
        
    st.write("### Predicted Percentiles")
    st.dataframe(df_pred[["predicted_percentile"]].head(20))
        
    # Summary statistics
    st.write("### Performance Summary")
    st.write(df_pred["predicted_percentile"].describe())
        
            
    # Download option
    output_file = "predicted_scores.xlsx"
    df_pred.to_excel(output_file, index=False)
        
        
    
    with open(output_file, "rb") as f:
        st.download_button("⬇️ Download Predictions", f, file_name="predicted_scores.xlsx")

else:
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
    
        st.write("### Preview of Uploaded Data")
        st.dataframe(df.head())
    
        # Predict
        df_pred = predict(df)
        
        st.write("### Predicted Percentiles")
        st.dataframe(df_pred[["predicted_percentile"]].head(20))
        
        # Summary statistics
        st.write("### Performance Summary")
        st.write(df_pred["predicted_percentile"].describe())
        
            
        # Download option
        output_file = "predicted_scores.xlsx"
        df_pred.to_excel(output_file, index=False)
        
        
    
        with open(output_file, "rb") as f:
            st.download_button("⬇️ Download Predictions", f, file_name="predicted_scores.xlsx")
        
    
    







