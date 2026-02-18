from typing import Dict, Optional, List, Union
from collections import Counter
from interfaces.IAnalysisMetrics import IAnalysisMetrics

class AnalysisMetrics(IAnalysisMetrics):
    def __init__(self):
        self.metrics = {}
    
    def calculate_metrics(self, data: Union[List[Dict], None] = None) -> Dict:
        """
        Calculates aggregate metrics from a list of narrative analysis results.
        Expected data schema per item:
        {
            "emotional_intensity": float,
            "stance": str,
            "emotional_tone": str,
            "key_entities": List[str]
        }
        """
        if data is None:
            return {}

        total_items = len(data)
        emotional_intensity_sum = 0.0
        stances = []
        tones = []
        all_entities = []

        for item in data:
            # Aggregate Emotional Intensity
            try:
                intensity = float(item.get("emotional_intensity", 0))
                emotional_intensity_sum += intensity
            except (ValueError, TypeError):
                pass
            
            # Aggregate Categories
            stances.append(item.get("stance", "unknown"))
            tones.append(item.get("emotional_tone", "unknown"))
            
            # Aggregate Entities
            entities = item.get("key_entities", [])
            if isinstance(entities, list):
                all_entities.extend(entities)

        # Compute Statistics
        avg_intensity = emotional_intensity_sum / total_items if total_items > 0 else 0
        
        self.metrics = {
            "total_analyzed": total_items,
            "average_sentiment_intensity": round(avg_intensity, 2),
            "stance_distribution": dict(Counter(stances)),
            "tone_distribution": dict(Counter(tones)),
            "top_entities": dict(Counter(all_entities).most_common(10))
        }
        
        return self.metrics