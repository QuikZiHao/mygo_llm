class Detection:
    def __init__(self, label, confidence, bbox):
        self.label = label
        self.confidence = confidence
        self.bbox = bbox
        self.have_open_mouth = False

    def score(self) -> float:
        return self.confidence * 2 if self.have_open_mouth else self.confidence
     
    def to_dict(self):
        """Convert the Detection object to a dictionary."""
        return {
            "label": self.label,
            "confidence": self.confidence,
            "bbox": self.bbox,
            "have_open_mouth": self.have_open_mouth
        }

    def __repr__(self):
        return f"Detection(label={self.label}, confidence={self.confidence}, bbox={self.bbox}, have_open_mouth={self.have_open_mouth})"