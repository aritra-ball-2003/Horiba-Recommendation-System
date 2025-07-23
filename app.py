# app.py

import streamlit as st
import asyncio
import os
from datetime import datetime
from pathlib import Path
from streamlit_option_menu import option_menu

from agents.Orchestrator import OrchestratorAgent
from utils.logger import setup_logger
from utils.exceptions import Requirements_pdfProcessingError

# Configure Streamlit page
st.set_page_config(
    page_title="Horiba Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

logger = setup_logger()

# Custom CSS
st.markdown(
    """
    <style>
        .stProgress .st-bo {
            background-color: #00a0dc;
        }
        .success-text { color: #00c853; }
        .warning-text { color: #ffd700; }
        .error-text { color: #ff5252; }
        .st-emotion-cache-1v0mbdj.e115fcil1 {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

async def process_requirements_pdf(file_path: str) -> dict:
    """Process requirements through the AI Product process pipeline"""
    try:
        orchestrator = OrchestratorAgent()
        requirements_pdf_data = {
            "file_path": file_path,
            "submission_timestamp": datetime.now().isoformat(),
        }
        return await orchestrator.process_application(requirements_pdf_data)
    except Exception as e:
        logger.error(f"Error processing requirements_pdf: {str(e)}")
        raise Requirements_pdfProcessingError(str(e))

def save_uploaded_file(uploaded_file) -> str:
    """Save uploaded file and return the file path"""
    try:
        save_dir = Path("uploads")
        save_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = save_dir / f"requirements_{timestamp}_{uploaded_file.name}"

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return str(file_path)
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        raise

def main():
    # Sidebar navigation
    with st.sidebar:
        st.image("https://img.icons8.com/resume", width=50)
        st.title("AI Recruiter Agency")
        selected = option_menu(
            menu_title="Navigation",
            options=["Upload Requirements_pdf", "About"],
            icons=["cloud-upload", "info-circle"],
            menu_icon="cast",
            default_index=0,
        )

    if selected == "Upload Requirements_pdf":
        st.header("📄 Requirement PDF Analysis")
        st.write("Upload a requirements PDF to get AI-powered recommendation and product matches.")

        uploaded_file = st.file_uploader(
            "Choose a PDF requirements file",
            type=["pdf"],
            help="Upload a PDF requirement file to analyze",
        )

        if uploaded_file:
            try:
                with st.spinner("Saving uploaded file..."):
                    file_path = save_uploaded_file(uploaded_file)

                st.info("Requirements PDF uploaded successfully! Processing...")

                progress_bar = st.progress(0)
                status_text = st.empty()

                try:
                    status_text.text("Analyzing requirements...")
                    progress_bar.progress(25)

                    result = asyncio.run(process_requirements_pdf(file_path))

                    if result["status"] == "completed":
                        progress_bar.progress(100)
                        status_text.text("Analysis complete!")

                        tab1, tab2, tab3, tab4 = st.tabs(
                            ["📊 Analysis", "💼 Product Matches", "🎯 Screening", "💡 Recommendation"]
                        )

                        with tab1:
                            st.subheader("Use Case Analysis")
                            st.write(result.get("analysis_result", {}).get("screening_report", {}))
                            st.metric(
                                "Confidence Score",
                                f"{result.get('analysis_result', {}).get('Analysis_match_score', 0)}%"
                            )

                        with tab2:
                            st.subheader("Matched Products")
                            matched = result.get("product_matches", {}).get("matched_products", [])
                            if not matched:
                                st.warning("No suitable products found.")
                            seen = set()
                            for product in matched:
                                if product["title"] in seen:
                                    continue
                                seen.add(product["title"])
                                with st.container():
                                    col1, col2, col3 = st.columns([2, 1, 1])
                                    col1.write(f"**{product['title']}**")
                                    col2.write(f"Match: {product.get('match_score', 'N/A')}")
                                    col3.write(f"📍 {product.get('type', 'N/A')}")
                                st.divider()

                        with tab3:
                            st.subheader("Screening Results")
                            st.metric(
                                "Screening Score",
                                f"{result.get('screening_results', {}).get('screening_match_score', 0)}%"
                            )
                            st.write(result.get("screening_results", {}).get("screening_report", ""))

                        with tab4:
                            st.subheader("Final Recommendation")
                            st.info(
                                result.get("suitable_recommendation", {}).get("suitable_recommendation", "No recommendation available."),
                                icon="💡",
                            )

                        output_dir = Path("results")
                        output_dir.mkdir(exist_ok=True)
                        output_file = output_dir / f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                        with open(output_file, "w") as f:
                            f.write(str(result))
                        st.success(f"Results saved to: {output_file}")

                    else:
                        st.error(
                            f"Process failed at stage: {result['current_stage']}\n"
                            f"Error: {result.get('error', 'Unknown error')}"
                        )

                except Exception as e:
                    st.error(f"Error processing requirements PDF: {str(e)}")
                    logger.error(f"Processing error: {str(e)}", exc_info=True)

                finally:
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        logger.error(f"Error removing temporary file: {str(e)}")

            except Exception as e:
                st.error(f"Error handling file upload: {str(e)}")
                logger.error(f"Upload error: {str(e)}", exc_info=True)

    elif selected == "About":
        st.header("About Horiba AI Support")
        st.write("""
        Welcome to Horiba AI Support, a cutting-edge product recommendation system powered by:
        - 🤖 **Ollama (LLaMA3.2)** for natural language understanding
        - 🧠 Swarm framework for AI agent coordination
        - 🖥️ Streamlit for web-based interaction

        This system extracts customer requirements, analyzes them, matches suitable products,
        screens them, and gives tailored recommendations.

        Upload a requirements PDF and let the AI handle the rest!
        """)

if __name__ == "__main__":
    main()
