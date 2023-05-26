import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

st.sidebar.title("Whatsapp chat analyzer")


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)

    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"overall")

    selected_user=st.sidebar.selectbox("show analysis wrt",user_list)

    if st.sidebar.button("Show analysis"):
        num_messages,words,num_media_messages,num_links=helper.fetch_stats(selected_user,df)
        st.title("Top statistics")
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header('Total messages')
            st.title(num_messages)
        with col2:
            st.header('Total words')
            st.title(words)
        with col3:
            st.header('Media shared')
            st.title(num_media_messages)
        with col4:
            st.header('Links shared')
            st.title(num_links)

        #monthly timeline
        st.title("Monthly timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("Daily timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title("Activity map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month=helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly activity map")
        user_heat_map=helper.activity_heat_map(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heat_map)
        st.pyplot(fig)


        #finding the busiest users in the group(group level
        if selected_user=='overall':
            st.title('Most busy users')
            x,new_df=helper.most_busy_users(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #wordcloud
        st.title("Wordcloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_common_df = helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most common words")
        st.pyplot(fig)

        #emoji analysis
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title("Emoji analysis")
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)



