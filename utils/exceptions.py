class Requirements_pdfProcessingError(Exception):
    """Base exception for requirements_pdf processing errors"""

    pass


class ExtractionError(Requirements_pdfProcessingError):
    """Raised when requirements_pdf extraction fails"""

    pass


class AnalysisError(Requirements_pdfProcessingError):
    """Raised when requirements_pdf analysis fails"""

    pass


class MatchingError(Requirements_pdfProcessingError):
    """Raised when product matching fails"""

    pass


class ScreeningError(Requirements_pdfProcessingError):
    """Raised when customer requirements screening fails"""

    pass


class RecommendationError(Requirements_pdfProcessingError):
    """Raised when generating recommendations fails"""

    pass