import secrets
import string
import streamlit as st

def generiere_passwort(laenge=16):
    # Kombiniert Groß-/Kleinbuchstaben, Zahlen und Sonderzeichen
    alle_zeichen = string.ascii_letters + string.digits + string.punctuation
    
    # Erstellt ein kryptografisch sicheres Passwort
    passwort = ''.join(secrets.choice(alle_zeichen) for _ in range(laenge))
    return passwort

def run_password_generator():
    st.title("Password Generator")
    st.write("Generate a secure password.")

    # Benutzerdefinierte Länge des Passworts
    laenge = st.slider("Password Length", min_value=8, max_value=64, value=16)

    if st.button("Generate Password"):
        passwort = generiere_passwort(laenge)
        st.success(f"Generated Password: {passwort}")