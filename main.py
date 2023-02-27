import streamlit as st


def dict_to_list(d: dict):
    l = []
    for key, value in d.items():
        l.extend([key, value])
    return l


def list_to_dict(l: list):
    d = {}
    for k, v in zip(l[::2], l[1::2]):
        d[k] = v
    return d


def dict_to_str(d: dict, newlines=True):
    d = {k: v for k, v in d.items() if k not in ["\\", "_"]}
    if not newlines:
        return " ".join(dict_to_list(d))
    return "\n".join(" ".join([k, v]) for k, v in d.items())


def str_to_dict(s: str):
    return list_to_dict(s.split())


HEB_LETTERS = "אבגדהוזחטיכלמנסעפצקרשת"
ENG_LETTERS = "abcdefghijklmnopqrstuvwxyz"
KEYS = {
    "Key": {str(i): str(i) for i in range(1, 1 + 50)},
    "English 1-26": {str(i): c for i, c in enumerate(ENG_LETTERS, 1)},
    "Hebrew 1-22": {str(i): c for i, c in enumerate(HEB_LETTERS, 1)},
}
DEFAULT_KEY = "English 1-26"


def new_key_button_callback():
    st.session_state["secret_key"] = dict_to_str(KEYS[method])


# inputs
st.set_page_config("Translator")
st.title("Translator")
col1up, col2up = st.columns(2)
with col1up:
    cipher_text = st.text_area(
        "cipher text",
        value="8 5 12 12 15 _ 23 15 18 12 4",
        height=200,
    )
col1, col2 = st.columns(2)
with col2:
    method = st.radio("Method", index=0, options=KEYS.keys())
    squeeze = st.checkbox("squeeze spaces", value=True)
    newline = st.checkbox("backslash is new line", value=True)
    space = st.checkbox("underscore is space", value=True)
    passthrough = st.checkbox("passthrough instead of ?", value=True)
with col1:
    secret_key = st.text_area(
        "secret key", value=dict_to_str(KEYS[DEFAULT_KEY]), height=200, key="secret_key"
    )
    if method == "Key":
        key = str_to_dict(secret_key)
    else:
        key = KEYS[method]
    if newline:
        key["\\"] = "\n"
    if space:
        key["_"] = " "
    st.button("New key", on_click=new_key_button_callback)
with col2up:
    output_sep = "" if squeeze else " "
    plain_text = output_sep.join(
        [key.get(c, c if passthrough else "?") for c in cipher_text.split()]
    )
    st.caption("**plain text**")
    st.text(plain_text)
