import Eskom, streamlit, pandas

streamlit.title('Find out the loadshedding schedule for a specific area in South Africa')

location = streamlit.text_input('Please specify the area by name that you would like to receive information about')

eskom = Eskom()

schedule = eskom.get_schedule(province=location[0].province, suburb=location[0], stage=Stage.STAGE_2)

streamlit.dataframe(schedule)



