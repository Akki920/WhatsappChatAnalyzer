import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessing, analyzer



def page_content():
    st.title("Welcome To Whatsapp chat Analyzer")
    chat = st.file_uploader("Upload your chat file: ")
    if chat is not None:
        bytes_data = chat.getvalue()
        data = bytes_data.decode('utf-8')
        df = preprocessing.preprocess(data)

        st.subheader("select user (For overall analysis select 'overall')")
        user_list = preprocessing.fetchUsers(df)
        selected_user = st.selectbox("Select user", user_list)

        
    pressed = st.button("Show Analysis")

    if pressed and chat is not None:
        # fetching stats

        st.title("Top Statistics")
        
        num_messages, tot_words, num_media_msg, no_links = analyzer.fetch_stats(selected_user, df)
        
        tot_mes, tot_w, no_media_msg, num_links = st.columns(4)

        with tot_mes:
            st.header("Total Messages")
            st.title(num_messages)
        
        with tot_w:
            st.header("Total Words")
            st.title(tot_words)
        with no_media_msg:
            st.header("Total number of media shared")
            st.title(num_media_msg)
        with num_links:
            st.header("Number of Links shared")
            st.title(no_links)


        #Time based analysis
        #monthly
        st.title("Monthly Timeline")
        timeline = analyzer.timeline_analysis(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        #daily
        st.title("daily Timeline")
        dailyTimeLine = analyzer.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(dailyTimeLine['datemap'], dailyTimeLine['message'])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        #activity map

        st.title("Activity Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = analyzer.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = analyzer.month_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = 'orange')
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        #Heatmap

        st.title("HeatMap")
        heatMap = analyzer.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(heatMap)
        st.pyplot(fig)


        # Fetching frequencies of users in group (ONLY FOR GROUPS)
        if selected_user == "Overall":
            st.title("Most Engaging Users")
            x, percent_count  = analyzer.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values, color = 'red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(percent_count)
                st.write("Percent share for group notification is eliminated")
        

        #Forming WordCloud
        st.title("Word Cloud")
        wc_image = analyzer.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wc_image)
        st.pyplot(fig)

        #showing most used words in chat

        st.title("Most common words used (Top 20)")
        commonWords = analyzer.word_counter(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(commonWords[0], commonWords[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji Analysis

        st.title("Emoji Analysis")
        emojis = analyzer.findEmoji(selected_user,df)
        if emojis.shape[0] == 0:
            st.title("No emoji used")

        else:
            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(emojis)
            with col2:
                fig,ax = plt.subplots()
                ax.pie(emojis[1].head(),labels=emojis[0].head(),autopct="%0.2f")
                st.pyplot(fig)

    if pressed and chat is None:
        st.write("Please upload chat first")    

         
