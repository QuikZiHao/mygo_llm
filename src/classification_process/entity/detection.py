class Detection:
    def __init__(self, label, confidence, bbox):
        self.label = label
        self.confidence = confidence
        self.bbox = bbox

    def to_dict(self):
        """Convert the Detection object to a dictionary."""
        return {
            "label": self.label,
            "confidence": self.confidence,
            "bbox": self.bbox
        }

    def __repr__(self):
        return f"Detection(label={self.label}, confidence={self.confidence}, bbox={self.bbox})"