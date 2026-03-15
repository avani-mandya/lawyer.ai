import streamlit as st
import google.generativeai as genai

def main():
    st.set_page_config(page_title="Legal War Room", page_icon="⚖️")
    st.title("⚖️ Courtroom Practice Simulator")

    api_key = st.secrets["GEMINI_API_KEY"]	

    # 2. THE FIX: Using 'transport=rest' and a newer model
    try:
        genai.configure(api_key=api_key, transport='rest')
        # We are using gemini-2.0-flash because older versions (1.5) are returning 404 for some
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        st.error(f"Setup Error: {e}")
        return

    case_summary = st.text_area("Enter Case Facts:", placeholder="e.g. Someone stole my bike...")

    if st.button("Start Practice"):
        if not case_summary:
            st.warning("Please enter some facts.")
        else:
            try:
                with st.spinner("AI is thinking..."):
                    # Generate response
                    prompt = f"Act as a lawyer. Give a rebuttal and 2 judge questions for this case: {case_summary}"
                    response = model.generate_content(prompt)

                st.success("✅ Success!")
                st.write(response.text)

            except Exception as e:
                # If it still says 404, we try ONE more backup model
                st.error(f"API Error: {e}")
                st.info("Try changing the model name to 'gemini-1.5-flash-latest' in the code if this failed.")

if __name__ == "__main__":
    main()
