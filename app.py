# Streamlit Web Application
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

# Initialize logger
logger = setup_logger()

# Custom CSS
st.markdown(
    """
    <style>
        .stProgress .st-bo {
            background-color: #00a0dc;
        }
        .success-text {
            color: #00c853;
        }
        .warning-text {
            color: #ffd700;
        }
        .error-text {
            color: #ff5252;
        }
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
        raise


def save_uploaded_file(uploaded_file) -> str:
    """Save uploaded file and return the file path"""
    try:
        # Create uploads directory if it doesn't exist
        save_dir = Path("uploads")
        save_dir.mkdir(exist_ok=True)

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = save_dir / f"requirements_{timestamp}_{uploaded_file.name}"

        # Save the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return str(file_path)
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        raise


def main():
    # Sidebar navigation
    with st.sidebar:
        st.image(
            "https://img.icons8.com/resume",
            width=50,
        )
        st.title("AI Recruiter Agency")
        selected = option_menu(
            menu_title="Navigation",
            options=["Upload Requirements_pdf", "About"],
            icons=["cloud-upload", "info-circle"],
            menu_icon="cast",
            default_index=0,
        )

    if selected == "Upload Requirement pdf":
        st.header("📄 Requirement pdf Analysis")
        st.write("Upload a requiremnts to get AI-powered recommendation and product matches.")

        uploaded_file = st.file_uploader(
            "Choose a PDF requiremnts file",
            type=["pdf"],
            help="Upload a PDF requirement pdf to analyze",
        )

        if uploaded_file:
            try:
                with st.spinner("Saving uploaded file..."):
                    file_path = save_uploaded_file(uploaded_file)

                st.info("Requirements pdf uploaded successfully! Processing...")

                # Create placeholder for progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Process requirements
                try:
                    status_text.text("Analyzing requirements...")
                    progress_bar.progress(25)

                    # Run analysis asynchronously
                    result = asyncio.run(process_requirements_pdf(file_path))

                    if result["status"] == "completed":
                        progress_bar.progress(100)
                        status_text.text("Analysis complete!")

                        # Display results in tabs
                        tab1, tab2, tab3, tab4 = st.tabs(
                            [
                                "📊 Analysis",
                                "💼 Product Matches",
                                "🎯 Screening",
                                "💡 Recommendation",
                            ]
                        )

                        with tab1:
                            st.subheader("Usecase Analysis")
                            st.write(result["analysis_results"]["Usecase_analysis"])
                            st.metric(
                                "Confidence Score",
                                f"{result['analysis_results']['confidence_score']:.0%}",
                            )

                        with tab2:
                            st.subheader("Matched Products")
                            if not result["Product_matches"]["matched_products"]:
                                st.warning("No suitable positions found.")

                            seen_titles = (
                                set()
                            )  # Track seen job titles to avoid duplicates

                            for products in result["Product_matches"]["matched_products"]:
                                if products["title"] in seen_titles:
                                    continue
                                seen_titles.add(products["title"])

                                with st.container():
                                    col1, col2, col3 = st.columns([2, 1, 1])
                                    with col1:
                                        st.write(f"**{products['title']}**")
                                    with col2:
                                        st.write(
                                            f"Match: {products.get('match_score', 'N/A')}"
                                        )
                                    with col3:
                                        st.write(f"📍 {products.get('Department', 'N/A')}")
                                st.divider()

                        with tab3:
                            st.subheader("Screening Results")
                            st.metric(
                                "Screening Score",
                                f"{result['screening_results']['screening_score']}%",
                            )
                            st.write(result["screening_results"]["screening_report"])

                        with tab4:
                            st.subheader("Suitable Recommendation")
                            st.info(
                                result["Suitable_recommendation"]["Suitable_recommendation"],
                                icon="💡",
                            )

                        # Save results
                        output_dir = Path("results")
                        output_dir.mkdir(exist_ok=True)
                        output_file = (
                            output_dir
                            / f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                        )

                        with open(output_file, "w") as f:
                            f.write(str(result))

                        st.success(f"Results saved to: {output_file}")

                    else:
                        st.error(
                            f"Process failed at stage: {result['current_stage']}\n"
                            f"Error: {result.get('error', 'Unknown error')}"
                        )

                except Exception as e:
                    st.error(f"Error processing requirements pdf: {str(e)}")
                    logger.error(f"Processing error: {str(e)}", exc_info=True)

                finally:
                    # Cleanup uploaded file
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        logger.error(f"Error removing temporary file: {str(e)}")

            except Exception as e:
                st.error(f"Error handling file upload: {str(e)}")
                logger.error(f"Upload error: {str(e)}", exc_info=True)

    elif selected == "About":
        st.header("About Horiba Ai Support")
        st.write(
            """
        Welcome to Horiba Ai Support, a cutting-edge recruitment analysis system powered by:
        
        - **Ollama (llama3.2)**: Advanced language model for natural language processing
        - **Swarm Framework**: Coordinated AI agents for specialized tasks
        - **Streamlit**: Modern web interface for easy interaction
        
        Our system uses specialized AI agents to:
        1. 📄 Extract information from  requirements pdf
        2. 🔍 Analyze the customer requirements
        3. 🎯 Match with suitable positions
        4. 👥 Screen candidates
        5. 💡 Provide detailed recommendations
        
        Upload a requirements pdf to experience AI-powered Product recomendation!
        """
        )


if __name__ == "__main__":
    main()


# == Command Line Interface (CLI) ==
# == to run use: python3 app.py resumes/sample_resume.pdf ==
# import asyncio
# import os
# import sys
# from datetime import datetime
# from rich.console import Console
# from rich.panel import Panel
# from rich.progress import Progress, SpinnerColumn, TextColumn
# from rich.table import Table
# from agents.orchestrator import OrchestratorAgent
# from utils.logger import setup_logger
# from utils.exceptions import ResumeProcessingError

# # Initialize Rich console for beautiful CLI output
# console = Console()
# logger = setup_logger()


# async def process_resume(file_path: str) -> None:
#     """Process a resume through the AI recruitment pipeline"""
#     try:
#         # Validate input file
#         if not os.path.exists(file_path):
#             raise FileNotFoundError(f"Resume not found at {file_path}")

#         if not file_path.lower().endswith(".pdf"):
#             raise ValueError("Please provide a PDF resume file")

#         logger.info(f"Starting recruitment process for: {os.path.basename(file_path)}")

#         # Display welcome banner
#         console.print(
#             Panel.fit(
#                 "[bold blue]AI Recruitment Agency[/bold blue]\n"
#                 "[dim]Powered by Ollama (llama2) and Swarm Framework[/dim]",
#                 border_style="blue",
#             )
#         )

#         # Initialize orchestrator
#         orchestrator = OrchestratorAgent()

#         # Prepare resume data
#         resume_data = {
#             "file_path": file_path,
#             "submission_timestamp": datetime.now().isoformat(),
#         }

#         # Process with progress indication
#         with Progress(
#             SpinnerColumn(),
#             TextColumn("[progress.description]{task.description}"),
#             console=console,
#         ) as progress:
#             task = progress.add_task("[cyan]Processing resume...", total=None)
#             result = await orchestrator.process_application(resume_data)
#             progress.update(task, completed=True)

#         if result["status"] == "completed":
#             logger.info("Resume processing completed successfully")

#             # Create results table
#             table = Table(
#                 title="Analysis Summary", show_header=True, header_style="bold magenta"
#             )
#             table.add_column("Category", style="cyan")
#             table.add_column("Details", style="white")

#             # Add analysis results
#             table.add_row(
#                 "Skills Analysis", str(result["analysis_results"]["skills_analysis"])
#             )
#             table.add_row(
#                 "Confidence Score",
#                 f"{result['analysis_results']['confidence_score']:.2%}",
#             )

#             console.print("\n", table)

#             # Display job matches
#             matches_table = Table(
#                 title="Job Matches", show_header=True, header_style="bold green"
#             )
#             matches_table.add_column("Position", style="cyan")
#             matches_table.add_column("Match Score", style="white")
#             matches_table.add_column("Location", style="white")

#             for job in result["job_matches"]["matched_jobs"]:
#                 matches_table.add_row(
#                     job["title"],
#                     f"{job.get('match_score', 'N/A')}",
#                     job.get("location", "N/A"),
#                 )

#             console.print("\n", matches_table)

#             # Display screening results
#             console.print(
#                 Panel(
#                     f"[bold]Screening Score:[/bold] {result['screening_results']['screening_score']}%\n\n"
#                     f"{result['screening_results']['screening_report']}",
#                     title="Screening Results",
#                     border_style="green",
#                 )
#             )

#             # Display final recommendation
#             console.print(
#                 Panel(
#                     result["final_recommendation"]["final_recommendation"],
#                     title="Final Recommendation",
#                     border_style="blue",
#                 )
#             )

#             # Save results to file
#             output_dir = "results"
#             if not os.path.exists(output_dir):
#                 os.makedirs(output_dir)

#             output_file = os.path.join(
#                 output_dir, f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
#             )

#             with open(output_file, "w") as f:
#                 f.write("AI Recruitment Analysis Results\n")
#                 f.write("=" * 50 + "\n\n")
#                 f.write(f"Resume: {os.path.basename(file_path)}\n")
#                 f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
#                 f.write("Analysis Summary\n")
#                 f.write("-" * 20 + "\n")
#                 f.write(
#                     f"Skills Analysis: {result['analysis_results']['skills_analysis']}\n"
#                 )
#                 f.write(
#                     f"Confidence Score: {result['analysis_results']['confidence_score']:.2%}\n\n"
#                 )
#                 f.write("Job Matches\n")
#                 f.write("-" * 20 + "\n")
#                 for job in result["job_matches"]["matched_jobs"]:
#                     f.write(f"\nPosition: {job['title']}\n")
#                     f.write(f"Match Score: {job.get('match_score', 'N/A')}\n")
#                     f.write(f"Location: {job.get('location', 'N/A')}\n")
#                 f.write("\nScreening Results\n")
#                 f.write("-" * 20 + "\n")
#                 f.write(f"Score: {result['screening_results']['screening_score']}%\n")
#                 f.write(
#                     f"Report: {result['screening_results']['screening_report']}\n\n"
#                 )
#                 f.write("Final Recommendation\n")
#                 f.write("-" * 20 + "\n")
#                 f.write(str(result["final_recommendation"]["final_recommendation"]))

#             console.print(f"\n[green]✓[/green] Results saved to: {output_file}")

#         else:
#             error_msg = f"Process failed at stage: {result['current_stage']}"
#             if "error" in result:
#                 error_msg += f"\nError: {result['error']}"
#             logger.error(error_msg)
#             console.print(f"\n[red]✗[/red] {error_msg}")

#     except FileNotFoundError as e:
#         logger.error(f"File error: {str(e)}")
#         console.print(f"[red]Error:[/red] {str(e)}")
#     except ValueError as e:
#         logger.error(f"Validation error: {str(e)}")
#         console.print(f"[red]Error:[/red] {str(e)}")
#     except ResumeProcessingError as e:
#         logger.error(f"Processing error: {str(e)}")
#         console.print(f"[red]Error:[/red] {str(e)}")
#     except Exception as e:
#         logger.error(f"Unexpected error: {str(e)}", exc_info=True)
#         console.print(f"[red]✗ An unexpected error occurred:[/red] {str(e)}")


# def main():
#     """Main entry point for the AI recruitment system"""
#     import argparse

#     parser = argparse.ArgumentParser(
#         description="AI Recruitment Agency - Resume Processing System",
#         formatter_class=argparse.RawDescriptionHelpFormatter,
#         epilog="""
# Examples:
#     python main.py path/to/resume.pdf
#     python main.py --help
#         """,
#     )

#     parser.add_argument("resume_path", help="Path to the PDF resume file to process")

#     parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

#     args = parser.parse_args()

#     if args.verbose:
#         console.print("[yellow]Running in verbose mode[/yellow]")

#     try:
#         asyncio.run(process_resume(args.resume_path))
#     except KeyboardInterrupt:
#         console.print("\n[yellow]Process interrupted by user[/yellow]")
#         sys.exit(1)


# if __name__ == "__main__":
#     main()