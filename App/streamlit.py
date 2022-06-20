import requests
import streamlit as st
import json
import pandas as pd


def FileTypeEntry():
    st.markdown("<h1 style='text-align: center; color: white;'>Loan Prediction</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("upload file", type=["csv"])
    if uploaded_file is not None:
        file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type,
                        "filesize": uploaded_file.size}
        # st.write(file_details)
        df = pd.read_csv(uploaded_file)
        data = df.to_dict(orient='records')
        # st.dataframe(df)
    show_file = st.empty()
    if not uploaded_file:
        show_file.info("Please upload a file".format(''.join(["csv"])))
        return
    if st.button("Predict"):
        postUrl = 'http://127.0.0.1:8000/fileType'
        stringifyData = json.dumps(data)
        data = {'file_data': stringifyData}
        response = requests.post(postUrl, json=data)
        #print(response.text)
        #print(response.json())
        json_response = json.loads(response.text)

        df=pd.json_normalize(json.loads(json_response))

    #print(type(json_response))
        # df = pd.DataFrame(list(reader(json_response )))

        # print(response.json(), "response from api")
        # y = response.json()
        # print(type(y))
        # df = pd.DataFrame(data=y)
        # x = pd.DataFrame.from_dict([y])
        st.dataframe(df)

        #print(type(convertedDict))
        #st.success(convertedDict)
        #st.success(json_response)
        #st.dataframe(df)
        return









def Indiviual_entry():

    st.markdown("<h1 style='text-align: center; color: white;'>Loan Prediction</h1>", unsafe_allow_html=True)
    product_list=[]
    product_list.append(st.text_input("Loan_ID"))
    product_list.append(st.selectbox("Gender",["Male","Female"]))
    product_list.append(st.selectbox("Married", ["Yes", "No"]))
    product_list.append(st.selectbox("Dependents", ["0", "1","2"]))
    product_list.append(st.selectbox("Education",["Graduate","Non-Graduate"]))
    product_list.append(st.selectbox("Self_Employed",["Yes","No"]))
    product_list.append(st.text_input("Applicant Income"))
    product_list.append(st.text_input("CoApplicant Income"))
    product_list.append(st.text_input("Loan Amount"))
    product_list.append(st.text_input("Loan Amount Term"))
    product_list.append(st.selectbox("Credit_History", ["1", "0"]))
    product_list.append(st.selectbox("Property_Area",["Urban","Semi-Urban","Rural"]))
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
        sub = True
        for val in data.values():
            print(val,len(val))
            if len(val) == 0:
                sub = False
                break
        if sub == True:

            postUrl = "http://127.0.0.1:8000/individualEntry"
            response = requests.post(postUrl, json=data)

            prediction = response.text

            print(prediction)
            print(prediction[6])

            if prediction[6] == "Y":
                st.success("He will return the loan")
            else:
                st.error("Sorry!! Customer will not return the loan")
        else:
            st.write ("form is not properly filled")

def previous_record():
    st.image("categories-of-a-loan-2048x1280 (1).jpg", width=800)
    loan_id = st.text_input("Loan ID")


    if st.button("Predict") and loan_id != "":
        postUrl = f"http://127.0.0.1:8000/retrieve_prediction/{loan_id}"
        response = requests.get(postUrl)
        print(response.json(), "response from api")
        y = response.json()
        x = pd.DataFrame.from_dict([y])
        st.dataframe(x)




if __name__=="__main__":
    Select_type_entry=st.sidebar.selectbox("Select the type of input",["File Type","Indiviual Entry", "previous record"])
    if(Select_type_entry=="File Type"):
        FileTypeEntry()
    elif  (Select_type_entry=="Indiviual Entry"):
         Indiviual_entry()
    else:
        previous_record()
