from dataclasses import dataclass
from typing import Dict, List, Any
from datetime import datetime

@dataclass
class DashboardMetrics:
    """Container for dashboard metrics and insights"""
    summary: Dict[str, Any]
    source_medium_analysis: Dict[str, Any]
    user_behavior: Dict[str, Any]
    event_analysis: Dict[str, Any]
    insights: List[str]
    recommendations: List[str]

class DashboardGenerator:
    """Generate dashboard with AI-powered insights"""
    
    def __init__(self, metrics: DashboardMetrics, llm_client=None):
        self.metrics = metrics
        self.llm_client = llm_client
    
    def generate_dashboard(self) -> Dict[str, Any]:
        """Generate complete dashboard structure"""
        dashboard = {
            'title': 'Google Analytics Performance Dashboard',
            'generated_at': datetime.now().isoformat(),
            'sections': [
                self._generate_executive_summary(),
                self._generate_traffic_overview(),
                self._generate_source_medium_section(),
                self._generate_user_behavior_section(),
                self._generate_events_section(),
                self._generate_insights_section(),
                self._generate_recommendations_section()
            ]
        }
        return dashboard
    
    def _generate_executive_summary(self) -> Dict[str, Any]:
        """Generate executive summary section"""
        summary = self.metrics.summary
        
        return {
            'section_id': 'executive_summary',
            'title': 'Executive Summary',
            'description': self._get_summary_narrative(summary),
            'kpis': [
                {
                    'name': 'Total Users',
                    'value': f"{summary.get('total_users', 0):,.0f}",
                    'description': 'Unique visitors to your website during this period'
                },
                {
                    'name': 'Total Sessions',
                    'value': f"{summary.get('total_sessions', 0):,.0f}",
                    'description': 'Total number of visits (a user can have multiple sessions)'
                },
                {
                    'name': 'Conversion Rate',
                    'value': f"{summary.get('conversion_rate', 0):.2f}%",
                    'description': 'Percentage of sessions that resulted in a conversion'
                },
                {
                    'name': 'Bounce Rate',
                    'value': f"{summary.get('avg_bounce_rate', 0):.2f}%",
                    'description': 'Percentage of single-page sessions (lower is generally better)'
                },
                {
                    'name': 'Pages/Session',
                    'value': f"{summary.get('pages_per_session', 0):.2f}",
                    'description': 'Average number of pages viewed per session'
                },
                {
                    'name': 'Total Revenue',
                    'value': f"${summary.get('total_revenue', 0):,.2f}",
                    'description': 'Total revenue generated during this period'
                }
            ]
        }
    
    def _get_summary_narrative(self, summary: Dict) -> str:
        """Generate narrative summary"""
        return f"""
During the reporting period ({summary.get('date_range', {}).get('start', 'N/A')} to {summary.get('date_range', {}).get('end', 'N/A')}), 
your website attracted {summary.get('total_users', 0):,.0f} users who initiated {summary.get('total_sessions', 0):,.0f} sessions. 
Users viewed an average of {summary.get('pages_per_session', 0):.2f} pages per session, 
with an overall bounce rate of {summary.get('avg_bounce_rate', 0):.2f}%. 
The conversion rate stood at {summary.get('conversion_rate', 0):.2f}%, 
generating ${summary.get('total_revenue', 0):,.2f} in total revenue.
        """.strip()
    
    def _generate_traffic_overview(self) -> Dict[str, Any]:
        """Generate traffic overview section"""
        source_analysis = self.metrics.source_medium_analysis
        
        return {
            'section_id': 'traffic_overview',
            'title': 'Traffic Overview by Source/Medium',
            'description': '''
This section breaks down your website traffic by acquisition source and medium. 
Understanding where your visitors come from helps optimize marketing spend and identify 
high-value traffic channels.
            '''.strip(),
            'charts': [
                {
                    'type': 'pie',
                    'title': 'Traffic Distribution by Channel',
                    'data': source_analysis.get('channel_distribution', [])
                },
                {
                    'type': 'bar',
                    'title': 'Users by Source/Medium',
                    'data': source_analysis.get('by_channel', [])[:10]
                }
            ],
            'table': {
                'title': 'Channel Performance Details',
                'columns': ['Channel', 'Users', 'Sessions', 'Bounce Rate', 'Conv. Rate'],
                'data': source_analysis.get('by_channel', [])
            }
        }
    
    def _generate_source_medium_section(self) -> Dict[str, Any]:
        """Generate detailed source/medium analysis section"""
        analysis = self.metrics.source_medium_analysis
        
        top_performers = analysis.get('top_performers', [])
        underperformers = analysis.get('underperformers', [])
        quality = analysis.get('quality_analysis', {})
        
        explanations = []
        
        # Top performers explanation
        if top_performers:
            top_channel = top_performers[0]
            explanations.append({
                'title': 'Top Performing Channel',
                'content': f"""
**{top_channel.get('channel', 'Unknown')}** is your top traffic source with {top_channel.get('users', 0):,} users.
This channel has a performance score of {top_channel.get('performance_score', 0)}, indicating strong engagement 
and conversion metrics. Consider increasing investment in this channel to drive more qualified traffic.
                """.strip()
            })
        
        # Quality analysis explanation
        if quality:
            explanations.append({
                'title': 'Traffic Quality Analysis',
                'content': f"""
**Best Quality Traffic**: {quality.get('best_conversion_channel', 'N/A')} shows the highest conversion rate, 
making it your most valuable traffic source for driving business outcomes.

**Engagement Leader**: {quality.get('best_bounce_rate_channel', 'N/A')} has the lowest bounce rate at 
{quality.get('avg_bounce_rate', 0):.2f}%, indicating highly engaged visitors.
                """.strip()
            })
        
        # Underperformers explanation
        if underperformers:
            problem_channels = ', '.join([u.get('channel', 'Unknown') for u in underperformers[:3]])
            explanations.append({
                'title': 'Channels Requiring Attention',
                'content': f"""
The following channels show concerning metrics: **{problem_channels}**. 
These sources have higher than average bounce rates, suggesting potential issues with:
- Landing page relevance
- Traffic quality
- User intent mismatch

Consider reviewing landing pages and audience targeting for these channels.
                """.strip()
            })
        
        return {
            'section_id': 'source_medium_analysis',
            'title': 'Source/Medium Deep Dive',
            'description': 'Detailed analysis of traffic acquisition channels with performance insights',
            'explanations': explanations,
            'data': {
                'top_performers': top_performers,
                'underperformers': underperformers,
                'quality_metrics': quality
            }
        }
    
    def _generate_user_behavior_section(self) -> Dict[str, Any]:
        """Generate user behavior analysis section"""
        behavior = self.metrics.user_behavior
        engagement = behavior.get('engagement_metrics', {})
        sessions = behavior.get('session_analysis', {})
        
        return {
            'section_id': 'user_behavior',
            'title': 'User Behavior Analysis',
            'description': '''
Understanding how users interact with your website is crucial for optimization. 
This section analyzes engagement patterns, session behavior, and user journey metrics.
            '''.strip(),
            'metrics': [
                {
                    'name': 'Average Pages per Session',
                    'value': engagement.get('avg_pages_per_session', 0),
                    'interpretation': self._interpret_pages_per_session(engagement.get('avg_pages_per_session', 0))
                },
                {
                    'name': 'Average Session Duration',
                    'value': f"{engagement.get('avg_session_duration', 0):.0f} seconds",
                    'interpretation': self._interpret_session_duration(engagement.get('avg_session_duration', 0))
                },
                {
                    'name': 'Engagement Rate',
                    'value': f"{engagement.get('engagement_rate', 0):.2f}%",
                    'interpretation': self._interpret_engagement_rate(engagement.get('engagement_rate', 0))
                },
                {
                    'name': 'Sessions per User',
                    'value': sessions.get('sessions_per_user', 0),
                    'interpretation': self._interpret_sessions_per_user(sessions.get('sessions_per_user', 0))
                }
            ],
            'behavior_insights': self._generate_behavior_insights(behavior)
        }
    
    def _interpret_pages_per_session(self, value: float) -> str:
        if value < 1.5:
            return "Low engagement - users are leaving quickly. Consider improving content relevance and internal linking."
        elif value < 3:
            return "Moderate engagement - users are exploring some content. Room for improvement in site navigation."
        else:
            return "Strong engagement - users are actively exploring multiple pages. Your content resonates well."
    
    def _interpret_session_duration(self, value: float) -> str:
        if value < 60:
            return "Very short sessions - users may not be finding what they need quickly."
        elif value < 180:
            return "Average session length - consider adding more engaging content to increase time on site."
        else:
            return "Excellent session duration - users are spending quality time with your content."
    
    def _interpret_engagement_rate(self, value: float) -> str:
        if value < 50:
            return "Low engagement rate - more than half of visitors leave immediately. Review landing pages."
        elif value < 70:
            return "Moderate engagement - room to improve landing page relevance and user experience."
        else:
            return "High engagement rate - your content successfully captures visitor interest."
    
    def _interpret_sessions_per_user(self, value: float) -> str:
        if value < 1.2:
            return "Most users visit only once - focus on retention strategies and email capture."
        elif value < 2:
            return "Some repeat visitors - consider loyalty programs and remarketing campaigns."
        else:
            return "Strong repeat visitation - users find value in returning to your site."
    
    def _generate_behavior_insights(self, behavior: Dict) -> List[str]:
        insights = []
        engagement = behavior.get('engagement_metrics', {})
        
        if engagement.get('engagement_rate', 0) > 70:
            insights.append("✅ Your engagement rate is above industry average, indicating relevant traffic and good UX.")
        else:
            insights.append("⚠️ Consider A/B testing landing pages to improve engagement rate.")
        
        if engagement.get('avg_pages_per_session', 0) > 2.5:
            insights.append("✅ Users are exploring your site deeply - your internal linking strategy is working.")
        else:
            insights.append("💡 Add more internal links and related content suggestions to increase page depth.")
        
        return insights
    
    def _generate_events_section(self) -> Dict[str, Any]:
        """Generate events analysis section"""
        events = self.metrics.event_analysis
        
        if 'message' in events:
            return {
                'section_id': 'events',
                'title': 'Event Analysis',
                'description': events['message'],
                'data': {}
            }
        
        return {
            'section_id': 'events',
            'title': 'Website Events Analysis',
            'description': '''
Events track specific user interactions on your website beyond pageviews. 
This includes clicks, form submissions, video plays, downloads, and conversion actions.
            '''.strip(),
            'summary': events.get('event_summary', {}),
            'top_events': {
                'title': 'Most Frequent Events',
                'description': 'These events occur most often on your website',
                'data': events.get('top_events', [])
            },
            'conversion_events': {
                'title': 'Conversion Events',
                'description': 'Events that indicate valuable user actions',
                'data': events.get('conversion_events', [])
            },
            'event_categories': events.get('engagement_events', {})
        }
    
    def _generate_insights_section(self) -> Dict[str, Any]:
        """Generate AI-powered insights section"""
        insights = self._compile_insights()
        
        return {
            'section_id': 'insights',
            'title': 'Key Insights & Findings',
            'description': 'Automated analysis of your data has revealed these important insights:',
            'insights': insights
        }
    
    def _compile_insights(self) -> List[Dict[str, str]]:
        """Compile insights from all analyses"""
        insights = []
        
        # Traffic insights
        source_analysis = self.metrics.source_medium_analysis
        if source_analysis.get('top_performers'):
            top = source_analysis['top_performers'][0]
            insights.append({
                'category': 'Traffic',
                'type': 'positive',
                'title': 'Top Traffic Source Identified',
                'description': f"{top.get('channel', 'Unknown')} drives the most users to your site with {top.get('users', 0):,} visitors."
            })
        
        # Conversion insights
        summary = self.metrics.summary
        if summary.get('conversion_rate', 0) > 3:
            insights.append({
                'category': 'Conversion',
                'type': 'positive',
                'title': 'Strong Conversion Rate',
                'description': f"Your {summary.get('conversion_rate', 0):.2f}% conversion rate is above the industry average of 2-3%."
            })
        elif summary.get('conversion_rate', 0) > 0:
            insights.append({
                'category': 'Conversion',
                'type': 'warning',
                'title': 'Conversion Rate Optimization Needed',
                'description': f"Your {summary.get('conversion_rate', 0):.2f}% conversion rate has room for improvement. Consider CRO testing."
            })
        
        # Engagement insights
        behavior = self.metrics.user_behavior
        if behavior.get('engagement_metrics', {}).get('engagement_rate', 0) < 50:
            insights.append({
                'category': 'Engagement',
                'type': 'critical',
                'title': 'High Bounce Rate Alert',
                'description': 'More than half of visitors leave without engaging. Review landing page relevance and load times.'
            })
        
        return insights
    
    def _generate_recommendations_section(self) -> Dict[str, Any]:
        """Generate actionable recommendations"""
        recommendations = self._compile_recommendations()
        
        return {
            'section_id': 'recommendations',
            'title': 'Actionable Recommendations',
            'description': 'Based on the analysis, here are prioritized recommendations to improve performance:',
            'recommendations': recommendations
        }
    
    def _compile_recommendations(self) -> List[Dict[str, Any]]:
        """Compile recommendations based on analysis"""
        recommendations = []
        
        summary = self.metrics.summary
        source_analysis = self.metrics.source_medium_analysis
        
        # Traffic recommendations
        if source_analysis.get('top_performers'):
            top = source_analysis['top_performers'][0]
            recommendations.append({
                'priority': 'High',
                'category': 'Traffic Acquisition',
                'title': f"Increase investment in {top.get('channel', 'top channel')}",
                'description': 'This channel shows the best performance. Consider increasing budget or content creation for this source.',
                'expected_impact': 'Potential 15-25% increase in quality traffic'
            })
        
        # Conversion recommendations
        if summary.get('conversion_rate', 0) < 3:
            recommendations.append({
                'priority': 'High',
                'category': 'Conversion Optimization',
                'title': 'Implement Conversion Rate Optimization',
                'description': 'A/B test landing pages, simplify conversion forms, and add trust signals near CTAs.',
                'expected_impact': 'Potential 0.5-1% improvement in conversion rate'
            })
        
        # Engagement recommendations
        if summary.get('avg_bounce_rate', 0) > 60:
            recommendations.append({
                'priority': 'Medium',
                'category': 'User Experience',
                'title': 'Reduce Bounce Rate',
                'description': 'Improve page load speed, ensure mobile optimization, and enhance above-the-fold content.',
                'expected_impact': 'Potential 10-15% reduction in bounce rate'
            })
        
        # Underperformer recommendations
        if source_analysis.get('underperformers'):
            recommendations.append({
                'priority': 'Medium',
                'category': 'Channel Optimization',
                'title': 'Review Underperforming Channels',
                'description': 'Audit landing pages and targeting for channels with high bounce rates. Consider pausing or reallocating budget.',
                'expected_impact': 'Better ROI on marketing spend'
            })
        
        return recommendations
