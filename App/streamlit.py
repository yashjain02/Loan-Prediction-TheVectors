import requests
import streamlit as st


def FileTypeEntry():
    st.header("Loan Prediction")
    file = st.file_uploader("upload file", type=["csv"])
    show_file = st.empty()
    if not file:
        show_file.info("Please upload a file".format(''.join(["csv"])))
        return
    filepath = '../data/' + file.name
    if st.button("Predict"):
        postUrl = "http://127.0.0.1:8000/fileType?myfiles=" + filepath
        response = requests.post(postUrl)
        prediction = response.text
        prediction = prediction.replace('"', '')
        listRes = list(prediction.split(" "))
        pred = []
        for i in listRes:
            if i == 'N':
                pred.append('Yes')
            else:
                pred.append('No')
        st.dataframe(pred)


def Indiviual_entry():
    product_list = [st.text_input("Loan_ID"), st.selectbox("Gender", ["Male", "Female"]),
                    st.selectbox("Married", ["Yes", "No"]), st.selectbox("Dependents", ["0", "1", "2"]),
                    st.selectbox("Education", ["Graduate", "Non-Graduate"]),
                    st.selectbox("Self_Employed", ["Yes", "No"]), st.text_input("Applicant Income"),
                    st.text_input("CoApplicant Income"), st.text_input("Loan Amount"),
                    st.text_input("Loan Amount Term"),
                    st.selectbox("Credit_History", ["1", "0"]),
                    st.selectbox("Property_Area", ["Urban", "Semi-Urban", "Rural"])]
    data = {
        'Loan_ID': product_list[0],
        'Gender': product_list[1],
        'Married': product_list[2],
        'Dependents': product_list[3],
        'Education': product_list[4],
        'Self_Employed': product_list[5],
        'ApplicantIncome': product_list[6],
        'CoapplicantIncome': product_list[7],
        'LoanAmount': product_list[8],
        'Loan_Amount_Term': product_list[9],
        'Credit_History': product_list[10],
        'Property_Area': product_list[11],
    }
    if st.button("Predict"):
        postUrl = "http://127.0.0.1:8000/individualEntry"
        response = requests.post(postUrl, json=data)
        prediction = response.text
        print(prediction)
        if prediction == "N":
            st.success(f"He will return the loan")
        else:
            st.error(f"Sorry!! Customer will not return the loan")


if __name__ == "__main__":
    Select_type_entry = st.sidebar.selectbox("Select the type of input", ["On Demand Prediction", "File Type"])
    if Select_type_entry == "File Type":
        FileTypeEntry()
    else:
        Indiviual_entry()
