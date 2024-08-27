import streamlit as st
import sqlite3

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('voting_system.db')
    return conn

# Page 1: Enter Registration Number
def page1():
    st.title('Voting System')
    reg_number = st.text_input('Enter your registration number:')
    if st.button('Next'):
        if reg_number:
            st.session_state.registration_number = reg_number
            st.session_state.page = 'page2'
        else:
            st.warning('Please enter a registration number.')

# Page 2: Vote for President
def page2():
    st.title('Vote for President')
    conn = get_db_connection()
    candidates = conn.execute("SELECT name FROM candidates WHERE role='president'").fetchall()
    conn.close()
    selected_candidate = st.selectbox('Select a candidate for President', [c[0] for c in candidates])
    if st.button('Next'):
        st.session_state.president = selected_candidate
        st.session_state.page = 'page3'

# Page 3: Vote for Secretary
def page3():
    st.title('Vote for Secretary')
    conn = get_db_connection()
    candidates = conn.execute("SELECT name FROM candidates WHERE role='secretary'").fetchall()
    conn.close()
    selected_candidate = st.selectbox('Select a candidate for Secretary', [c[0] for c in candidates])
    if st.button('Next'):
        st.session_state.secretary = selected_candidate
        st.session_state.page = 'page4'

# Page 4: Vote for Vice President
def page4():
    st.title('Vote for Vice President')
    conn = get_db_connection()
    candidates = conn.execute("SELECT name FROM candidates WHERE role='vice_president'").fetchall()
    conn.close()
    selected_candidate = st.selectbox('Select a candidate for Vice President', [c[0] for c in candidates])
    if st.button('Next'):
        st.session_state.vice_president = selected_candidate
        st.session_state.page = 'page5'

# Page 5: Vote for Assistant Secretary
def page5():
    st.title('Vote for Assistant Secretary')
    conn = get_db_connection()
    candidates = conn.execute("SELECT name FROM candidates WHERE role='assistant_secretary'").fetchall()
    conn.close()
    selected_candidate = st.selectbox('Select a candidate for Assistant Secretary', [c[0] for c in candidates])
    if st.button('Submit'):
        conn = get_db_connection()
        conn.execute('''
        INSERT INTO votes (registration_number, president, secretary, vice_president, assistant_secretary)
        VALUES (?, ?, ?, ?, ?)
        ''', (st.session_state.registration_number, st.session_state.president, st.session_state.secretary, st.session_state.vice_president, st.session_state.assistant_secretary))
        conn.commit()
        conn.close()
        st.success('Your vote has been submitted!')
        st.session_state.page = 'page1'

# Authorization page for vote count
def admin_page():
    st.title('Admin Login')
    username = st.text_input('Username:')
    password = st.text_input('Password:', type='password')
    if st.button('Login'):
        if username == 'admin' and password == 'password':  # Replace with real authentication
            st.session_state.admin_authenticated = True
            st.session_state.page = 'vote_count'
        else:
            st.error('Invalid username or password.')

def vote_count_page():
    st.title('Vote Count')
    conn = get_db_connection()
    results = conn.execute('''
    SELECT role, candidate, COUNT(*) AS votes
    FROM (
        SELECT 'president' AS role, president AS candidate FROM votes
        UNION ALL
        SELECT 'secretary' AS role, secretary AS candidate FROM votes
        UNION ALL
        SELECT 'vice_president' AS role, vice_president AS candidate FROM votes
        UNION ALL
        SELECT 'assistant_secretary' AS role, assistant_secretary AS candidate FROM votes
    )
    GROUP BY role, candidate
    ''').fetchall()
    conn.close()
    for row in results:
        st.write(f"{row[0]} - {row[1]}: {row[2]} votes")

# Page Routing
def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'page1'

    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False

    if st.session_state.page == 'page1':
        page1()
    elif st.session_state.page == 'page2':
        page2()
    elif st.session_state.page == 'page3':
        page3()
    elif st.session_state.page == 'page4':
        page4()
    elif st.session_state.page == 'page5':
        page5()
    elif st.session_state.page == 'admin_login':
        admin_page()
    elif st.session_state.page == 'vote_count' and st.session_state.admin_authenticated:
        vote_count_page()
    else:
        st.write('Access Denied.')

if __name__ == "__main__":
    main()
