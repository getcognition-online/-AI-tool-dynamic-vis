# Dynamic AI Visualization Engine

[![PyPI version](https://badge.fury.io/py/dynamic-viz.svg)](https://badge.fury.io/py/dynamic-viz)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Open Source by GetCognition** 💚

A visualization engine that allows AI/LLM systems to programmatically request and generate custom visualizations to explain insights.

## ✨ Features

- 🎨 **9 Chart Types**: Bar, Line, Scatter, Pie, Gauge, Funnel, Heatmap, Radial, Timeline
- 🤖 **AI-First Design**: Natural language interface for AI to request visualizations
- 📚 **Vega-Lite Output**: Standards-based, renders anywhere
- 🎯 **Customizable**: Easy to override colors and styling

## 📦 Installation

```bash
pip install dynamic-viz
```

For full features (recommended):
```bash
pip install dynamic-viz[altair]
```

## 🚀 Quick Start

```python
from dynamic_viz import AIVizAssistant

assistant = AIVizAssistant()

# AI requests a comparison chart
spec = assistant.visualize_comparison(
    title="Competitor Threat Levels",
    categories=["Crayon", "Klue", "Kompyte"],
    values=[8, 7, 5],
    insight="Crayon is the primary threat"
)

# Render with vega-embed in browser or save as JSON
print(spec)
```

## 📊 Available Methods

### Comparison (Bar Chart)
```python
spec = assistant.visualize_comparison(
    title="Market Share",
    categories=["Microsoft", "Google", "Amazon"],
    values=[35, 30, 25],
    insight="Microsoft leads the market"
)
```

### Trend (Line Chart)
```python
spec = assistant.visualize_trend(
    title="Revenue Growth",
    dates=["2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4"],
    values=[100, 120, 135, 150],
    insight="Consistent 15% quarterly growth"
)
```

### Distribution (Pie/Donut)
```python
spec = assistant.visualize_distribution(
    title="Market Segments",
    categories=["Enterprise", "SMB", "Consumer"],
    values=[50, 35, 15]
)
```

### Single Metric (Gauge)
```python
spec = assistant.visualize_metric(
    title="Customer Satisfaction",
    value=85,
    max_value=100,
    insight="Above target of 80"
)
```

### Funnel
```python
spec = assistant.visualize_funnel(
    title="Sales Pipeline",
    stages=["Leads", "Qualified", "Proposals", "Closed"],
    values=[1000, 500, 200, 50]
)
```

### Custom (Any Vega-Lite Spec)
```python
spec = assistant.visualize_custom({
    "title": "Custom Chart",
    "chart_type": "scatter",
    "data": [{"x": 1, "y": 2}, {"x": 3, "y": 4}],
    "x_field": "x",
    "y_field": "y"
})
```

## 🎨 Customization

```python
from dynamic_viz import BRAND

# Override colors
BRAND["primary"] = "#00F5FF"
BRAND["secondary"] = "#E000FF"
BRAND["background"] = "#111827"
BRAND["text"] = "#e2e8f0"
```

## 🔧 API Reference

### AIVizAssistant

| Method | Description |
|--------|-------------|
| `visualize_comparison()` | Bar chart for category comparison |
| `visualize_trend()` | Line chart for time series |
| `visualize_distribution()` | Pie/donut for proportions |
| `visualize_metric()` | Gauge for single value |
| `visualize_funnel()` | Funnel for process stages |
| `visualize_custom()` | Any chart from dict spec |
| `get_chart_history()` | Get all generated charts |

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 💚 Credits

Open sourced with love by [GetCognition](https://getcognition.ai)

### Built With
- [Altair](https://altair-viz.github.io/) - Declarative statistical visualization library for Python
- [Vega-Lite](https://vega.github.io/vega-lite/) - Grammar of interactive graphics
- [Vega](https://vega.github.io/vega/) - Visualization grammar

Special thanks to the Altair team for their amazing work on declarative visualization! 🙏

