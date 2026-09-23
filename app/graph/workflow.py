from pathlib import Path

from langgraph.graph import END, START, StateGraph

from app.documents.loader import DocumentLoader
from app.extraction.extractor import QuotationExtractor
from app.graph.state import AgentState
from app.validation.confidence import ConfidenceScorer
from app.validation.validator import QuotationValidator


def load_document(state: AgentState) -> AgentState:
    """Load and normalize the input document."""

    file_path = Path(state["file_path"])

    loader = DocumentLoader()
    document = loader.load(file_path)

    state["document"] = document
    state["warnings"] = document.extraction_warnings

    return state


def extract_quotation(state: AgentState) -> AgentState:
    """Extract structured quotation information."""

    extractor = QuotationExtractor()

    quotation = extractor.extract(
        state["document"]
    )

    state["quotation"] = quotation

    return state


def validate_quotation(state: AgentState) -> AgentState:
    """Run deterministic validation checks."""

    validator = QuotationValidator()

    quotation = validator.validate(
        state["quotation"]
    )

    state["quotation"] = quotation

    return state


def score_confidence(state: AgentState) -> AgentState:
    """Calculate confidence scores for the extracted data."""

    scorer = ConfidenceScorer()

    quotation = scorer.score(
        state["quotation"]
    )

    state["quotation"] = quotation

    return state


def build_workflow():
    """Build the complete document intelligence workflow."""

    workflow = StateGraph(AgentState)

    workflow.add_node(
        "load_document",
        load_document,
    )

    workflow.add_node(
        "extract_quotation",
        extract_quotation,
    )

    workflow.add_node(
        "validate_quotation",
        validate_quotation,
    )

    workflow.add_node(
        "score_confidence",
        score_confidence,
    )

    workflow.add_edge(
        START,
        "load_document",
    )

    workflow.add_edge(
        "load_document",
        "extract_quotation",
    )

    workflow.add_edge(
        "extract_quotation",
        "validate_quotation",
    )

    workflow.add_edge(
        "validate_quotation",
        "score_confidence",
    )

    workflow.add_edge(
        "score_confidence",
        END,
    )

    return workflow.compile()