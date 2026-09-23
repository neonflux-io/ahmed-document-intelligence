# Architecture

The Document Intelligence Agent uses a staged pipeline:

```text
Input files
    |
    v
Document Loader
    |
    +--> JSON adapter
    +--> PDF adapter
    +--> Email adapter
    +--> Image/OCR adapter
    |
    v
NormalizedDocument
    |
    v
Structured Extraction
    |
    v
Validation
    |
    v
Confidence + Human Review
    |
    v
SQLite / CSV
```
