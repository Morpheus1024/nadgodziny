import time
import datetime
import streamlit as st
import kalkulator_nadgodzin as kn
import db_connector as connector


db_url = st.secrets["SUPABASE_URL"]
db_key = st.secrets["SUPABASE_KEY"]



def reload_interface():
            reload_text = st.text('Reloading in 3 seconds...')
            time.sleep(1)
            reload_text.text('Reloading in 2 seconds...')
            time.sleep(1)
            reload_text.text('Reloading in 1 second...')
            time.sleep(1)
            reload_text.text('Reloading...')
            time.sleep(1)
            reload_text.empty()
            st.rerun()  
            

def streamlit_interface(db_client):
    
    if db_client is None:
        st.error("Nie można połączyć się z bazą danych.")
        return
    
    
    data = kn.load_data_from_json()
    
    st.title('Kalkulator nadgodzin')
    
    st.write(f'### Odczytano: godziny: {data["godziny"]}, minuty: {data["minuty"]}')
    st.write('---')
    
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
    
        st.write('### Godzina rozpoczecia')
        czas_rospoczecia = st.time_input(
            value=datetime.time(7,0), 
            label = 'Godzina rozpoczęcia', 
            key='czas_rozpoczecia_inpust', 
            step = 60, 
            label_visibility='collapsed'
            )
    
        st.write('### Godzina zakonczenia')
        czas_zakonczenia = st.time_input(
            value = "now", 
            label = 'Godzina zakończenia', 
            key='czas_zakonczenia_input', 
            step = 60, 
            label_visibility='collapsed'
            )
    
        czas = kn.oblicz_nadgodziny_datetime(czas_rospoczecia, czas_zakonczenia)
        nadgodziny_teskt = f'## Nadgodziny: {czas}' if czas.second>0 else f'## Nadgodziny: {datetime.timedelta(seconds=0)}' 
        st.write(nadgodziny_teskt)
        
        if st.button('Dodaj czas',use_container_width=True):
            hours = czas.seconds // 3600
            minutes = (czas.seconds % 3600) // 60
            czas = 60*hours + minutes
            kn.dodaj_czas_do_jsona(czas = czas)
            st.success('Dodano czas')
            reload_interface()
        

    with col2:
        
        st.write('### Odejmij nadgodziny')
        
        czas_do_odjecia = st.time_input(
            label = 'Czas do odjęcia', 
            key='czas_do_odjecia_input', 
            step = 60, 
            value = datetime.time(1,0)
            )
        if st.button('Odejmij', type='primary', use_container_width=True):
            #st.write(czas_do_odjecia.hour)
            # print(czas_do_odjecia)
            # print(f"{czas_do_odjecia.hour}:{czas_do_odjecia.minute}") 
            czas = f'{czas_do_odjecia.hour}:{czas_do_odjecia.minute}'
            kn.odejmij_czas_z_jsona(czas = czas)
            st.success('Odejmiono czas')
            reload_interface()
        
        # st.write('---')
        st.write('### Dodaj nadgodzin')
        czas_do_dodania = st.time_input(
            label = 'Czas do dodania',
            key='czas_do_dodania_input',
            step = 60,
            value = datetime.time(1,0)
            )
        if st.button('Dodaj', type='primary', use_container_width=True):
            czas = f'{czas_do_dodania.hour}:{czas_do_dodania.minute}'
            
            hours = czas.seconds // 3600
            minutes = (czas.seconds % 3600) // 60
            czas = 60*hours + minutes
            kn.dodaj_czas_do_jsona(czas = czas)
            st.success('Dodano czas')
            reload_interface()

    st.write('---')
    

    
def main():
    
    supabase_client = connector.connect_to_db(db_url=db_url, db_key=db_key)
    streamlit_interface(supabase_client)
    
if __name__ == '__main__':
    main()