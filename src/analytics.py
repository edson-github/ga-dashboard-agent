import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional

class AnalyticsEngine:
    """Engine for computing GA metrics and insights"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
    
    def compute_summary_metrics(self) -> Dict[str, Any]:
        """Calculate high-level summary metrics"""
        summary = {
            'total_users': self._safe_sum('users'),
            'total_sessions': self._safe_sum('sessions'),
            'total_pageviews': self._safe_sum('pageviews'),
            'total_conversions': self._safe_sum('conversions'),
            'total_revenue': self._safe_sum('revenue'),
            'avg_bounce_rate': self._safe_mean('bounce_rate'),
            'avg_session_duration': self._safe_mean('avg_session_duration'),
            'pages_per_session': self._calculate_pages_per_session(),
            'conversion_rate': self._calculate_conversion_rate(),
            'date_range': self._get_date_range()
        }
        return summary
    
    def analyze_source_medium(self) -> Dict[str, Any]:
        """Detailed source/medium analysis"""
        if 'source_medium' not in self.data.columns:
            if 'source' in self.data.columns:
                group_col = 'source'
            else:
                return {'error': 'No source/medium data available'}
        else:
            group_col = 'source_medium'
        
        # Aggregate by source/medium
        agg_cols = {col: 'sum' for col in ['users', 'sessions', 'pageviews', 
                                            'conversions', 'revenue'] 
                   if col in self.data.columns}
        
        if 'bounce_rate' in self.data.columns:
            agg_cols['bounce_rate'] = 'mean'
        if 'avg_session_duration' in self.data.columns:
            agg_cols['avg_session_duration'] = 'mean'
        
        grouped = self.data.groupby(group_col).agg(agg_cols).reset_index()
        
        # Calculate derived metrics
        if 'users' in grouped.columns and 'sessions' in grouped.columns:
            grouped['sessions_per_user'] = grouped['sessions'] / grouped['users'].replace(0, np.nan)
        
        if 'conversions' in grouped.columns and 'sessions' in grouped.columns:
            grouped['conversion_rate'] = (grouped['conversions'] / grouped['sessions'].replace(0, np.nan)) * 100
        
        # Sort by users (primary traffic indicator)
        grouped = grouped.sort_values('users', ascending=False)
        
        # Performance categorization
        analysis = {
            'by_channel': grouped.to_dict('records'),
            'top_performers': self._identify_top_performers(grouped),
            'underperformers': self._identify_underperformers(grouped),
            'channel_distribution': self._calculate_distribution(grouped, 'users'),
            'quality_analysis': self._analyze_traffic_quality(grouped)
        }
        
        return analysis
    
    def analyze_user_behavior(self) -> Dict[str, Any]:
        """Analyze user behavior patterns"""
        behavior = {
            'engagement_metrics': self._compute_engagement_metrics(),
            'session_analysis': self._analyze_sessions(),
            'retention_indicators': self._compute_retention_indicators(),
            'user_journey': self._analyze_user_journey()
        }
        return behavior
    
    def analyze_events(self) -> Dict[str, Any]:
        """Analyze website events"""
        if 'event_name' not in self.data.columns:
            return {'message': 'No event data available in CSV'}
        
        event_analysis = {
            'event_summary': self._summarize_events(),
            'top_events': self._get_top_events(),
            'conversion_events': self._identify_conversion_events(),
            'engagement_events': self._categorize_engagement_events()
        }
        return event_analysis
    
    def _identify_top_performers(self, grouped: pd.DataFrame) -> List[Dict]:
        """Identify top performing channels"""
        top = grouped.head(5)
        performers = []
        
        for _, row in top.iterrows():
            performer = {
                'channel': row.get('source_medium', row.get('source', 'Unknown')),
                'users': int(row.get('users', 0)),
                'performance_score': self._calculate_performance_score(row)
            }
            performers.append(performer)
        
        return performers
    
    def _identify_underperformers(self, grouped: pd.DataFrame) -> List[Dict]:
        """Identify underperforming channels needing attention"""
        # Channels with high bounce rate or low conversion
        underperformers = []
        
        if 'bounce_rate' in grouped.columns:
            high_bounce = grouped[grouped['bounce_rate'] > grouped['bounce_rate'].mean() + grouped['bounce_rate'].std()]
            for _, row in high_bounce.iterrows():
                underperformers.append({
                    'channel': row.get('source_medium', row.get('source', 'Unknown')),
                    'issue': 'High bounce rate',
                    'bounce_rate': round(row['bounce_rate'], 2)
                })
        
        return underperformers[:5]
    
    def _calculate_performance_score(self, row) -> float:
        """Calculate composite performance score"""
        score = 0
        weights = {'conversion_rate': 0.4, 'sessions_per_user': 0.3, 'bounce_rate': -0.3}
        
        for metric, weight in weights.items():
            if metric in row.index and pd.notna(row[metric]):
                if weight > 0:
                    score += row[metric] * weight
                else:
                    score += (100 - row[metric]) * abs(weight)
        
        return round(score, 2)
    
    def _safe_sum(self, col: str) -> float:
        return float(self.data[col].sum()) if col in self.data.columns else 0
    
    def _safe_mean(self, col: str) -> float:
        return float(self.data[col].mean()) if col in self.data.columns else 0
    
    def _calculate_pages_per_session(self) -> float:
        if 'pageviews' in self.data.columns and 'sessions' in self.data.columns:
            total_sessions = self.data['sessions'].sum()
            if total_sessions > 0:
                return round(self.data['pageviews'].sum() / total_sessions, 2)
        return 0
    
    def _calculate_conversion_rate(self) -> float:
        if 'conversions' in self.data.columns and 'sessions' in self.data.columns:
            total_sessions = self.data['sessions'].sum()
            if total_sessions > 0:
                return round((self.data['conversions'].sum() / total_sessions) * 100, 2)
        return 0
    
    def _get_date_range(self) -> Dict[str, str]:
        if 'date' in self.data.columns:
            return {
                'start': str(self.data['date'].min()),
                'end': str(self.data['date'].max())
            }
        return {'start': 'N/A', 'end': 'N/A'}
    
    def _calculate_distribution(self, grouped: pd.DataFrame, metric: str) -> List[Dict]:
        if metric not in grouped.columns:
            return []
        
        total = grouped[metric].sum()
        distribution = []
        
        for _, row in grouped.iterrows():
            distribution.append({
                'channel': row.get('source_medium', row.get('source', 'Unknown')),
                'value': int(row[metric]),
                'percentage': round((row[metric] / total) * 100, 2) if total > 0 else 0
            })
        
        return distribution
    
    def _analyze_traffic_quality(self, grouped: pd.DataFrame) -> Dict[str, Any]:
        """Analyze quality of traffic from different sources"""
        quality_metrics = {}
        
        if 'bounce_rate' in grouped.columns:
            quality_metrics['avg_bounce_rate'] = round(grouped['bounce_rate'].mean(), 2)
            quality_metrics['best_bounce_rate_channel'] = grouped.loc[grouped['bounce_rate'].idxmin(), 'source_medium'] if 'source_medium' in grouped.columns else 'N/A'
        
        if 'conversion_rate' in grouped.columns:
            quality_metrics['avg_conversion_rate'] = round(grouped['conversion_rate'].mean(), 2)
            quality_metrics['best_conversion_channel'] = grouped.loc[grouped['conversion_rate'].idxmax(), 'source_medium'] if 'source_medium' in grouped.columns else 'N/A'
        
        return quality_metrics
    
    def _compute_engagement_metrics(self) -> Dict[str, Any]:
        return {
            'avg_pages_per_session': self._calculate_pages_per_session(),
            'avg_session_duration': self._safe_mean('avg_session_duration'),
            'engagement_rate': 100 - self._safe_mean('bounce_rate')
        }
    
    def _analyze_sessions(self) -> Dict[str, Any]:
        return {
            'total_sessions': self._safe_sum('sessions'),
            'sessions_per_user': round(self._safe_sum('sessions') / max(self._safe_sum('users'), 1), 2)
        }
    
    def _compute_retention_indicators(self) -> Dict[str, Any]:
        return {
            'returning_user_indicator': round(self._safe_mean('sessions') / max(self._safe_sum('users'), 1), 2)
        }
    
    def _analyze_user_journey(self) -> Dict[str, Any]:
        return {
            'avg_touchpoints': self._calculate_pages_per_session(),
            'conversion_funnel_rate': self._calculate_conversion_rate()
        }
    
    def _summarize_events(self) -> Dict[str, Any]:
        if 'event_name' not in self.data.columns:
            return {}
        return {
            'total_events': int(self._safe_sum('event_count')),
            'unique_event_types': int(self.data['event_name'].nunique())
        }
    
    def _get_top_events(self, n: int = 10) -> List[Dict]:
        if 'event_name' not in self.data.columns:
            return []
        
        event_counts = self.data.groupby('event_name')['event_count'].sum().sort_values(ascending=False).head(n)
        return [{'event': name, 'count': int(count)} for name, count in event_counts.items()]
    
    def _identify_conversion_events(self) -> List[str]:
        conversion_keywords = ['purchase', 'signup', 'submit', 'complete', 'conversion', 'lead']
        if 'event_name' not in self.data.columns:
            return []
        
        events = self.data['event_name'].unique()
        return [e for e in events if any(kw in str(e).lower() for kw in conversion_keywords)]
    
    def _categorize_engagement_events(self) -> Dict[str, List[str]]:
        engagement_categories = {
            'navigation': ['page_view', 'scroll', 'click'],
            'interaction': ['video_play', 'file_download', 'form_start'],
            'conversion': ['purchase', 'sign_up', 'generate_lead']
        }
        
        if 'event_name' not in self.data.columns:
            return {}
        
        events = self.data['event_name'].unique()
        categorized = {cat: [] for cat in engagement_categories}
        
        for event in events:
            for category, keywords in engagement_categories.items():
                if any(kw in str(event).lower() for kw in keywords):
                    categorized[category].append(str(event))
                    break
        
        return categorized
