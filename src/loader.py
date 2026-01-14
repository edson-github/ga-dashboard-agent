import pandas as pd
from typing import Dict, List, Any, Optional

class GADataLoader:
    """Helper class for loading GA CSV data"""
    
    def __init__(self):
        self.column_mappings = {
            'source': ['source', 'sessionsource', 'session_source'],
            'medium': ['medium', 'sessionmedium', 'session_medium'],
            'campaign': ['campaign', 'sessioncampaign', 'session_campaign'],
            'users': ['users', 'totalusers', 'total_users', 'activeusers'],
            'sessions': ['sessions', 'sessioncount', 'session_count'],
            'pageviews': ['pageviews', 'screenpageviews', 'screen_page_views'],
            'bounce_rate': ['bouncerate', 'bounce_rate'],
            'avg_session_duration': ['avgsessionduration', 'averagesessionduration', 'avg_session_duration'],
            'conversions': ['conversions', 'goalcompletions'],
            'revenue': ['revenue', 'totalrevenue', 'purchaserevenue'],
            'event_name': ['eventname', 'event_name'],
            'event_count': ['eventcount', 'event_count'],
            'date': ['date', 'daterange', 'daterangestart']
        }
    
    def load_csv(self, file_path: str) -> pd.DataFrame:
        """Load and prepare CSV data"""
        # Try different encodings
        data = None
        for encoding in ['utf-8', 'latin-1', 'iso-8859-1']:
            try:
                data = pd.read_csv(file_path, encoding=encoding)
                break
            except UnicodeDecodeError:
                continue
        
        if data is None:
            raise ValueError("Could not read CSV file with any supported encoding")
        
        # Standardize column names
        data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Map columns
        column_rename = {}
        for standard_name, variants in self.column_mappings.items():
            for variant in variants:
                if variant in data.columns:
                    column_rename[variant] = standard_name
                    break
        
        data.rename(columns=column_rename, inplace=True)
        
        # Create source/medium combined
        if 'source' in data.columns and 'medium' in data.columns:
            data['source_medium'] = data['source'].astype(str) + ' / ' + data['medium'].astype(str)
        
        # Convert numeric columns
        numeric_cols = ['users', 'sessions', 'pageviews', 'bounce_rate', 
                       'avg_session_duration', 'conversions', 'revenue', 'event_count']
        for col in numeric_cols:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
        
        return data
