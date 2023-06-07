
# necessary libraries and pacakges
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# import sweetviz as sv


from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

# from ydata_profiling import ProfileReport
# from ydata_profiling.st_profile_report import st_profile_report

import scipy.stats as stats
import numpy as np
from PIL import Image



# function to calculate confidence interval
def calculate_confidence_interval(data, confidence=0.95):
    data = np.array(data)
    n = len(data)
    mean = np.mean(data)
    std_err = stats.sem(data)
    margin_error = std_err * stats.t.ppf((1 + confidence) / 2, n - 1)
    lower_bound = mean - margin_error
    upper_bound = mean + margin_error
    return lower_bound, upper_bound




st.markdown(""" # StatFlow - is a new way of EDA! """)

logo_image = Image.open("StatFlowLogo.png")
st.image(logo_image, use_column_width=True)



st.set_option('deprecation.showPyplotGlobalUse', False)
data = st.file_uploader("Upload a Dataset", type=["csv", "txt"])




# main function to do all small functionality inside this app
def main(): 
    activities = ["EDA", "Plots", "Report", "Sweetviz"]
    choice = st.sidebar.radio("Select Operation", activities)

# EDA part1
    if choice == 'EDA':
        st.subheader("Exploratory Data Analysis")
        
        if data is not None:
            df = pd.read_csv(data)

            if st.checkbox("Show Head 5 data"):
                st.dataframe(df.head())

            if st.checkbox("Show Shape"):
                st.write(df.shape)

            if st.checkbox("Show Columns"):
                all_columns = df.columns.to_list()
                st.write(all_columns)

            if st.checkbox("Summary"):
                st.write(df.describe().T)

            if st.checkbox("Show Selected Columns"):
                selected_columns = st.multiselect("Select Columns", all_columns)
                new_df = df[selected_columns]
                st.dataframe(new_df)

            if st.checkbox("Calculate Confidence Interval"):
                selected_column = st.selectbox("Select a Column", all_columns)
                column_data = df[selected_column]
                lower, upper = calculate_confidence_interval(column_data)
                st.write("Confidence Interval:")
                st.write(f"Lower Bound: {lower}")
                st.write(f"Upper Bound: {upper}")


            if st.checkbox("Show Value Counts"):
                st.write(df.iloc[:, -1].value_counts())

            if st.checkbox("Correlation Plot(Matplotlib)"):
                plt.matshow(df.corr())
                st.pyplot()

            if st.checkbox("Correlation Plot(Seaborn)"):
                st.write(sns.heatmap(df.corr(), annot=True))
                st.pyplot()

            if st.checkbox("Pie Plot"):
                all_columns = df.columns.to_list()
                column_to_plot = st.selectbox("Select 1 Column", all_columns)
                pie_plot = df[column_to_plot].value_counts().plot.pie(autopct="%1.1f%%")
                st.write(pie_plot)
                st.pyplot()

#plots part2
    elif choice == 'Plots':
        st.subheader("Data Visualization")
        if data is not None:
            df = pd.read_csv(data)
            st.write("Top 5 data")
            st.dataframe(df.head())

            if st.checkbox("Show Value Counts"):
                st.write(df.iloc[:, -1].value_counts().plot(kind='bar'))
                st.pyplot()

            # Customizable Plot
            all_columns_names = df.columns.tolist()
            type_of_plot = st.radio("Select Type of Plot", ["area", "bar", "line", "hist", "box", "kde"])
            selected_columns_names = st.multiselect("Select Columns To Plot", all_columns_names)

            if st.button("Generate Plot"):
                st.success("Generating Customizable Plot of {} for {}".format(type_of_plot, selected_columns_names))

                # Plot By Streamlit
                if type_of_plot == 'area':
                    cust_data = df[selected_columns_names]
                    st.area_chart(cust_data)

                elif type_of_plot == 'bar':
                    cust_data = df[selected_columns_names]
                    st.bar_chart(cust_data)

                elif type_of_plot == 'line':
                    cust_data = df[selected_columns_names]
                    st.line_chart(cust_data)

                # Custom Plot
                elif type_of_plot:
                    cust_plot = df[selected_columns_names].plot(kind=type_of_plot)
                    st.write(cust_plot)
                    st.pyplot()

# Report part3
    elif choice == 'Report':
        # Automated EDA with Pandas Profiling section
        st.subheader("Automated EDA with Pandas Profile")
        # data_file = st.file_uploader("Upload CSV", type=["csv", "txt"])
        # Pandas Profiling Report
        if data is not None:
            @st.cache
            def load_csv():
                csv = pd.read_csv(data)
                return csv
            df = load_csv()
            pr = ProfileReport(df, explorative=True)
            st.header('**Input DataFrame**')
            st.write(df)
            st.write('---')
            st.header('**Pandas Profiling Report**')
            st_profile_report(pr)
        else:
            st.info('Awaiting for CSV file to be uploaded.')
            if st.button('Press to use Example Dataset'):
                # Example data
                @st.cache
                def load_data():
                    a = pd.DataFrame(
                        np.random.rand(100, 5),
                        columns=['a', 'b', 'c', 'd', 'e']
                    )
                    return a
                df = load_data()
                pr = ProfileReport(df, explorative=True)
                st.header('**Input DataFrame**')
                st.write(df)
                st.write('---')
                st.header('**Pandas Profiling Report**')
                st_profile_report(pr)
        

# #SweetViz part4
#     elif choice == 'Sweetviz':
#         st.subheader("Automated EDA with Sweetviz")
#         # Automated EDA with Sweetviz section
#         if data is not None:
#             df = pd.read_csv(data)
#             st.dataframe(df.head())
#             if st.button("Generate Sweetviz Report"):
#                 report = sv.analyze(df)
#                 report.show_html()
#                 st_display_sweetviz("SWEETVIZ_REPORT.html")

if __name__ == '__main__':
    main()


