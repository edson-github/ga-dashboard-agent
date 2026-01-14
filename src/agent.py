from typing import Dict, Any
import json
from .loader import GADataLoader
from .analytics import AnalyticsEngine
from .dashboard import DashboardGenerator, DashboardMetrics

class GADashboardAgent:
    """Main orchestrator for GA Dashboard generation"""
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.data = None
        self.analytics_engine = None
        self.dashboard_generator = None
    
    def process(self, csv_file_path: str) -> Dict[str, Any]:
        """
        Main entry point - process CSV and generate dashboard
        
        Args:
            csv_file_path: Path to the Google Analytics CSV export
            
        Returns:
            Complete dashboard with analysis and recommendations
        """
        # Step 1: Load and validate data
        print("📊 Loading CSV data...")
        self._load_data(csv_file_path)
        
        # Step 2: Initialize analytics engine
        print("🔍 Analyzing data...")
        self.analytics_engine = AnalyticsEngine(self.data)
        
        # Step 3: Compute all metrics
        metrics = DashboardMetrics(
            summary=self.analytics_engine.compute_summary_metrics(),
            source_medium_analysis=self.analytics_engine.analyze_source_medium(),
            user_behavior=self.analytics_engine.analyze_user_behavior(),
            event_analysis=self.analytics_engine.analyze_events(),
            insights=[],
            recommendations=[]
        )
        
        # Step 4: Generate dashboard
        print("📈 Generating dashboard...")
        self.dashboard_generator = DashboardGenerator(metrics, self.llm_client)
        dashboard = self.dashboard_generator.generate_dashboard()
        
        print("✅ Dashboard generation complete!")
        return dashboard
    
    def _load_data(self, file_path: str):
        """Load CSV with comprehensive error handling"""
        loader = GADataLoader()
        self.data = loader.load_csv(file_path)
    
    def export_dashboard(self, dashboard: Dict, format: str = 'json') -> str:
        """Export dashboard to various formats"""
        if format == 'json':
            return json.dumps(dashboard, indent=2, default=str)
        elif format == 'html':
            return self._generate_html_dashboard(dashboard)
        elif format == 'markdown':
            return self._generate_markdown_dashboard(dashboard)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _generate_html_dashboard(self, dashboard: Dict) -> str:
        """Generate HTML dashboard"""
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{dashboard.get('title', 'GA Dashboard')}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               margin: 0; padding: 20px; background: #f5f5f5; }}
        .dashboard {{ max-width: 1400px; margin: 0 auto; }}
        .section {{ background: white; border-radius: 8px; padding: 24px; margin-bottom: 20px; 
                   box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .section-title {{ font-size: 1.5rem; color: #1a73e8; margin-bottom: 16px; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }}
        .kpi-card {{ background: #f8f9fa; padding: 16px; border-radius: 8px; text-align: center; }}
        .kpi-value {{ font-size: 2rem; font-weight: bold; color: #1a73e8; }}
        .kpi-name {{ font-size: 0.875rem; color: #666; margin-top: 8px; }}
        .insight {{ padding: 12px; margin: 8px 0; border-radius: 4px; }}
        .insight.positive {{ background: #e6f4ea; border-left: 4px solid #34a853; }}
        .insight.warning {{ background: #fef7e0; border-left: 4px solid #fbbc04; }}
        .insight.critical {{ background: #fce8e6; border-left: 4px solid #ea4335; }}
        .recommendation {{ padding: 16px; margin: 8px 0; background: #e8f0fe; border-radius: 4px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
        th {{ background: #f8f9fa; font-weight: 600; }}
    </style>
</head>
<body>
    <div class="dashboard">
        <h1>{dashboard.get('title', 'Google Analytics Dashboard')}</h1>
        <p>Generated: {dashboard.get('generated_at', '')}</p>
"""
        
        for section in dashboard.get('sections', []):
            html += self._render_section_html(section)
        
        html += """
    </div>
</body>
</html>
"""
        return html
    
    def _render_section_html(self, section: Dict) -> str:
        """Render a dashboard section as HTML"""
        html = f"""
        <div class="section">
            <h2 class="section-title">{section.get('title', '')}</h2>
            <p>{section.get('description', '')}</p>
"""
        
        # Render KPIs if present
        if 'kpis' in section:
            html += '<div class="kpi-grid">'
            for kpi in section['kpis']:
                html += f"""
                <div class="kpi-card">
                    <div class="kpi-value">{kpi.get('value', '')}</div>
                    <div class="kpi-name">{kpi.get('name', '')}</div>
                    <small>{kpi.get('description', '')}</small>
                </div>
"""
            html += '</div>'
        
        # Render insights if present
        if 'insights' in section:
            for insight in section['insights']:
                insight_type = insight.get('type', 'info')
                html += f"""
                <div class="insight {insight_type}">
                    <strong>{insight.get('title', '')}</strong>
                    <p>{insight.get('description', '')}</p>
                </div>
"""
        
        # Render recommendations if present
        if 'recommendations' in section:
            for rec in section['recommendations']:
                html += f"""
                <div class="recommendation">
                    <strong>[{rec.get('priority', '')}] {rec.get('title', '')}</strong>
                    <p>{rec.get('description', '')}</p>
                    <small>Expected Impact: {rec.get('expected_impact', '')}</small>
                </div>
"""
        
        html += '</div>'
        return html
    
    def _generate_markdown_dashboard(self, dashboard: Dict) -> str:
        """Generate Markdown dashboard"""
        md = f"# {dashboard.get('title', 'GA Dashboard')}\n\n"
        md += f"*Generated: {dashboard.get('generated_at', '')}*\n\n"
        
        for section in dashboard.get('sections', []):
            md += f"## {section.get('title', '')}\n\n"
            md += f"{section.get('description', '')}\n\n"
            
            if 'kpis' in section:
                md += "| Metric | Value |\n|--------|-------|\n"
                for kpi in section['kpis']:
                    md += f"| {kpi.get('name', '')} | {kpi.get('value', '')} |\n"
                md += "\n"
            
            if 'insights' in section:
                for insight in section['insights']:
                    emoji = {'positive': '✅', 'warning': '⚠️', 'critical': '🚨'}.get(insight.get('type', ''), 'ℹ️')
                    md += f"{emoji} **{insight.get('title', '')}**: {insight.get('description', '')}\n\n"
            
            if 'recommendations' in section:
                for rec in section['recommendations']:
                    md += f"### [{rec.get('priority', '')}] {rec.get('title', '')}\n"
                    md += f"{rec.get('description', '')}\n"
                    md += f"*Expected Impact: {rec.get('expected_impact', '')}*\n\n"
        
        return md
