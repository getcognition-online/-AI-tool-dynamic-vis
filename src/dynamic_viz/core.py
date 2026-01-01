"""
Dynamic Visualization Engine Core.

Allows AI/LLM to programmatically request custom visualizations
to explain insights and findings.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from .config import BRAND, BRAND_PALETTE

logger = logging.getLogger(__name__)

# Try Altair first, fall back to raw Vega-Lite
try:
    import altair as alt
    ALTAIR_AVAILABLE = True
    logger.info("[DynamicViz] Altair available - using full chart generation")
except ImportError:
    ALTAIR_AVAILABLE = False
    logger.info("[DynamicViz] Altair not available - using Vega-Lite fallback")


# =============================================================================
# VISUALIZATION REQUEST TYPES
# =============================================================================

class VizRequest:
    """
    A structured request for a visualization from the AI.
    
    The AI describes what it wants to visualize, and the engine
    generates the appropriate chart.
    """
    
    CHART_TYPES = [
        'bar',           # Comparison of categories
        'line',          # Trends over time
        'scatter',       # Relationships between variables
        'pie',           # Proportions
        'heatmap',       # Matrix correlations
        'gauge',         # Single metric
        'funnel',        # Process stages
        'radial',        # Multi-dimensional comparison
        'timeline',      # Events over time
    ]
    
    def __init__(
        self,
        title: str,
        chart_type: str,
        data: List[Dict],
        x_field: str = None,
        y_field: str = None,
        color_field: str = None,
        description: str = "",
        insight: str = "",
    ):
        """
        Create a visualization request.
        
        Args:
            title: Chart title
            chart_type: One of CHART_TYPES
            data: List of data points [{field: value, ...}]
            x_field: Field for x-axis
            y_field: Field for y-axis  
            color_field: Field for color encoding
            description: What this chart shows
            insight: The key takeaway/insight
        """
        self.title = title
        self.chart_type = chart_type if chart_type in self.CHART_TYPES else 'bar'
        self.data = data
        self.x_field = x_field
        self.y_field = y_field
        self.color_field = color_field
        self.description = description
        self.insight = insight
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'chart_type': self.chart_type,
            'data': self.data,
            'x_field': self.x_field,
            'y_field': self.y_field,
            'color_field': self.color_field,
            'description': self.description,
            'insight': self.insight,
            'created_at': self.created_at,
        }


# =============================================================================
# DYNAMIC VIZ ENGINE
# =============================================================================

class DynamicVizEngine:
    """
    Generates visualizations from AI requests.
    
    The AI can call this to create custom charts that explain
    its insights to the reader.
    """
    
    def __init__(self):
        self.generated_charts: List[Dict] = []
    
    def generate(self, request: VizRequest) -> Dict:
        """
        Generate a Vega-Lite spec from a visualization request.
        
        Args:
            request: VizRequest with chart details
            
        Returns:
            Vega-Lite JSON spec
        """
        logger.info(f"[DynamicViz] Generating {request.chart_type}: {request.title}")
        
        generators = {
            'bar': self._gen_bar,
            'line': self._gen_line,
            'scatter': self._gen_scatter,
            'pie': self._gen_pie,
            'gauge': self._gen_gauge,
            'funnel': self._gen_funnel,
            'heatmap': self._gen_heatmap,
            'radial': self._gen_radial,
            'timeline': self._gen_timeline,
        }
        
        generator = generators.get(request.chart_type, self._gen_bar)
        spec = generator(request)
        
        # Add to history
        self.generated_charts.append({
            'request': request.to_dict(),
            'spec': spec,
        })
        
        return spec
    
    def generate_from_dict(self, req_dict: Dict) -> Dict:
        """Generate from a dictionary (for API calls)."""
        request = VizRequest(
            title=req_dict.get('title', 'Chart'),
            chart_type=req_dict.get('chart_type', 'bar'),
            data=req_dict.get('data', []),
            x_field=req_dict.get('x_field'),
            y_field=req_dict.get('y_field'),
            color_field=req_dict.get('color_field'),
            description=req_dict.get('description', ''),
            insight=req_dict.get('insight', ''),
        )
        return self.generate(request)
    
    # -------------------------------------------------------------------------
    # Chart Type Generators
    # -------------------------------------------------------------------------
    
    def _base_spec(self, request: VizRequest) -> Dict:
        """Create base spec with brand styling."""
        return {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "title": {
                "text": request.title,
                "color": BRAND["text"],
                "anchor": "start",
                "fontSize": 16,
                "subtitle": request.insight if request.insight else None,
                "subtitleColor": BRAND["text_muted"],
            },
            "width": 400,
            "height": 250,
            "data": {"values": request.data},
            "config": {
                "background": BRAND["bg_dark"],
                "view": {"stroke": None},
                "axis": {
                    "labelColor": BRAND["text_muted"],
                    "titleColor": BRAND["text"],
                    "gridColor": "#374151",
                },
                "legend": {
                    "labelColor": BRAND["text_muted"],
                    "titleColor": BRAND["text"],
                },
            }
        }
    
    def _gen_bar(self, request: VizRequest) -> Dict:
        """Generate bar chart."""
        spec = self._base_spec(request)
        spec["mark"] = {"type": "bar", "cornerRadiusEnd": 4}
        spec["encoding"] = {
            "x": {"field": request.x_field or "category", "type": "nominal", "title": None},
            "y": {"field": request.y_field or "value", "type": "quantitative"},
            "color": {
                "field": request.color_field or request.x_field or "category",
                "type": "nominal",
                "scale": {"range": BRAND_PALETTE},
                "legend": None,
            },
            "tooltip": [
                {"field": request.x_field or "category"},
                {"field": request.y_field or "value"},
            ]
        }
        return spec
    
    def _gen_line(self, request: VizRequest) -> Dict:
        """Generate line chart."""
        spec = self._base_spec(request)
        spec["mark"] = {"type": "line", "strokeWidth": 3, "point": True}
        spec["encoding"] = {
            "x": {"field": request.x_field or "date", "type": "temporal", "title": None},
            "y": {"field": request.y_field or "value", "type": "quantitative"},
            "color": {"value": BRAND["cyan"]},
            "tooltip": [
                {"field": request.x_field or "date"},
                {"field": request.y_field or "value"},
            ]
        }
        return spec
    
    def _gen_scatter(self, request: VizRequest) -> Dict:
        """Generate scatter plot."""
        spec = self._base_spec(request)
        spec["mark"] = {"type": "circle", "size": 80}
        spec["encoding"] = {
            "x": {"field": request.x_field or "x", "type": "quantitative"},
            "y": {"field": request.y_field or "y", "type": "quantitative"},
            "color": {
                "field": request.color_field or "category",
                "type": "nominal",
                "scale": {"range": BRAND_PALETTE},
            },
            "tooltip": [
                {"field": request.x_field or "x"},
                {"field": request.y_field or "y"},
            ]
        }
        return spec
    
    def _gen_pie(self, request: VizRequest) -> Dict:
        """Generate pie/donut chart."""
        spec = self._base_spec(request)
        spec["mark"] = {"type": "arc", "innerRadius": 50}
        spec["encoding"] = {
            "theta": {"field": request.y_field or "value", "type": "quantitative"},
            "color": {
                "field": request.x_field or "category",
                "type": "nominal",
                "scale": {"range": BRAND_PALETTE},
            },
            "tooltip": [
                {"field": request.x_field or "category"},
                {"field": request.y_field or "value"},
            ]
        }
        return spec
    
    def _gen_gauge(self, request: VizRequest) -> Dict:
        """Generate gauge chart for single metric."""
        # Extract the value from data
        value = request.data[0].get(request.y_field or 'value', 50) if request.data else 50
        max_val = 100
        
        gauge_data = [
            {"segment": "Value", "value": value},
            {"segment": "Remaining", "value": max_val - value},
        ]
        
        spec = self._base_spec(request)
        spec["data"] = {"values": gauge_data}
        spec["mark"] = {"type": "arc", "innerRadius": 60, "outerRadius": 100}
        spec["encoding"] = {
            "theta": {"field": "value", "type": "quantitative", "stack": True},
            "color": {
                "field": "segment",
                "type": "nominal",
                "scale": {
                    "domain": ["Value", "Remaining"],
                    "range": [BRAND["cyan"], "#1e293b"],
                },
                "legend": None,
            },
        }
        spec["width"] = 200
        spec["height"] = 200
        return spec
    
    def _gen_funnel(self, request: VizRequest) -> Dict:
        """Generate funnel chart."""
        spec = self._base_spec(request)
        spec["mark"] = {"type": "bar", "cornerRadiusEnd": 4}
        spec["encoding"] = {
            "y": {"field": request.x_field or "stage", "type": "ordinal", "sort": None, "title": None},
            "x": {"field": request.y_field or "value", "type": "quantitative"},
            "color": {
                "field": request.x_field or "stage",
                "type": "nominal",
                "scale": {"range": BRAND_PALETTE},
                "legend": None,
            },
        }
        return spec
    
    def _gen_heatmap(self, request: VizRequest) -> Dict:
        """Generate heatmap."""
        spec = self._base_spec(request)
        spec["mark"] = "rect"
        spec["encoding"] = {
            "x": {"field": request.x_field or "x", "type": "ordinal"},
            "y": {"field": request.y_field or "y", "type": "ordinal"},
            "color": {
                "field": request.color_field or "value",
                "type": "quantitative",
                "scale": {"range": [BRAND["purple"], BRAND["cyan"]]},
            },
        }
        return spec
    
    def _gen_radial(self, request: VizRequest) -> Dict:
        """Generate radial/arc chart."""
        spec = self._base_spec(request)
        spec["mark"] = {"type": "arc", "innerRadius": 30}
        spec["encoding"] = {
            "theta": {"field": request.y_field or "value", "type": "quantitative", "stack": True},
            "color": {
                "field": request.x_field or "category",
                "type": "nominal",
                "scale": {"range": BRAND_PALETTE},
            },
        }
        return spec
    
    def _gen_timeline(self, request: VizRequest) -> Dict:
        """Generate timeline with events."""
        spec = self._base_spec(request)
        spec["mark"] = {"type": "circle", "size": 100}
        spec["encoding"] = {
            "x": {"field": request.x_field or "date", "type": "temporal"},
            "y": {"value": 0},
            "color": {
                "field": request.color_field or "category",
                "type": "nominal",
                "scale": {"range": BRAND_PALETTE},
            },
            "tooltip": [
                {"field": request.x_field or "date"},
                {"field": "event", "type": "nominal"},
            ]
        }
        spec["height"] = 80
        return spec


# =============================================================================
# AI VISUALIZATION ASSISTANT
# =============================================================================

class AIVizAssistant:
    """
    Provides a natural language interface for AI to request visualizations.
    
    The AI describes what insight it wants to communicate,
    and this assistant generates the appropriate chart.
    """
    
    def __init__(self):
        self.engine = DynamicVizEngine()
    
    def visualize_comparison(
        self,
        title: str,
        categories: List[str],
        values: List[float],
        insight: str = ""
    ) -> Dict:
        """
        Create a comparison chart (bar).
        
        Example: "Compare market share: [Microsoft 35%, Google 30%, Amazon 25%]"
        """
        data = [{"category": cat, "value": val} for cat, val in zip(categories, values)]
        request = VizRequest(
            title=title,
            chart_type='bar',
            data=data,
            x_field='category',
            y_field='value',
            insight=insight,
        )
        return self.engine.generate(request)
    
    def visualize_trend(
        self,
        title: str,
        dates: List[str],
        values: List[float],
        insight: str = ""
    ) -> Dict:
        """
        Create a trend chart (line).
        
        Example: "Show competitor growth Q1-Q4"
        """
        data = [{"date": d, "value": v} for d, v in zip(dates, values)]
        request = VizRequest(
            title=title,
            chart_type='line',
            data=data,
            x_field='date',
            y_field='value',
            insight=insight,
        )
        return self.engine.generate(request)
    
    def visualize_distribution(
        self,
        title: str,
        categories: List[str],
        values: List[float],
        insight: str = ""
    ) -> Dict:
        """
        Create a distribution chart (pie/donut).
        
        Example: "Market segment breakdown"
        """
        data = [{"category": cat, "value": val} for cat, val in zip(categories, values)]
        request = VizRequest(
            title=title,
            chart_type='pie',
            data=data,
            x_field='category',
            y_field='value',
            insight=insight,
        )
        return self.engine.generate(request)
    
    def visualize_metric(
        self,
        title: str,
        value: float,
        max_value: float = 100,
        insight: str = ""
    ) -> Dict:
        """
        Create a single metric gauge.
        
        Example: "Customer satisfaction score: 85/100"
        """
        data = [{"value": value, "max": max_value}]
        request = VizRequest(
            title=title,
            chart_type='gauge',
            data=data,
            y_field='value',
            insight=insight,
        )
        return self.engine.generate(request)
    
    def visualize_funnel(
        self,
        title: str,
        stages: List[str],
        values: List[float],
        insight: str = ""
    ) -> Dict:
        """
        Create a funnel chart.
        
        Example: "Sales pipeline: Leads→Qualified→Proposals→Closed"
        """
        data = [{"stage": s, "value": v, "order": i} for i, (s, v) in enumerate(zip(stages, values))]
        request = VizRequest(
            title=title,
            chart_type='funnel',
            data=data,
            x_field='stage',
            y_field='value',
            insight=insight,
        )
        return self.engine.generate(request)
    
    def visualize_custom(self, request_dict: Dict) -> Dict:
        """
        Generate a custom visualization from a dictionary spec.
        
        For flexible, AI-defined charts.
        """
        return self.engine.generate_from_dict(request_dict)
    
    def get_chart_history(self) -> List[Dict]:
        """Get all charts generated in this session."""
        return self.engine.generated_charts
